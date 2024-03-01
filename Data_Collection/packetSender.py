import configparser
import time
from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, fragment


class PacketSender:

    def __init__(self) -> None:
        self.readConfig()
        self.packet = None

    def readConfig(self) -> None:
        config = configparser.ConfigParser()
        config.read('./config.ini')
        pcktSenderConfig = config['PacketSender']

        self.src = pcktSenderConfig['source']
        self.dest = pcktSenderConfig['destination']
        self.iface = pcktSenderConfig['iface']
        self.burstDuration = float(pcktSenderConfig['burstDuration'])
        
        # print("Src: ", self.src, "\nDest: ", self.dest, "\nInterface:", self.iface)

    def P0(self) -> None:
        '''IDLE Line No Traffic'''
        return None

    def P1(self) -> IP:
        ''' P1 : all 0 UDP '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes 
        # UDP header : 8 bytes 
        # Payload : 1472
        payload = bytearray(1472)
        ipPacket = IP(dst=self.dest)/UDP()/Raw(load=payload)

        return ipPacket

    def P2(self) -> IP:
        ''' P2 : all 1 UDP '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes 
        # UDP header : 8 bytes 
        # Payload : 1472
        payload = bytearray([255]*1472)
        ipPacket = IP(dst=self.dest)/UDP()/Raw(load=payload)

        return ipPacket

    def P3(self) -> IP:
        ''' P3 : all 0 TCP '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes 
        # TCP header : 20 bytes 
        # Payload : 1460
        payload = bytearray(1460)
        ipPacket = IP(dst=self.dest)/TCP(dport=1200)/Raw(load=payload)

        return ipPacket

    def P4(self) -> IP:
        ''' P4 : all 1 TCP '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes 
        # TCP header : 20 bytes 
        # Payload : 1460
        payload = bytearray([255]*1460)
        ipPacket = IP(dst=self.dest)/TCP()/Raw(load=payload)

        return ipPacket

    def P5(self) -> IP:
        ''' P5 : all 0 raw IP packet '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes
        # Payload : 1480
        payload = bytearray(1480)
        ipPacket = IP(dst=self.dest)/Raw(load=payload)

        return ipPacket

    def P6(self) -> IP:
        ''' P6 : all 1 raw IP packet '''
        # Max unfragmented packet size : 1500 bytes 
        # IP header : 20 bytes
        # Payload : 1480
        payload = bytearray([255]*1480)
        ipPacket = IP(dst=self.dest)/Raw(load=payload)

        return ipPacket

    def getPatterns(self):
        # patterns = [self.P0, self.P1, self.P2, self.P3, self.P4, self.P5, self.P6]
        patterns = [self.P5, self.P6]
        return patterns

    def getDestIP(self):
        return self.dest

    def sendPackets(self, pattern, events):
        ipPacket = pattern()
        print(f'\t{ipPacket}')

        print("\tSender: Waiting for sniffer")
        events["pcktSnifferReady"].wait()
        print("\tSender: Detected sniffer ready")

        print("\tSender: Packet sending started...")
        events["pcktSendingStarted"].set()

        endTime = time.time() + self.burstDuration

        while time.time() < endTime:
            if(ipPacket):
                send(ipPacket, verbose=False, iface = self.iface)
        
        print("\tSender: Packet sending completed\n")
        events["pcktSendingCompleted"].set()
        
