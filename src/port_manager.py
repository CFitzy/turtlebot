# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 13:44:36 2025
Manage port access and sending commands to them
For connecting to the USB dongle port and the turtlebot via it
@author: cmf6
"""
from serial.tools.list_ports import comports
from serial import Serial
from time import sleep
from threading import Thread

class Port_Manager():
    def __init__(self, connection_states):
        #Save given instance of Connection_Display in order to display it
        self.connection_states = connection_states
        #Whether port setup is being done
        self.setup_state =False
        #Whether the USB dongle and turtlebot are connected
        self.usb_connection = False
        self.turtle_connection = False
        #Current port
        self.port = None
        #Number of commands awaiting acknowledgement
        self.awaiting_ack = 0
        #Number of commands the buffer can take at a time
        self.buffer_number = 10
        #Current values saved to the EEPROM
        self.saved_settings = None
        #Whether waiting to acquire settings
        self.awaiting_settings = False
        
    #Open a port    
    def open_port(self, port_name):
        #If name does not start with COM apend /dev/ path (aka if not running on a Windows system)
        if not port_name[:3] == "COM":
            port_name = "/dev/"+port_name
        
        #Close current port and update states and display to match
        self.close_port()
        self.turtle_connection = False
        self.connection_states.update_states(self.usb_connection, self.turtle_connection)

        #Open the port
        self.port = Serial(port_name, baudrate=115200)
        
        #Update setup state as new connection that needs setting up
        self.setup_state =False
        #Update current states and display to show that the port has been opened
        self.usb_connection =True
        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
        #Start reading from the port
        Thread(target= self.read_port).start()
            
    #Get the names of the available ports and return as list
    def get_port_names(self):
        port_names = []
        #For each port in the available ports
        for p in list(comports()):
            #Append its name to the names list
            port_names.append(p.name)
        return port_names
        
        
    #Establish connection with turtle and read from it   
    def read_port(self):
        #Whilst the USB connection is open
        while (self.usb_connection):
            #Probe to turtle if in setup state and no connection to ituntil acknowledged
            if(self.setup_state and not self.turtle_connection):
                self.port.write("=Hello\n".encode('utf-8'))
                self.awaiting_ack=self.awaiting_ack+1

            #Try reading from the turtle
            try:
                #Check if there are incoming bytes waiting to be read
                if (self.port.in_waiting > 0):
                    #Read the bytes
                    data_str = self.port.read(self.port.in_waiting) 
                    #Decode into ascii
                    in_str = str(data_str, 'utf-8')
                    print(in_str)
                    
                    #If AT received, send an OKPC message to establish connection
                    if "AT" == in_str:
                        #Encode into bytes (won't compile to send otherwise)
                        out = ('OKPC').encode('utf-8')
                        print("Out: ", out)
                        #Put into mid-setup state to send message
                        self.setup_state=True
                        
                    #If acknowledging initial Hello, set turtle connection to true and pdate display
                    elif "=Hello ACK" in in_str:
                        self.turtle_connection = True
                        self.connection_states.update_states(self.usb_connection, self.turtle_connection)
                        
                    #Waiting for settings and response contains expected wheel characters
                    elif self.awaiting_settings and "wheel" in in_str:
                        #Put input into saved settings and set acquired to true
                        self.saved_settings = in_str
                        self.awaiting_settings = False
                        
                        
                    #If acknowledgemnt received, reduce number of ones being waited for by one
                    if "ACK" in in_str:        
                        self.awaiting_ack=self.awaiting_ack-1
                        #Check for negative acknowledgement (for when turtlebot commands encounter an unexpected command)
                        if "NACK" in in_str:
                            raise Exception("Turtlebot command failed to execute")
            #If exception is thrown            
            except:
                #Close port
                self.close_port()
                #Update display
                self.usb_connection = False
                self.turtle_connection = False
                self.connection_states.update_states(self.usb_connection, self.turtle_connection)
            #Wait a second before looping/reading again
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
            self.awaiting_ack = self.awaiting_ack+1
            #Encode and send command
            self.write_to_turtle(command)
            #Wait until buffer has enough space for another command
            while self.awaiting_ack>self.buffer_number:
                print("waiting")
                sleep(0.01)
            
            
    #Get turtlebot settings from EEPROM    
    def get_settings(self):
        #Set to waiting for settings
        self.awaiting_settings = True
        #Encode and send get command
        self.write_to_turtle("get")
        #Wait until settings sent back
        while self.awaiting_settings:
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