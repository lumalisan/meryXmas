import threading
import time

THREADS = 4



class SantaClaus(object):
    def def __init__(self):
        self.renos = 0
        
        
    def reno_lock(self):
        with self.mutex:
            while self.waiting:
                self.reno.wait()
            self.renos += 1
            self.reno.notify()
            
    def reno_unlock(self):
        with self.mutex:
            self.renos -= 1
            if not self.renos:
                self.elfo.notify()
                
    def elfo_lock(self):
        with self.mutex:
            while self.elfos or self.renos:
                self.elfo.wait()
            self.elfos = True
            
    def elfo_unlock(self):
        with self.mutex:
            self.elfos = False
            self.reno.notify()
            self.elfo.notify()
            
counter = 0
def thread(sc):
    global counter
    id = threading.currentThread().name
    print()

elfos = ["Taleasin", "Halafarin", "Ailduin", "Adamar", "Galather", "Estelar", "Lyari", "Andrathath", "Wyn"]

renos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]


def Santa():
    print("-------> Santa says: I'm tired")
    print("-------> Santa says: I'm going to sleep")
    
    print("-------> Santa says: I'm awake ho ho ho!")
    print("-------> Santa says: Toys are ready!")
    print("Santa loads the toys")
    print("-------> Santa says: Until next Christmas")
    
