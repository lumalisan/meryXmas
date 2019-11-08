import threading
import time

# Wait = Acquire
# Signal = Release
# https://www.youtube.com/watch?v=pqO6tKN2lc4

RENOS = 9
ELFOS = 9

nombreElfos = ["Taleasin", "Halafarin", "Ailduin", "Adamar", "Galather", "Estelar", "Lyari", "Andrathath", "Wyn"]

nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]

class meryXmas(object):
    def __init__(self):
        self.contadorElfos = 0
        self.contadorRenos = 0
        self.mutex = threading.Lock()
        self.elfoMutex = threading.Lock()
        self.santaSem = threading.Semaphore(0)
        self.elfoSem = threading.Semaphore(0)
        self.renoSem = threading.Semaphore(0)
        
    def reno(self):
        #Lo que esta dentro del with es la seccion critica
        with self.mutex:
            print("{} here!".format(nombreRenos[self.contadorRenos]))
            self.contadorRenos += 1
            if self.contadorRenos == 9:
                self.santaSem.release()
        self.renoSem.acquire()
        prepararReno()
    
    def santa(self):
        self.santaSem.acquire()
        print("-------> Santa says: I'm awake ho ho ho!")
        with self.mutex:
            if self.contadorRenos == 9:
                self.contadorRenos = 0
                prepararTrineo()
                self.renoSem.release(9)
            else:
                self.elfoSem.release(3)
                ayudarElfos()
                
    def elfo(self):
        self.elfoMutex.acquire()
        with self.mutex:
            self.contadorElfos += 1
            if self.contadorElfos == 3:
                self.santaSem.release()
            else:
                self.elfoMutex.release()
        self.elfoSem.acquire()
        pedirAyuda()
        with self.mutex:
            self.contadorElfos -= 1
            if self.contadorElfos == 0:
                self.elfoMutex.release()
            
                
                

def prepararReno(self):
    

counter = 0
def thread(sc):
    global counter
    id = threading.currentThread().name
    print()


def Santa():
    print("-------> Santa says: I'm tired")
    print("-------> Santa says: I'm going to sleep")
    
    print("-------> Santa says: I'm awake ho ho ho!")
    print("-------> Santa says: Toys are ready!")
    print("Santa loads the toys")
    print("-------> Santa says: Until next Christmas")
    
def main():
    threads = []

    buffer = meryXmas()
    for i in range(ELFOS):
        e = threading.Thread(target=consumer, args=(buffer,))
        threads.append(e)

    for i in range(RENOS):
        r = threading.Thread(target=producer, args=(buffer,))
        threads.append(r)

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    print("End")


if __name__ == "__main__":
    main()