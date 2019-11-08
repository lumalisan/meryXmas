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
            self.contadorRenos += 1
            if self.contadorRenos == 9:
                print("Reindeer {} I'm the 9!".format(nombreRenos[self.contadorRenos - 1]))
                self.santaSem.release()
            else:
                print("Reindeer {} arrives!".format(nombreRenos[self.contadorRenos - 1]))
        self.renoSem.acquire()
        with self.mutex:
            self.contadorRenos -= 1
            prepararReno(nombreRenos[self.contadorRenos])

    def santa(self):
        print("-------> Santa says: I'm going to sleep")
        self.santaSem.acquire()
        print("-------> Santa says: I'm awake ho ho ho!")
        with self.mutex:
            if self.contadorRenos == 9:
                #self.contadorRenos = 0
                prepararTrineo()
                #self.renoSem.release(9)
                for i in range(9):
                    self.renoSem.release()
                    self.contadorRenos -= 1
            else:
                #self.elfoSem.release(3)
                for i in range(3):
                    self.elfoSem.release()
                ayudarElfos()

    def elfo(self):
        self.elfoMutex.acquire()
        with self.mutex:
            self.contadorElfos += 1
            print("Elf {} says: I have a question, I'm the {} waiting...".format(nombreElfos[self.contadorElfos - 1], self.contadorElfos))
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




def prepararReno(name):
    print("{} ready and hitched".format(name))

def prepararTrineo():
    print("-------> Santa says: Toys are ready!")
    print("Santa loads the toys")
    print("-------> Santa says: Until next Christmas")

def ayudarElfos():
    print("PPEP")

def pedirAyuda():
    print("stephanie who S U C C S like a PPEP")



# Creamos las funciones de los threads
def threadSanta(mxm):
    print("-------> Santa says: I'm tired")
    mxm.santa()

def threadRenos(mxm):
    print("{} here!".format(nombreRenos[self.contadorRenos]))
    mxm.reno()

def threadElfos(mxm):
    print("Hi I am the elf {}".format(nombreElfos[self.contadorElfos]))
    mxm.elfo()



def main():
    threads = []

    mxm = meryXmas()

    # Creamos el thread de santa
    s = threading.Thread(target=threadSanta, args=(mxm,))
    threads.append(s)

    # Creamos los threads de los renos
    for i in range(RENOS):
        r = threading.Thread(target=threadRenos, args=(mxm,))
        threads.append(r)

    # Creamos los threads de los elfos
    for i in range(ELFOS):
        e = threading.Thread(target=threadElfos, args=(mxm,))
        threads.append(e)

    # Iniciamos los threads
    for t in threads:
        t.start()

    # Esperamos a que acaben
    for t in threads:
        t.join()

    print("Ejecución finalizada correctamente")


if __name__ == "__main__":
    main()
