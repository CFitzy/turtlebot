# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:44:36 2025

@author: cmf6
"""

from serial.tools.list_ports import comports
from serial import Serial
from time import sleep
from threading import Thread

class Port_Manager():
    def __init__(self, connection_states):
        self.connection_states = connection_states
        self.setup =False
        self.usb_connection = False
        self.turtle_connection = False
        self.port = None
        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
        self.sent = 0
        #number of commands the buffer can take at a time
        self.buffer_number = 10
        #current values saved to the EEPROM
        self.saved_settings = None
        
        
    def set_port(self, port_name):
        #if not first 3 letters
        if not port_name[:3] == "COM":
            port_name = "/dev/"+port_name
        
        #Close current port and update states and display to match
        self.close_port()
        self.turtle_connection = False
        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
        
        self.ports = list(comports())

        print("open port ", port_name)       #For debugging
        self.port = Serial(port_name, baudrate=115200)
        self.setup =False
        self.usb_connection =True
        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
        Thread(target= self.read_port).start()
            
    
    def get_port_names(self):
        port_names = []
        for p in list(comports()):
            port_names.append(p.name)
        
        return port_names
        
        
        
    def read_port(self):
        in_str =""
        self.settings_acquired = True

        #non blocking read
        while (self.usb_connection):
            #probe to turtle if setup until acknowledged
            if(self.setup and not self.turtle_connection):
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
                        self.turtle_connection = False
                        in_str = ""
                    
                    if "=Hello ACK" in in_str:
                        self.turtle_connection = True
                        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
                    if "ACK" in in_str:         #check for NACK
                        self.sent=self.sent-1
                        if "NACK" in in_str:
                            raise Exception("Turtlebot command failed to execute")
                        #print("ACKED", self.sent)
                    if not self.settings_acquired and "wheel" in in_str:
                        in_str = in_str.lstrip(")")
                        
                        #Put input into saved settings and set acquired to true
                        self.saved_settings = in_str
                        self.settings_acquired = True
                        
            except:
                self.usb_connection = False
                self.turtle_connection = False
                self.connection_states.update_states(self.usb_connection, self.turtle_connection)
                print("port disconnected", self.usb_connection)
                self.close_port()
                    
            sleep(1)

    
    #Close the current port       
    def close_port(self):
        #If there is an open port
        if not self.port == None:
            #Close it
            self.port.close()
            self.usb_connection = False
            print("port closed")
                    
                     
    #Send commmand to turtlebot
    def send_command(self, command):
        #If turtlebot is connected
        if self.turtle_connection:
            #Increase number of messages sent
            self.sent = self.sent+1
            #Encode and send command
            self.write_to_turtle(command)
            #Wait until buffer has enough space for another command
            while self.sent>self.buffer_number:
                sleep(0.01)
            
            
    #Get turtlebot settings from EEPROM    
    def get_settings(self):
        #Set to waiting for settings
        self.settings_acquired = False
        #Encode and send get command
        self.write_to_turtle("get")
        #Wait until settings sent back
        while not self.settings_acquired:
            sleep(0.01)
        #Return the settings sent back
        return self.saved_settings
    
    
    #Write given command to port (to get to turtle) after formatting/encoding
    def write_to_turtle(self, command):
        #Encode and send command
        command=command+"\n"
        out = command.encode("utf-8")
        self.port.write(out)
        #Print out for debugging purposes
        print("Out: ", out)