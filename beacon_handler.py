import socket
import struct
from threading import Thread

class BeaconHandler:
    def __init__(self,s,addr):
        print("[*] Becon handler for %s started"%(addr))
        try:
            handle_packet(s)
        except Exception as e:
            raise

    def handle_packet(bot):
        pkt = bot.recv(1024)
        len_headers = len(pkt) - 4
        headers = struct.unpack("<HH",pkt[len_headers:])
        if headers[0] = 1:
            #Has data
            pass
        if headers[0] = 0:
            #Does not have data
            pass
        if headers[1] != 5:
            #Default interval changed
            pass
