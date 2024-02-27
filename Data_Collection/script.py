
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
    freqs = emCollector.getFreqs()

    for pattern in patterns:
        for freq in freqs:

            threadPacketSender = threading.Thread(target=pcktSender.sendPackets, args=(pattern, events))
            # threadPacketSniffer = threading.Thread(target=pcktSniffer.sniffPackets)
            threadEMCollector = threading.Thread(target=emCollector.collectEMData, args=(pattern, freq, events))

            threadPacketSender.start()
            threadEMCollector.start()

            threadPacketSender.join()
            threadEMCollector.join()

    #         # self.initTransmission(pattern.__name__, freq)


    #         self.sendPackets(pattern)

simulation()
