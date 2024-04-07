
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

            print(f"\n\n\t====== Pattern {pattern.__name__} : {freq}Mhz=====\n")
            threadPacketSender = threading.Thread(target=pcktSender.sendPackets, args=(pattern, events))
            threadPacketSniffer = threading.Thread(target=pcktSniffer.sniffPackets, args=(pattern, freq, destIP, events))
            threadEMCollector = threading.Thread(target=emCollector.collectEMData, args=(pattern, freq, events))

            threadPacketSender.start()
            threadEMCollector.start()
            threadPacketSniffer.start()

            threadPacketSender.join()
            threadEMCollector.join()
            threadPacketSniffer.join()

            events["pcktSnifferReady"].clear()
            events["emCollectorReady"].clear()
            events["pcktSendingStarted"].clear()
            events["pcktSendingCompleted"].clear()

simulation()
