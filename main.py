import numpy
import wave
import re

sampleRate = 44100
length = 0.07 # 70ms
pause = 0.05 # 50ms

reg = "[\d]|\*|#|[A-D]" #regular expression

def createSineWave(freq):
    time = numpy.linspace(0, length, round(length * sampleRate))

    return 0.5 * numpy.sin(freq * 2 * numpy.pi * time)

def createBreak():
    return numpy.linspace(0, pause, round(pause * sampleRate))



def getUserInput():

    userAcceptsInput = False

    while not userAcceptsInput:
        telephoneNumber = input("Wie lautet deine Telefonnummer? ")

        filteredInput = ""

        for _, tNumber in enumerate([*telephoneNumber]):
            
            isValidChar = re.search(reg, tNumber.upper())

            if(isValidChar != None):
                filteredInput = filteredInput + tNumber
        
        print("Das ist deine Telefonnummer: " + filteredInput + " Ist das richtig (Schreibe \"Ja\" oder \"Nein\") ")

        while True:
            userDecision = input("")

            if userDecision == "Ja":
                userAcceptsInput = True
                break
            elif userDecision == "Nein":
                userAcceptsInput == False
                break
    return filteredInput



def convertNumberToDTMF(input):
    match input:
        case "1":
            return createSineWave(697) + createSineWave(1209)
        case "2":
            return createSineWave(697) + createSineWave(1336)
        case "3":
            return createSineWave(697) + createSineWave(1477)
        case "A":
            return createSineWave(697) + createSineWave(1633)
        case "4":
            return createSineWave(770) + createSineWave(1209)
        case "5":
            return createSineWave(770) + createSineWave(1336)
        case "6":
            return createSineWave(770) + createSineWave(1477)
        case "B":
            return createSineWave(770) + createSineWave(1633)
        case "7":
            return createSineWave(852) + createSineWave(1209)
        case "8":
            return createSineWave(852) + createSineWave(1336)
        case "9":
            return createSineWave(852) + createSineWave(1477)
        case "C":
            return createSineWave(852) + createSineWave(1633)
        case "*":
            return createSineWave(941) + createSineWave(1209)
        case "0":
            return createSineWave(942) + createSineWave(1336)
        case "#":
            return createSineWave(942) + createSineWave(1477)
        case "D":
            return createSineWave(942) + createSineWave(1633)
            

def createFile(data):
    wavFile = wave.open('beepboop.wav','w')

    wavFile.setnchannels(1) # mono
    wavFile.setsampwidth(2) # 2 byte = 16 bits
    wavFile.setframerate(sampleRate)

    # Convert to (little-endian) 16 bit integers.
    data = (data * (2 ** 15 - 1)).astype("<h") # dankeschön lieber User in stackoverflow

    wavFile.writeframes(data)
    wavFile.close()

def generateFile(telephoneNumber):
    data = 1
    for index, tNumber in enumerate([*telephoneNumber]):
        tNumber = tNumber.upper()
        y = re.search(reg, tNumber)
        if y:
            toneAndPause = numpy.append(convertNumberToDTMF(tNumber), createBreak())
            data = numpy.append(data, toneAndPause)
    createFile(data)



def main():
    userInput = getUserInput()
    generateFile(userInput)

if __name__ == "__main__":
    main()
