# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:01:29 2025

@author: cmf6
"""
import threading 
import time

class Connection_State():
    def __init__(self, port_manager, usb, turtle):
        self.port_manager = port_manager
        self.usb_connection = False
        self.turt_connection= False
        self.usb_label = usb
        self.turt_label = turtle
        self.read = threading.Thread(target= self.check_states)
        self.read.start()
        
    def check_states(self):
        while(True):
            self.usb_connection = self.port_manager.usb_connection
            self.turt_connection = self.port_manager.allow_writing
            if self.port_manager.usb_connection:
                self.usb_label.configure(text_color="green")
            else:
                self.usb_label.configure(text_color="red")
                
            if self.port_manager.allow_writing:
                self.turt_label.configure(text_color="green")
            else:
                self.turt_label.configure(text_color="red")
            time.sleep(1)