
class PacketSniffer:
    def __init__(self) -> None:
        pass

    def sniffPackets(self):
        pass


    # def sniffPackets(freq, pcap_path, pattern):
    #     print("\tSniffer: Waiting for hackrf")
    #     evt_hackrf_ready.wait()
    #     evt_sniffer_ready.set()
    #     evt_data_collection_started.wait()

    #     print("\tSniffing started...")
    #     pckts = sniff(iface=sniffer_interface, stop_filter=stopfilter2)

    #     evt_stop_data_collection.set()
    #     # stop_tb()

    #     print("\tSniffing stopped...")
    #     wrpcap(f'{pcap_path}/{pattern}_{freq}Mhz_sniffed.pcap', pckts)
    #     print("\tPcap file saved...")
