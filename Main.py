from multiprocessing import Process, Queue
import DataSource

q= Queue()
p = Process(target=DataSource.process, args=((q,)))

p.start()
p.join