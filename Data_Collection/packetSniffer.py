import configparser
from scapy.all import *

class PacketSniffer:
    def __init__(self) -> None:
        self.readConfig()

    def readConfig(self) -> None:
        config = configparser.ConfigParser()
        config.read('./config.ini')
        pcktSnifferConfig = config['PacketSniffer']

        self.snifferIface = pcktSnifferConfig['iface']
        self.snifferOutputPath = pcktSnifferConfig['outputPath']
        self.sniffDuration = float(pcktSnifferConfig['sniffDuration'])

    def getFilePath(self, pattern, freq,):
        path = f"{self.snifferOutputPath}/{pattern}_{freq}Mhz_sniffed.pcap"

        if not os.path.isdir(self.snifferOutputPath):
            os.mkdir(self.snifferOutputPath)

        return path

    def sniffPackets(self, pattern, freq, destIP, events):
        path = self.getFilePath(pattern.__name__, freq)

        print("\tSniffer: Waiting for emCollector")
        events["emCollectorReady"].wait()
        print("\tSniffer: Detected emCollector ready")

        print("\tSniffer: Set pcktSniffer ready")
        events["pcktSnifferReady"].set()

        filterExpression = f"ip dst {destIP}"

        print("\tSniffer: Waiting for pcktSender")
        events["pcktSendingStarted"].wait()
        print("\tSniffer: Detected pcktSender started")

        print("\tSniffer: Sniffing started...")
        pckts = sniff(filter=filterExpression, iface=self.snifferIface, timeout=self.sniffDuration)
        print("\tSniffer: Detected packet sending completed")
        print("\tSniffer: Sniffing completed and writing...")
        wrpcap(path, pckts)
        print("\tSniffer: Pcap file saved")

