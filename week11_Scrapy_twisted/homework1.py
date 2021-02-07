# 示例代码
import threading
import queue


# 當吃過的次數達到某值，回傳到鎖裡；鎖裡已經有五位哲學家回傳的值，則表示結束

class DiningPhilosophers(threading.Thread):
   def __init__(self,
               philosopher,
               leftFork,
               rightFork,
               queueResult,
               num):
      super().__init__()
      self.name = philosopher
      self.leftFork = leftFork
      self.rightFork = rightFork
      self.queueResult = queueResult

   def pickLeftFork(self):
      pass

   def pickRightFork(self):
      pass

   def eat(self):
      pass

   def putLeftFork(self):
      pass

   def putRightFork(self):
      pass

if __name__ == '__main__':
   queueResult = queue.Queue()

   fork1 = threading.Lock()

   