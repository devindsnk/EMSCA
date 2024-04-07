#!/usr/bin/env Python3

import configparser
import os
import time
import threading
import osmosdr
from gnuradio import blocks
from gnuradio import gr
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class EMCollector(gr.top_block):
    def __init__(self) -> None:
        gr.top_block.__init__(self)
        self.readConfig()
        self.setupOsmocomSource()

        if not os.path.isdir(self.outputPath):
            os.mkdir(self.outputPath)

    def readConfig(self) -> None:
        config = configparser.ConfigParser()
        config.read('./config.ini')
        
        emCollectorSWConfig = config['EMCollector.Software']
        self.outputPath = emCollectorSWConfig['outputPath']
        self.startFreq = int(emCollectorSWConfig['startFrequency'])
        self.endFreq = int(emCollectorSWConfig['endFrequency'])
        self.freqMultiplier = float(emCollectorSWConfig['freqencyMultiplier'])
        self.freqStep = int(emCollectorSWConfig['freqencyStep'])

        emCollectorHWConfig = config['EMCollector.Hardware']
        self.rfGain = float(emCollectorHWConfig['rfGain']) 
        self.ifGain = float(emCollectorHWConfig['ifGain'])
        self.bbGain = float(emCollectorHWConfig['bbGain'])
        self.sampleRate = float(emCollectorHWConfig['sampleRate'])
        self.gainControl = bool(emCollectorHWConfig['gainControl'])

    def setupOsmocomSource(self) -> None:
        self.osmosdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )

        self.osmosdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(0, 0)
        self.osmosdr_source_0.set_iq_balance_mode(0, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.osmosdr_source_0.set_sample_rate(self.sampleRate)
        self.osmosdr_source_0.set_gain_mode(self.gainControl, 0)
        self.osmosdr_source_0.set_gain(self.rfGain, 0)
        self.osmosdr_source_0.set_if_gain(self.ifGain, 0)
        self.osmosdr_source_0.set_bb_gain(self.bbGain, 0)

    def getOutputPath(self, pattern, freq) -> str:
        freq = f"{freq}MHz"
        folderName = f"{self.outputPath}/{freq}"

        if not os.path.isdir(folderName):
            os.mkdir(folderName)

        filePath = f"{folderName}/{pattern}_{freq}.iq"
        # print("filePath", filePath)
        open(filePath, "w").close()

        return filePath

    def getFreqs(self) -> range:
        freqs = range(self.startFreq, self.endFreq+1, self.freqStep)
        return freqs

    def initDataCollection(self, pattern : str, freq) -> None:
        filePath = self.getOutputPath(pattern, freq)
        
        self.blocks_file_sink_0 = blocks.file_sink(gr.sizeof_gr_complex * 1, filePath, False)
        self.blocks_file_sink_0.set_unbuffered(False)
        self.osmosdr_source_0.set_center_freq(freq * self.freqMultiplier, 0)

        # print(f"configure center freq : {freq * self.freqMultiplier}")

        self.disconnect_all()
        self.connect((self.osmosdr_source_0, 0), (self.blocks_file_sink_0, 0))
    
    def collectEMData(self, pattern : str, freq : int, events):

        self.initDataCollection(pattern.__name__, freq)

        print(f"\temCollector: HackRF Ready ({freq}Mhz)")
        events["emCollectorReady"].set()

        print("\temCollector: Waiting for pcktSender")
        events["pcktSendingStarted"].wait()
        print("\temCollector: Detected pcktSender started")

        print("\temCollector: EM collecting started...")
        threadHackRF = threading.Thread(target=self.startHackRF)
        threadHackRF.start()

        print("\temCollector: Waiting for packet sending to complete")
        events["pcktSendingCompleted"].wait()
        print("\temCollector: Detected packet sending completed")
        print("\temCollector: EM collecting stopping...")
        self.stopHackRF()
        time.sleep(2)

    def startHackRF(self) -> None:
        print("\temCollector: HackRf data collection started")
        self.run()

    def stopHackRF(self) -> None:
        self.stop()
        time.sleep(3)
        self.blocks_file_sink_0.close()
        print("\temCollector: HackRF data collection stopped")
        
        



        


        
