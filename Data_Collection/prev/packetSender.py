from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, fragment
from typing import List
import configparser
import logging
import time
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

config = configparser.ConfigParser()


class PacketSender():
    protocol: str
    src: str
    iface: str
    payload = str
    packetCount: int
    packet: UDP
    frags: List[str]
    patternData = {
        "protocol": ['TCP'],
        "payload": [b'\x00']
    }
    # patternData = {
    #     "protocol": ['UDP', 'TCP'],
    #     "payload": [b'\x00' * 1472, b'\xff' * 1472]
    # }

    def __init__(self) -> None:
        self.readConfig()

    def readConfig(self) -> None:
        config.read('config.ini')
        defaultConfig = config['default']

        self.src = defaultConfig['source']
        self.dest = defaultConfig['destination']
        self.iface = defaultConfig['iface']
        self.duration = defaultConfig['duration']
        # self.payload = defaultConfig['payload']
        # self.protocol = defaultConfig['protocol']
        # self.packetCount = int(defaultConfig['packetCount'])

        print("Src: ", self.src, "\nDest: ",
              self.dest, "\nInterface:", self.iface)

    def definePacket(self, protocol, payload):
        # NDD : define packet based on passed parameters
        if protocol == 'UDP':
            self.packet = IP(dst=self.dest, proto=17)/UDP(sport=1100, dport=1200)/(payload*1472)
            self.frags = fragment(self.packet)
        elif protocol == 'TCP':
            self.packet = IP(dst=self.dest, proto=6)/TCP(dport=1200)/(payload*1460)
            self.frags = fragment(self.packet)
        else:
            raise ValueError("Invalid protocol. Supported protocols are 'UDP' and 'TCP'.")
        

    def sendPackets(self):
        # NDD : send packets for specific duration and log it properly as well
        print("Sending Packet...", self.packet)
        send(self.packet, count=1, verbose=False, iface=self.iface)

    def simulatePatterns(self):
        for payload in self.patternData['payload']:
            for protocol in self.patternData['protocol']:
                endTime = time.time() + int(self.duration)
                while time.time() < endTime:
                    print("Sending" ,protocol ,"packet with payload",payload)
                    self.definePacket(protocol, payload)
                    print(self.packet)
                    # print(sender.frags)
                    self.sendPackets()
                    print("\n\n\n")                

if __name__ == "__main__":
    sender = PacketSender()
    # sender.sendPackets()
    sender.simulatePatterns()
    # print()
