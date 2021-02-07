# 示例代码
import threading
import queue

class lockToCountEating:
   def __init__(self, count):
      self.count = count
      self.condition = threading.Condition()
   
   def wait(self):
      """ 
      1. 等待所有線程完成，再讓程序繼續執行後續的打印結果。
      2. threading.Condition()是一個鎖及等待池。當acquire()鎖後，執行wait()，會進行阻塞(blocked狀態)，並釋放Condition內部鎖，並在等待池waiting pool紀錄該狀態。直到count_down()，除了count - 1外，執行confition.notify()，會喚醒waiting pool中的程序，即方才blocked狀態的wait()。但count>0，故仍在while循環中，直到count>0離開迴圈，finally裡Condition.release()，才將waiting pool的所有鎖皆釋放，才會繼續進行程序。
      """
      try:
         self.condition.acquire()
         while self.count > 0:
            self.condition.wait()

      finally:
         self.condition.release()

   def count_down(self):
      try:
         self.condition.acquire() 
         #做count計算和喚醒wait()確認count是否>0前，需要上鎖，否則wait()會確認不到正確的數值，在確認錢可能被其他線程修改。
         self.count -= 1
         self.condition.notify()
         # notify()從waiting pool通知一個線程acquire一個內部鎖；notifyAll()通知所有在waiting pool的線程acquire一個內部鎖，目的在防止有永遠沉默的線程。
      finally:
         self.condition.release()


class DiningPhilosophers(threading.Thread):
   def __init__(self,
               philosopher,
               leftFork,
               rightFork,
               queueResult,
               lockToCountEating):
      super().__init__()
      self.name = philosopher
      self.leftFork = leftFork
      self.rightFork = rightFork
      self.queueResult = queueResult
      self.lockToCountEating = lockToCountEating

   # 1. 拿起左邊的叉子: [人名, 1:左邊, 1:拿起]，將結果存到queueResult
   def pickLeftFork(self):
      self.queueResult.put([self.name, 1, 1])

   # 2. 拿起右邊的叉子: [人名, 2:右邊, 1:拿起]，將結果存到queueResult
   def pickRightFork(self):
      self.queueResult.put([self.name, 2, 1])

   # 3. 放下左邊的叉子: [人名, 1:左邊, 2:放下]，(1)釋放鎖 (2)將結果存到queueResult
   def putLeftFork(self):
      self.leftFork.release()
      self.queueResult.put([self.name, 1, 2])

   # 4. 放下右邊的叉子: [人名, 1:右邊, 2:放下]，(1)釋放鎖 (2)將結果存到queueResult
   def putRightFork(self):
      self.rightFork.release()
      self.queueResult.put([self.name, 2, 2])

   # 5. 吃: [人名, 0: 不分左右, 3:吃麵]
   def eat(self):
      self.queueResult.put([self.name, 0, 3])

   """
   主要邏輯: 
      (1)死循環直到「吃到」，將鎖存器的count總數減去1，並終止循環、該線程。
      (2)acquire(blocking=False)，非阻塞狀態，無論有無得到鎖，皆立即返回布林值。
      (3)當拿到 "兩個叉(鎖)"，執行拿兩叉、吃、放兩叉，再"鎖存器count - 1"，結束該線程。
      (4)當只拿到 "左叉(鎖)"，沒法吃所以釋放掉 "左叉(鎖)"
      (5)當只拿到 "右叉(鎖)"，沒法吃所以釋放掉 "右叉(鎖)"
   """
   def run(self):
      while True:
         left = self.leftFork.acquire(blocking=False)
         right = self.rightFork.acquire(blocking=False)
         
         if left and right:
            self.pickLeftFork()
            self.pickRightFork()
            self.eat()
            self.putLeftFork()
            self.putRightFork()

            self.lockToCountEating.count_down()
            break

         elif left and not right:
            self.leftFork.release()

         elif right and not left:
            self.rightFork.release()

         else:
            pass

"""
1. 建立儲存結果的queue
2. 建立五支叉(鎖)
3. 建立一個鎖存器，紀錄五位哲學家eat次數的總數，當總數被減為零時，代表五位哲學家皆飲食完成。
   (1) 例如: n = 3時，5位哲學家皆要eat 3次，等於5位哲學家各發起3個線程，即總共有15線程。
   (2) 每個哲學家會做5個動作，拿起左叉、拿起右叉、吃、放下左叉、放下右叉，所以結果list會有5(行為數)*5(人)*3(次)，總共75個行為紀錄。
"""
if __name__ == '__main__':
   queueResult = queue.Queue()

   fork1 = threading.Lock()
   fork2 = threading.Lock()
   fork3 = threading.Lock()
   fork4 = threading.Lock()
   fork5 = threading.Lock()

   while True:
      try:
         n = int(input("input a num between 1 and 60(included)>> "))
      except:
         print("it's not a integer.")
      
      if n > 60 or n < 1:
         print("Please input correct value.")
         continue
      else:
         break
   
   # 5位哲學家各吃n次，總共5 * n次 = count
   lockToCount = lockToCountEating(5 * n)

   # 為5位哲學家分別建立n個線程
   for _ in range(n):
      ph0 = DiningPhilosophers(0, fork5, fork1, queueResult, lockToCount)
      ph0.start()

      ph1 = DiningPhilosophers(1, fork1, fork2, queueResult, lockToCount)
      ph1.start()

      ph2 = DiningPhilosophers(2, fork2, fork3, queueResult, lockToCount)
      ph2.start()

      ph3 = DiningPhilosophers(3, fork3, fork4, queueResult, lockToCount)
      ph3.start()

      ph4 = DiningPhilosophers(4, fork4, fork5, queueResult, lockToCount)
      ph4.start()  

   lockToCount.wait()
   lst_result = []

   while not queueResult.empty():
      lst_result.append(queueResult.get())

   print(lst_result)