import socket
from threading import Thread
import struct
from time import sleep

# Global Varibales

ip = "127.0.0.1"
port = 2003
inter = 5 #Interval between each beacon
has_info = 0 # 1--> True, 0 --> False
cmd_output = ""

def process_cmd(cmd):
    pass

def send_beacons(s):
    global ip,port,inter,has_info,cmd_output
    try:
        s.connect((ip,port))
        if has_info == 1:
            beacon_packet = struct.pack("<%dsHH",cmd_output,has_info,inter)
        else:
            beacon_packet = struct.pack("<HH",has_info,inter)
        s.send(beacon_packet)
        #print("[*] Packet : %s"%(str(beacon_packet)))
        resp = s.recv(1024)
        len_meta_data = len(resp) - 4
        data = struct.unpack("<HH",resp[len_meta_data:])
        if data[0] == 1:
            cmd = struct.unpack("<%ds"%(len_meta_data),resp[:len_meta_data])
            process_cmd(cmd)
        elif data[0] == 0:
            pass
        if data[1] != inter:
            inter = data[1]
    except socket.error:
        pass
    except Exception as e:
        print("[*] Error in send_beacons : %s"%(str(e)))
        s.close()
    s.close()
    return

def main():
    global inter
    try:
        while True:
            s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            beacon_thread = Thread(target=send_beacons,args=(s,))
            beacon_thread.start()
            beacon_thread.join()
            #print("[*] Beacon_thread dead")
            sleep(inter)
    except Exception as e:
        print("[*] Error in main : %s"%(str(e)))

if __name__ == '__main__':
    main()
