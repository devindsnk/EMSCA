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
        self.burstLength = int(pcktSenderConfig['burstLength'])
        
        # print("Src: ", self.src, "\nDest: ", self.dest, "\nInterface:", self.iface)

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

    def getPatterns(self):
        patterns = [self.P1, self.P2, self.P3, self.P4]
        return patterns

    def sendPackets(self, pattern, events):
        
        ipPacket = pattern()
        print(f'\t{ipPacket}')

        print("\tSender: Waiting for emCollector")
        events["emCollectorReady"].wait()
        print("\tSender: EM collector ready detected")

        events["pcktSendingStarted"].set()
        print("\tSender: Packet sending started")

        send(ipPacket, count=self.burstLength, verbose=False, iface = self.iface)

        events["pcktSendingCompleted"].set()
        print("\tSender: Packet sending completed\n")

        # NDD : end sniffing

    


