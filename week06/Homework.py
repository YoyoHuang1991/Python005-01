# <h3>具体要求：</h3>
# * 定义“动物”、“猫”、“狗”、“动物园”四个类，动物类不允许被实例化。
# * 动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
# * 猫类要求有“叫声”、“是否适合作为宠物”以及“名字”三个属性，其中“叫声”作为类属性，除凶猛动物外都适合作为宠物，猫类继承自动物类。狗类属性与猫类相同，继承自动物类。
# * 动物园类要求有“名字”属性和“添加动物”的方法，“添加动物”方法要实现同一只动物（同一个动物实例）不能被重复添加的功能。

from abc import ABCMeta, abstractmethod
shapes = {'大':3, '中等':2, '小':1 }
class Animal(metaclass=ABCMeta):
    #动物类要求定义“类型”、“体型”、“性格”、“是否属于凶猛动物”四个属性，是否属于凶猛动物的判断标准是：“体型 >= 中等”并且是“食肉类型”同时“性格凶猛”。
    
    @abstractmethod
    def __init__(self, eat, shape, character):
        self.eat = eat
        self.shapeValue = shapes[shape] #分1小、2中等、3大
        self.character = character
        if self.shapeValue >= 2 and self.eat == "食肉" and self.character == "兇猛":
            self.isFerocious = True
        else:
            self.isFerocious = False

class Cat(Animal):
    sound = 'Mew'
    def __init__(self, name, eat, shape, character):
        self.name = name
        super().__init__(eat, shape, character)
        self.suit_pet = not self.isFerocious
        
class Dog(Animal):
    sound = 'Wang'
    def __init__(self, name, eat, shape, character):
        self.name = name
        super().__init__(eat, shape, character)
        self.suit_pet = not self.isFerocious       

class Zoo(object):
    def __init__(self, name):
        self.name = name
        self.animals = set()

    def add_animal(self,animal): 
        if animal in self.animals:
            return "已有該動物實例"       
        if animal.__class__.__name__ not in self.animals:
            self.__dict__[animal.__class__.__name__]=animal.__class__.__name__
        self.animals.add(animal)
        for an in self.animals:
            print(an.name)

if __name__ == '__main__':
    # 实例化动物园
    z = Zoo('时间动物园')
    # 实例化一只猫，属性包括名字、类型、体型、性格
    cat1 = Cat('大花猫 1', '食肉', '小', '温顺')
    # 增加一只猫到动物园
    z.add_animal(cat1)
    # 动物园是否有猫这种动物
    have_cat = hasattr(z, 'Cat')