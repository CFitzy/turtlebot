# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:44:36 2025

@author: cmf6
"""


import serial.tools.list_ports
import serial
import time

class port_handler():
    def __init__(self):
        self.setup =False
        self.open_port()
        


    #list and open first port
    def open_port(self):
        first=False
        allow_next =False
        allow_writing = False
        ports = list(serial.tools.list_ports.comports())
        print("ports: ", ports, "\n")

        print("open port ", ports[0].name)       #For debugging
        
        self.port = serial.Serial(ports[0].name, baudrate=115200)
        in_str =""
        i =0
        #non blocking read
        while (True):
            print(i)
            i+=1
            #probe to turtle if setup until acknowledged
            if(self.setup and not allow_writing):
                #first = False
                print("Hello")
                self.port.write("=Hello\n".encode('utf-8'))
                
            if (allow_writing):
                self.allow_write()
                
            # Check if incoming bytes are waiting to be read from the serial input buffer.
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
                    first = True
                    in_str = ""
                    
                if "=Hello ACK" in in_str:
                    allow_writing = True
                    
                    
                    
    
        # Optional, but recommended: sleep 10 ms (0.01 sec) once per loop to let 
        # other threads on your PC run during this time. 
            time.sleep(1)
            
    def allow_write(self):
        while (True):
            self.send_command(input())
        
    #send commmands to turtlebot
    def send_command(self, command):
        command=command+"\n"
        out = command.encode("utf-8")
        print("outgoing: ", out)
        self.port.write(out)
        





if __name__=="__main__":
    port_handler()