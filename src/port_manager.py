# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:44:36 2025

@author: cmf6
"""

import serial.tools.list_ports
import serial
import time
import threading

class Port_Manager():
    def __init__(self, connection_states):
        self.connection_states = connection_states
        self.setup =False
        self.usb_connection = False
        self.allow_writing = False
        self.port = None
        self.port_name =None
        self.connection_states.update_states(self.usb_connection, self.allow_writing)
        self.sent = 0
        #number of commands the buffer can take at a time
        self.buffer_number = 10
        #current values saved to the EEPROM
        self.saved_settings = None
        
    def change_port(self):
        self.allow_writing = False
        self.connection_states.update_states(self.usb_connection, self.allow_writing)
        #close current port
        if self.port:
            self.port.close()
        
        self.ports = list(serial.tools.list_ports.comports())

        if not self.port_name == None:
            print("open port ", self.port_name)       #For debugging
            self.port = serial.Serial(self.port_name, baudrate=115200)
            self.setup =False
            self.usb_connection =True
            self.connection_states.update_states(self.usb_connection, self.allow_writing)
            self.port_name =None
            threading.Thread(target= self.read_port).start()
        else:
            self.usb_connection =False
            self.connection_states.update_states(self.usb_connection, self.allow_writing)
            #wait for a second then try again
            time.sleep(1)
        
    def set_port(self, port_name):
        #if first 3 letters
        if port_name[:3] == "COM":
            self.port_name = port_name
            print(port_name[:3])
        else:
            self.port_name = "/dev/"+port_name
        self.usb_connection = False
        print(port_name)
        self.change_port()
            
    
    def get_port_names(self):
        port_names = []
        for p in list(serial.tools.list_ports.comports()):
            port_names.append(p.name)
        
        if not port_names:
            return "No ports", port_names
        else:
            return "Select port", port_names
        
        
        
    def read_port(self):
        in_str =""
        self.settings_acquired = True

        #non blocking read
        while (self.usb_connection):
            #probe to turtle if setup until acknowledged
            if(self.setup and not self.allow_writing):
                print("Hello")
                self.port.write("=Hello\n".encode('utf-8'))
                self.sent=self.sent+1

                
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
                        #print(self.port.write(out))
                        self.setup=True
                        self.allow_writing = False
                        in_str = ""
                    
                    if "=Hello ACK" in in_str:
                        self.allow_writing = True
                        self.connection_states.update_states(self.usb_connection, self.allow_writing)
                    if "ACK" in in_str:         #check for NACK
                        self.sent=self.sent-1
                        #print("ACKED", self.sent)
                    if not self.settings_acquired:
                        in_str = in_str.lstrip(")")
                        
                        
                        
                        self.saved_settings = in_str
                        self.settings_acquired = True
                        
            except:
                
                self.usb_connection = False
                self.allow_writing = False
                self.connection_states.update_states(self.usb_connection, self.allow_writing)
                print("port disconnected", self.usb_connection)
                self.close_port()
                    
            time.sleep(1)

    
            
    def close_port(self):
        if not self.port == None:
            self.port.close()
            self.usb_connection = False
            print("port closed")
                    
            
                     
    #send commmands to turtlebot
    def send_command(self, command):
        if self.allow_writing:
            self.sent = self.sent+1
            command=command+"\n"
            out = command.encode("utf-8")
            print("outgoing: ", out)
            self.port.write(out)
            print(self.sent)
            while self.sent>self.buffer_number:
                #print("waiting")
                time.sleep(0.01)
            print("escape", self.sent)
            
            
    def get_settings(self):
        self.settings_acquired = False
        out = "get\n".encode("utf-8")
        print("outgoing: ", out)
        self.port.write(out)
        
        while not self.settings_acquired:
            time.sleep(0.01)
        return self.saved_settings
        
        