'''
Created on 2016-7-27

'''
#!/usr/bin/env python
#! encoding=utf-8


from threading import Thread, Condition
import time
import random

queue = []
MAX_NUM = 5
condition = Condition() # Condition对象可以在某些事件触发或者达到特定的条件后才处理数据，Condition除了具有Lock对象的acquire方法和release方法外，还有wait方法、notify方法、notifyAll方法等用于条件处理


# 1、加入数据前，生产者检查队列是否满，满->等待condition.wait(),未满->继续生产
# 2、消费者可以运行/消耗，若有空余位置，通知condition.notify()生产者，唤醒condition.wait()
# 3、队列为空时，消费者等待condition.wait()，生产者生产后，通知condition.notify()消费者运行/消耗


class ProducerThread(Thread):   # 生产者线程
    isExit = False  # 循环的条件

    def run(self):
        nums = range(MAX_NUM)
        global queue    # 全局变量
        while self.isExit == False:
            condition.acquire()  # acquire()/release()：获取/释放 Lock，先acquire Lock.再release Lock
            if len(queue) == MAX_NUM:
                print ("Queue full, producer is waiting");
                condition.wait()   # wait([timeout]):线程挂起，直到收到一个notify通知或者超时（可选的，浮点数，单位是秒s）才会被唤醒继续运行
                print ("Space in queue, Consumer notified the producer");
            num = random.choice(nums)   # choice() 方法返回一个列表，元组或字符串的随机项
            queue.append(num)   # append() 方法用于在列表末尾添加新的对象
            print ("Produced", num);

            condition.notify()  # notify()方法发送通知，唤醒wait()
            condition.release() # acquire()/release()：获取/释放 Lock
            time.sleep(random.random()) # random() 方法返回随机生成的一个实数

    def end(self):
        self.isExit = True  # 循环结束     


class ConsumerThread(Thread):   # 消费者线程
    isExit = False

    def run(self):
        global queue
        while self.isExit == False:
            condition.acquire()
            if not queue:
                print ("Nothing in queue, consumer is waiting");
                condition.wait()
                print ("Producer added something to queue and notified the consumer");
            num = queue.pop(0)  # pop() 函数用于移除列表中的一个元素，并且返回该元素的值
            print ("Consumed", num);

            condition.notify()
            condition.release()
            time.sleep(random.random()) # random()返回一个0~num-1之间的随机数(整型)
            # time.sleep(random.random()) 也可写成：time.sleep(random.choice(nums)) 

    def end(self):
        self.isExit = True  # # 循环结束


p = ProducerThread();   # p 是一个Thread对象
c = ConsumerThread()    # C 是一个Thread对象

p.start()
c.start()

time.sleep(5)

p.end()
c.end()

p.join()
c.join()

# thread的join():主线程不能立即退出，必须等待p线程运行完毕才能退出。
# 此程序总共有三个线程，主线程即执行 main的线程，消费者线程c,生产者线程p，主线程不能过早退出，因为它必须等待子线程p,c工作完成才能退出，因此需要使用join等待子线程运行完毕