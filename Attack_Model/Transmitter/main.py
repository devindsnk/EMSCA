# Takes the input from the user and encodes it 
import queue
import configparser
import time
from crc import CRC
from hammingCode import Hamming
from packetSender import PacketSender

class Transmitter:

    def __init__(self) -> None:
        self.readConfig()

        self.pcktSender = PacketSender(count=self.packetCount, iface=self.iface, dest=self.destination)
        self.charBuffer = queue.Queue()
        self.frames = []

    def readConfig(self):
        config = configparser.ConfigParser()
        config.read('../config.ini')

        generalConfig = config['general']
        self.paddingChar = generalConfig['PaddingCharacter']
        self.charsPerFrame = int(generalConfig['CharsPerFrame'])
        self.payloadSize = int(generalConfig['PayloadSize'])
        self.padChar = generalConfig['PaddingCharacter']
        self.preamble = generalConfig['Preamble']
        self.bitTimeMS = int(generalConfig['BitTimeMS'])
        self.divisor = generalConfig['CRCDivisor']
        self.iface = generalConfig['NetworkInterface']
        self.destination = generalConfig['Destination']
        self.packetCount = int(generalConfig['PacketCount'])


    # prepare frames from the char buffer
    def prepFrames(self):
        ham = Hamming()

        while not(self.charBuffer.empty()):
            charStream = self.getChars(self.charsPerFrame)
            print(f'\ncharStream: {charStream}')
            # preparing ascii bin stream 
            asciiBinStream = ""
            for char in charStream:
                asciiBinStream += format(ord(char), '08b')
            print(f'asciiStreamBeforePadding:\t{asciiBinStream}')
            
            if len(charStream) < self.payloadSize:
                padLen = self.payloadSize - len(charStream)
                
                for _ in range(padLen):
                    asciiBinStream += format(ord(self.padChar), '08b')
            print(f'asciiStreamAfterPadding:\t{asciiBinStream}')

            crc = self.calcCRC(asciiBinStream)
            asciiBinStream += crc
            print(f'After adding CRC:\t\t{asciiBinStream}')

            hamCode = ""
            for i in range(0, len(asciiBinStream), 4):
                segment = asciiBinStream[i: i+4]
                enc = ham.encode(segment)
                enc = ham.matrixToString(enc)
                hamCode += enc

            print(f'After hamming encoding:\t\t{hamCode}')

            frame = self.preamble + hamCode

            print(f'After adding preamble:\t\t{frame}')

            self.frames.append(frame)

        # self.printFrames()

    # get message as a input and put into char buffer
    def getInput(self) -> None:
        message = str(input("Enter Message to Transmit: "))

        print(f'Input: {message}')

        for c in message:
            self.charBuffer.put(c)

    # returns a specific number of chars from the char buffer 
    def getChars(self, charCount:int) -> str:
        chars = ""

        for _ in range(charCount):
            if self.charBuffer.empty():
                break
            chars += self.charBuffer.get()
        
        return chars

    def calcCRC(self, dataString: str)-> str:
        c = CRC(self.divisor)
        crc = c.calculateCrc(dataString)
        return crc

    def printFrames(self):
        for e in self.frames:
            print(e)

    def getCurrentTimeMS(self) -> int:
        ms = time.time_ns() // 1_000_000
        return ms

    def sendData(self):
        for i in range(len(self.frames)):
            print(f'Frame {i}: {self.frames[i]}')
        for frame in self.frames:
            self.manchesterModulate(frame)

    def manchesterModulate(self, frame):
        bitEndTime = self.getCurrentTimeMS()

        for bit in frame:
            bitEndTime += self.bitTimeMS
            halfBitEndTime = bitEndTime - (self.bitTimeMS / 2)

            if bit == "0": self.transmitManchester0(halfBitEndTime)
            elif bit == "1": self.transmitManchester1(bitEndTime)

        print("Frame Sent")
    
    def sendPreambleCont(self):
        bitEndTime = self.getCurrentTimeMS()
        bit = "1"

        while True:
            bitEndTime += self.bitTimeMS
            halfBitEndTime = bitEndTime - (self.bitTimeMS / 2)

            if bit == "0": self.transmitManchester0(halfBitEndTime)
            elif bit == "1": self.transmitManchester1(bitEndTime)

            bit = "0" if bit == "1" else "1"

            print("Preamble sent...")
            time.sleep((self.bitTimeMS / 2) / 1000)

    def transmitManchester0(self, halfBitEndTime):
        print(f"Sending 0")

        while self.getCurrentTimeMS() < halfBitEndTime:
            self.pcktSender.sendPackets()
        time.sleep((self.bitTimeMS / 2) / 1000)

    def transmitManchester1(self, bitEndTime):
        print(f"Sending 1")

        time.sleep((self.bitTimeMS / 2) / 1000)
        while self.getCurrentTimeMS() < bitEndTime:
            self.pcktSender.sendPackets()
            

        
    


myTransmitter = Transmitter()
myTransmitter.getInput()
myTransmitter.prepFrames()
myTransmitter.sendData()
# print(myTransmitter.getChars(3))
# print(myTransmitter.getChars(6))
