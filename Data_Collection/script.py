
from packetSender import PacketSender
from packetSniffer import PacketSniffer
from emCollector import EMCollector

import threading

pcktSender = PacketSender()
pcktSniffer = PacketSniffer()
emCollector = EMCollector()

# defining threading events
events = {
    "pcktSnifferReady": threading.Event(),
    "emCollectorReady": threading.Event(),
    "pcktSendingStarted": threading.Event(),
    "pcktSendingCompleted": threading.Event()
}

def simulation():
    patterns = pcktSender.getPatterns()
    destIP = pcktSender.getDestIP()
    freqs = emCollector.getFreqs()
    

    for pattern in patterns:
        for freq in freqs:

            threadPacketSender = threading.Thread(target=pcktSender.sendPackets, args=(pattern))
            threadPacketSniffer = threading.Thread(target=pcktSniffer.sniffPackets, args=(pattern, freq, destIP))
            threadEMCollector = threading.Thread(target=emCollector.collectEMData, args=(pattern, freq))

            threadPacketSender.start()
            threadEMCollector.start()

            threadPacketSender.join()
            threadEMCollector.join()

    #         # self.initTransmission(pattern.__name__, freq)


    #         self.sendPackets(pattern)

simulation()
