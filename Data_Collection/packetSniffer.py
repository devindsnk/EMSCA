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

    def getFilePath(self, pattern, freq,):
        path = f"{self.outputPath}/{pattern}_{freq}Mhz_sniffed.pcap"
        return path

    def sniffPackets(self, pattern, freq, destIP):
        global events 

        path = self.getFilePath(pattern.__name__, freq)

        print("\tSniffer: Waiting for emCollector")
        events["emCollectorReady"].wait()
        print("\tSniffer: Detected emCollector ready")

        events["pcktSnifferReady"].set()
        print("\tSniffer: Set pcktSniffer ready")

        filterExpression = f"ip dst {destIP}"

        print("\tSniffer: Waiting for pcktSender")
        events["pcktSendingStarted"].wait()
        print("\tSniffer: Detected pcktSender started")

        print("\tSniffer: Sniffing started...")
        pckts = sniff(filter=filterExpression, iface=self.snifferIface, stop_filter=self.checkStopFilter)
        print("\tSniffer: Detected packet sending completed")
        print("\tSniffer: Sniffing completed and writing...")
        wrpcap(path, pckts)
        print("\tSniffer: Pcap file saved")

    def checkStopFilter(self) -> bool:
        global events
        if events["pcktSendingCompleted"].wait():
            return True
        else:
            return False


    # def filterPackets(self):
    #     pass
