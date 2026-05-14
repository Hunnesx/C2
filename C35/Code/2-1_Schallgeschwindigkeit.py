import numpy as np

def schallgeschwindigkeit(laenge, zeit): #laenge in mm, zeit in mus
    #Schallgeschwindigkeit in medium
    return(2*laenge/zeit)

def schallgeschwindigkeit_fehler(laenge, zeit, laenge_fehler, zeit_fehler):
    #Fehler der Schallgeschwindigkeit
    return(schallgeschwindigkeit(laenge, zeit) * np.sqrt((laenge_fehler/laenge)**2 + (zeit_fehler/zeit)**2))

#Fehler
laenge_fehler = 0.1 #mm
zeit_fehler = 1 #mus

##1 MHz
    
###großer zylinder
laenge_1MHz_groß = 120.76 #mm
zeit_1MHz_groß = 92 #mus

###mittlerer zylinder
laenge_1MHz_mittel = 80.81 #mm
zeit_1MHz_mittel = 61 #mus

###kleiner zylinder
laenge_1MHz_klein = 41.30 #mm
zeit_1MHz_klein = 32 #mus

print("Schallgeschwindigkeit 1 MHz großer Zylinder: ", schallgeschwindigkeit(laenge_1MHz_groß, zeit_1MHz_groß), "+/-", schallgeschwindigkeit_fehler(laenge_1MHz_groß, zeit_1MHz_groß, laenge_fehler, zeit_fehler), "mm/mus")
print("Schallgeschwindigkeit 1 MHz mittlerer Zylinder: ", schallgeschwindigkeit(laenge_1MHz_mittel, zeit_1MHz_mittel), "+/-", schallgeschwindigkeit_fehler(laenge_1MHz_mittel, zeit_1MHz_mittel, laenge_fehler, zeit_fehler), "mm/mus")
print("Schallgeschwindigkeit 1 MHz kleiner Zylinder: ", schallgeschwindigkeit(laenge_1MHz_klein, zeit_1MHz_klein), "+/-", schallgeschwindigkeit_fehler(laenge_1MHz_klein, zeit_1MHz_klein, laenge_fehler, zeit_fehler), "mm/mus")

mittelwert_1MHz = (schallgeschwindigkeit(laenge_1MHz_groß, zeit_1MHz_groß) + schallgeschwindigkeit(laenge_1MHz_mittel, zeit_1MHz_mittel) + schallgeschwindigkeit(laenge_1MHz_klein, zeit_1MHz_klein))/3
fehler_1MHz = np.sqrt(schallgeschwindigkeit_fehler(laenge_1MHz_groß, zeit_1MHz_groß, laenge_fehler, zeit_fehler)**2 + schallgeschwindigkeit_fehler(laenge_1MHz_mittel, zeit_1MHz_mittel, laenge_fehler, zeit_fehler)**2 + schallgeschwindigkeit_fehler(laenge_1MHz_klein, zeit_1MHz_klein, laenge_fehler, zeit_fehler)**2)/3
#print("Mittelwert Schallgeschwindigkeit 1 MHz: ", mittelwert_1MHz, "+/-", fehler_1MHz, "mm/mus")
print("------------------------------")
##2 MHz

###großer zylinder
laenge_2MHz_groß = 120.76 #mm
zeit_2MHz_groß = 89 #mus

###mittlerer zylinder
laenge_2MHz_mittel = 80.81 #mm
zeit_2MHz_mittel = 60 #mus

###kleiner zylinder
laenge_2MHz_klein = 41.30 #mm
zeit_2MHz_klein = 31.5 #mus

print("Schallgeschwindigkeit 2 MHz großer Zylinder: ", schallgeschwindigkeit(laenge_2MHz_groß, zeit_2MHz_groß), "+/-", schallgeschwindigkeit_fehler(laenge_2MHz_groß, zeit_2MHz_groß, laenge_fehler, zeit_fehler), "mm/mus")
print("Schallgeschwindigkeit 2 MHz mittlerer Zylinder: ", schallgeschwindigkeit(laenge_2MHz_mittel, zeit_2MHz_mittel), "+/-", schallgeschwindigkeit_fehler(laenge_2MHz_mittel, zeit_2MHz_mittel, laenge_fehler, zeit_fehler), "mm/mus")
print("Schallgeschwindigkeit 2 MHz kleiner Zylinder: ", schallgeschwindigkeit(laenge_2MHz_klein, zeit_2MHz_klein), "+/-", schallgeschwindigkeit_fehler(laenge_2MHz_klein, zeit_2MHz_klein, laenge_fehler, zeit_fehler), "mm/mus")

mittelwert_2MHz = (schallgeschwindigkeit(laenge_2MHz_groß, zeit_2MHz_groß) + schallgeschwindigkeit(laenge_2MHz_mittel, zeit_2MHz_mittel) + schallgeschwindigkeit(laenge_2MHz_klein, zeit_2MHz_klein))/3
fehler_2MHz = np.sqrt(schallgeschwindigkeit_fehler(laenge_2MHz_groß, zeit_2MHz_groß, laenge_fehler, zeit_fehler)**2 + schallgeschwindigkeit_fehler(laenge_2MHz_mittel, zeit_2MHz_mittel, laenge_fehler, zeit_fehler)**2 + schallgeschwindigkeit_fehler(laenge_2MHz_klein, zeit_2MHz_klein, laenge_fehler, zeit_fehler)**2)/3
#print("Mittelwert Schallgeschwindigkeit 2 MHz: ", mittelwert_2MHz, "+/-", fehler_2MHz, "mm/mus")
print("------------------------------")

##4 MHz

###mittlerer zylinder
laenge_4MHz_mittel = 80.81 #mm
zeit_4MHz_mittel = 59 #mus

###kleiner zylinder
laenge_4MHz_klein = 41.30 #mm
zeit_4MHz_klein = 30 #mus

print("Schallgeschwindigkeit 4 MHz mittlerer Zylinder: ", schallgeschwindigkeit(laenge_4MHz_mittel, zeit_4MHz_mittel), "+/-", schallgeschwindigkeit_fehler(laenge_4MHz_mittel, zeit_4MHz_mittel, laenge_fehler, zeit_fehler), "mm/mus")
print("Schallgeschwindigkeit 4 MHz kleiner Zylinder: ", schallgeschwindigkeit(laenge_4MHz_klein, zeit_4MHz_klein), "+/-", schallgeschwindigkeit_fehler(laenge_4MHz_klein, zeit_4MHz_klein, laenge_fehler, zeit_fehler), "mm/mus")

mittelwert_4MHz = (schallgeschwindigkeit(laenge_4MHz_mittel, zeit_4MHz_mittel) + schallgeschwindigkeit(laenge_4MHz_klein, zeit_4MHz_klein))/2
fehler_4MHz = np.sqrt(schallgeschwindigkeit_fehler(laenge_4MHz_mittel, zeit_4MHz_mittel, laenge_fehler, zeit_fehler)**2 + schallgeschwindigkeit_fehler(laenge_4MHz_klein, zeit_4MHz_klein, laenge_fehler, zeit_fehler)**2)/2
#print("Mittelwert Schallgeschwindigkeit 4 MHz: ", mittelwert_4MHz, "+/-", fehler_4MHz, "mm/mus")