import threading
import time

# Wait = Acquire
# Signal = Release
# https://www.youtube.com/watch?v=pqO6tKN2lc4
# CADA ELFO PUEDE PREGUNTAR COMO MAXIMO 2 VECES

RENOS = 9
ELFOS = 9

nombreElfos = ["Taleasin", "Halafarin", "Ailduin", "Adamar", "Galather", "Estelar", "Lyari", "Andrathath", "Wyn"]

nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]

contadorElfos = 0
contadorRenos = 0
contadorTurnos = 0
contadorTurnosElfos = 0

class meryXmas(object):
    def __init__(self):
        self.mutex = threading.Lock()
        self.elfoMutex = threading.Lock()
        self.santaSem = threading.Semaphore(0)
        self.elfoSem = threading.Semaphore(0)
        self.renoSem = threading.Semaphore(0)

    def reno(self, i):
        global contadorRenos
        #Lo que esta dentro del with es la seccion critica
        with self.mutex:
            contadorRenos += 1
            if contadorRenos == 9:
                print("Reindeer {} I'm the 9!".format(nombreRenos[i]))
                self.santaSem.release()
            else:
                print("Reindeer {} arrives!".format(nombreRenos[i]))
        self.renoSem.acquire()
        with self.mutex:
            contadorRenos -= 1
            prepararReno(nombreRenos[contadorRenos])
        print("Elf {} ends".format(nombreRenos[i]))

    def santa(self):
        global contadorRenos
        global contadorTurnos
        while contadorTurnos != 6:
            print("-------> Santa says: I'm going to sleep")
            self.santaSem.acquire()
            print("-------> Santa says: I'm awake ho ho ho!")
            with self.mutex:
                if contadorRenos == 9:
                    #self.contadorRenos = 0
                    prepararTrineo()
                    #self.renoSem.release(9)
                    for i in range(9):
                        self.renoSem.release()
                        contadorRenos -= 1
                else:
                    #self.elfoSem.release(3)
                    ayudarElfos()
                    for i in range(3):
                        self.elfoSem.release()
                        pedirAyuda(i + 1)
                    print("-------> Santa ends turn {}".format(contadorTurnos + 1)) 
                    contadorTurnos += 1

    def elfo(self, i):
        global contadorElfos
        while contadorTurnosElfos != 2:
            self.elfoMutex.acquire()
            with self.mutex:
                contadorElfos += 1
                print("Elf {} says: I have a question, I'm the {} waiting...".format(nombreElfos[i], contadorElfos))
                if contadorElfos == 3:
                    self.santaSem.release()
                else:
                    self.elfoMutex.release()
            self.elfoSem.acquire()
            with self.mutex:
                contadorElfos -= 1
                if contadorElfos == 0:
                    self.elfoMutex.release()
        print("Elf {} ends".format(nombreElfos[i]))


def prepararReno(name):
    print("{} ready and hitched".format(name))

def prepararTrineo():
    print("-------> Santa says: Toys are ready!")
    print("Santa loads the toys")
    print("-------> Santa says: Until next Christmas")

def ayudarElfos():
    print("-------> Santa says: What is the problem BITCH!")

def pedirAyuda(contadorAyuda):
    print("-------> Santa helps the elf {} of 3".format(contadorAyuda))
    

# Creamos las funciones de los threads
def threadSanta(mxm):
    print("-------> Santa says: I'm tired")
    mxm.santa()

def threadRenos(mxm, i):
    print("{} here!".format(nombreRenos[i]))
    time.sleep(1)
    mxm.reno(i)

def threadElfos(mxm, i):
    print("Hi I am the elf {}".format(nombreElfos[i]))
    mxm.elfo(i)
    



def main():
    threads = []

    mxm = meryXmas()

    # Creamos el thread de santa
    s = threading.Thread(target=threadSanta, args=(mxm,))
    threads.append(s)

    # Creamos los threads de los renos
    for i in range(RENOS):
        r = threading.Thread(target=threadRenos, args=(mxm, i))
        threads.append(r)

    # Creamos los threads de los elfos
    for i in range(ELFOS):
        e = threading.Thread(target=threadElfos, args=(mxm, i))
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
