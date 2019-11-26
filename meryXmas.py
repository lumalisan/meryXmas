#####################################################################
#####################################################################
#####################################################################
#  ___   _   _  _____  _____ ______  _____  _____ 
# / _ \ | | | ||_   _||  _  || ___ \|  ___|/  ___|
#/ /_\ \| | | |  | |  | | | || |_/ /| |__  \ `--. 
#|  _  || | | |  | |  | | | ||    / |  __|  `--. \
#| | | || |_| |  | |  \ \_/ /| |\ \ | |___ /\__/ /
#\_| |_/ \___/   \_/   \___/ \_| \_|\____/ \____/ 
#                                                                                                                                                                                                                               
# _____                   _____              _                _               
#|_   _|                 /  __ \            | |              (_)              
#  | |  ____ __ _  _ __  | /  \/  __ _  ___ | |_  ___   _ __  _  _ __    __ _ 
#  | | |_  // _` || '__| | |     / _` |/ __|| __|/ _ \ | '__|| || '_ \  / _` |
# _| |_ / /| (_| || |    | \__/\| (_| |\__ \| |_| (_) || |   | || | | || (_| |
# \___//___|\__,_||_|     \____/ \__,_||___/ \__|\___/ |_|   |_||_| |_| \__,_|
#
# _      _                         _              ______              _            
#| |    (_)                       | |             | ___ \            | |           
#| |     _  ___   __ _  _ __    __| | _ __  ___   | |_/ / ___    ___ | |__    __ _ 
#| |    | |/ __| / _` || '_ \  / _` || '__|/ _ \  |    / / _ \  / __|| '_ \  / _` |
#| |____| |\__ \| (_| || | | || (_| || |  | (_) | | |\ \| (_) || (__ | | | || (_| |
#\_____/|_||___/ \__,_||_| |_| \__,_||_|   \___/  \_| \_|\___/  \___||_| |_| \__,_|
#
#####################################################################
#####################################################################
#####################################################################
###### ENLACE AL VÍDEO: {insertar enlace video aquí}     ############
#####################################################################
#####################################################################
#####################################################################

import threading
import time

RENOS = 9
ELFOS = 9

nombreElfos = ["Taleasin", "Halafarin", "Ailduin", "Adamar", "Galather", "Estelar", "Lyari", "Andrathath", "Wyn"]

nombreRenos = ["RUDOLPH", "BLITZEN", "DONDER", "CUPID", "COMET", "VIXEN", "PRANCER", "DANCER", "DASHER"]

class meryXmas(object):
    def __init__(self):
        self.mutex = threading.Lock()
        self.elfoMutex = threading.Lock()
        self.santaSem = threading.Semaphore(0)
        self.elfoSem = threading.Semaphore(0)
        self.renoSem = threading.Semaphore(0)
        self.contadorElfos = 0
        self.contadorRenos = 0

    def reno(self, i):
        #Lo que esta dentro del with es la seccion critica
        with self.mutex:
            self.contadorRenos += 1
            if self.contadorRenos == 9:
                print("Reindeer {} I'm the 9!".format(nombreRenos[i]))
                self.santaSem.release()
            else:
                print("Reindeer {} arrives!".format(nombreRenos[i]))
        self.renoSem.acquire()
        with self.mutex:
            self.contadorRenos -= 1
            prepararReno(nombreRenos[i])
        print("Reindeer {} ends".format(nombreRenos[i]))

    def santa(self):
        contadorTurnos = 1
        while contadorTurnos <= 6:
            print("-------> Santa says: I'm going to sleep")
            self.santaSem.acquire()
            print("-------> Santa says: I'm awake ho ho ho!")
            with self.mutex:
                if self.contadorRenos == 9:
                    prepararTrineo()
                    for i in range(9):
                        self.renoSem.release()
                        self.contadorRenos -= 1
                else:
                    #self.elfoSem.release(3)
                    time.sleep(0.5)
                    ayudarElfos()
                    for i in range(3):
                        self.elfoSem.release()
                        pedirAyuda(i + 1)
                    print("-------> Santa ends turn {}".format(contadorTurnos))
                    contadorTurnos += 1
        print("-------> Santa ends")

    def elfo(self, i):
        contadorTurnosElfos = 0
        while contadorTurnosElfos != 2:
            self.elfoMutex.acquire()
            with self.mutex:
                self.contadorElfos += 1
                if self.contadorElfos < 3:
                    print("Elf {} says: I have a question, I'm the {} waiting...".format(nombreElfos[i], self.contadorElfos))
                else:
                    print("Elf {} says: I have a question, I'm the {} SANTAAAAAA!!".format(nombreElfos[i], self.contadorElfos))
                if self.contadorElfos == 3:
                    self.santaSem.release()
                else:
                    self.elfoMutex.release()
            self.elfoSem.acquire()
            with self.mutex:
                self.contadorElfos -= 1
                if self.contadorElfos == 0:
                    self.elfoMutex.release()
            contadorTurnosElfos += 1
        print("Elf {} ends".format(nombreElfos[i]))


def prepararReno(name):
    print("{} ready and hitched".format(name))

def prepararTrineo():
    print("-------> Santa says: Toys are ready!")
    print("Santa loads the toys")
    print("-------> Santa says: Until next Christmas")

def ayudarElfos():
    print("-------> Santa says: What is the problem?¿?¿?!¡¡!¡¡!!!")

def pedirAyuda(contadorAyuda):
    print("-------> Santa helps the elf {} of 3".format(contadorAyuda))
    

# Creamos las funciones de los threads
def threadSanta(mxm):
    print("-------> Santa says: I'm tired")
    mxm.santa()

def threadRenos(mxm, i):
    print("{} here!".format(nombreRenos[i]))
    time.sleep(0.02)
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
