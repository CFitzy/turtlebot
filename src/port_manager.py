# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:44:36 2025

@author: cmf6
"""


import serial.tools.list_ports
import serial
import time
import threading

class port_manager():
    def __init__(self, connection_states):
        self.connection_states = connection_states
        self.setup =False
        self.usb_connection = False
        self.allow_writing = False
        self.up =0.5
        self.down = 0.3
        self.port = None
        self.connection_states.update_states(self.usb_connection, self.allow_writing)
        self.read = threading.Thread(target= self.open_port)
        self.read.start()
        
    def change_port(self):
        self.allow_writing = False
        self.connection_states.update_states(self.usb_connection, self.allow_writing)
        if not self.port == None:
            self.port.close()
        
        ports = list(serial.tools.list_ports.comports())
        print("ports: ", ports, "\n")

        if len(ports)>0:
            print("open port ", ports[0].name)       #For debugging
            self.port = serial.Serial(ports[0].name, baudrate=115200)
            self.setup =False
            self.usb_connection =True
            self.connection_states.update_states(self.usb_connection, self.allow_writing)
            return True
        else:
            self.usb_connection =False
            self.connection_states.update_states(self.usb_connection, self.allow_writing)
            self.change_port()
            
    #list and open first port
    def open_port(self):
        ports = list(serial.tools.list_ports.comports())
        print("ports: ", ports, "\n")

        if len(ports)>0:
            print("open port ", ports[0].name)       #For debugging
            self.port = serial.Serial(ports[0].name, baudrate=115200)
            self.usb_connection =True
            self.connection_states.update_states(self.usb_connection, self.allow_writing)
            self.setup = False
            self.read_port()
        else:
            self.change_port()
        
    def read_port(self):
        in_str =""
        i =0
        #non blocking read
        while (self.usb_connection):
            #print(i)
            i+=1
            #probe to turtle if setup until acknowledged
            if(self.setup and not self.allow_writing):
                #first = False
                print("Hello")
                self.port.write("=Hello\n".encode('utf-8'))
                
                
            try:# Check if incoming bytes are waiting to be read from the serial input buffer.
                if (self.port.in_waiting > 0):
                    # read the bytes and convert from binary array to ASCII
                    data_str = self.port.read(self.port.in_waiting) 
                    #decode into ascii
                    in_str = str(data_str, 'utf-8')
                    print(in_str)

                    if "AT" == in_str:
                        #encode into bytes (won't compile to send otherwise)
                        out = ('OKPC').encode('utf-8')
                        print("outgoing: ", out)
                        print(self.port.write(out))
                        self.setup=True
                        self.allow_writing = False
                        in_str = ""
                    
                    if "=Hello ACK" in in_str:
                        self.allow_writing = True
                        self.connection_states.update_states(self.usb_connection, self.allow_writing)
            except:
                
                self.usb_connection = False
                print("port disconnected")
                self.change_port()
                    
            time.sleep(1)

    
            
    def close_port(self):
        if not self.port == None:
            self.port.close()
            print("port closed")
                    
            
                     
    #send commmands to turtlebot
    def send_command(self, command):
        if self.allow_writing:
            command=command+"\n"
            out = command.encode("utf-8")
            print("outgoing: ", out)
            self.port.write(out)
        





if __name__=="__main__":
    port_manager()