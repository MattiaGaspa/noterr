from time import sleep

riga = "Mattia"
i = 0

while(True):
    with open("test", "a") as f:
        f.write(riga + str(i) + "\n")
        i += 1
        sleep(3)
