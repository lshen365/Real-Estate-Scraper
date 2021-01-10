import math

class Max_Priority:

    def __init__(self):
        self.queue = []
        self.size = 0

    def get_parent(self,index):
        return self.queue[math.floor((index-1)/2)]

    def get_left_child(self,index):
        print("index is: {} and size is {}".format(index,self.size))
        return self.queue[math.floor(index*2)+1]

    def get_right_child(self,index):
        return self.queue[math.floor(index*2+2)]

    def get_parent_index(self,index):
        return math.floor((index-1)/2)

    def get_left_child_index(self,index):
        return index*2+1

    def get_right_child_index(self,index):
        return index*2+2

    def does_left_child_exist(self,index):
        index = self.get_left_child_index(index)
        if index < self.size:
            return True
        return False

    def does_right_child_exist(self,index):
        index = self.get_right_child_index(index)
        if index < self.size:
            return True
        return False

    def does_parent_exist(self,index):
        if index >0:
            return True
        return False

    def swap(self,loc1,loc2):
        #Takes in INDEX location of values
        temp = self.queue[loc1]
        self.queue[loc1] = self.queue[loc2]
        self.queue[loc2] = temp
        print("swapped {} and {}".format(self.queue[loc1],self.queue[loc2]))

    def insert(self,value):
        self.queue.append(value)
        self.size += 1
        self.heapify_up()

    def print(self):
        for x in self.queue:
            print(x, end=" ")
    def heapify_up(self):
        index = self.size - 1
        while(self.does_parent_exist(index) and self.get_parent(index) <= self.queue[index]):
            self.swap(index,self.get_parent_index(index))
            index = self.get_parent_index(index)
            self.print()
        print("successfully heapified")

    def heapify_down(self):
        index = 0
        while self.does_left_child_exist(index):
            loc = self.get_left_child_index(index)
            print("{} {}".format(self.get_left_child(index),self.get_right_child(index)))
            if self.does_right_child_exist(index) and self.get_left_child(index) < self.get_right_child(index):
                loc = self.get_right_child_index(index)
            self.swap(index,loc)
            index = loc


    def remove(self):
        self.swap(0,self.size-1)
        self.print()
        self.queue.pop()
        self.size -= 1
        self.heapify_down()


test = Max_Priority()
test.insert(10010)
test.insert(5555)
test.insert(13005)
test.insert(28349)
print("Removing now...")
test.remove()
test.print()