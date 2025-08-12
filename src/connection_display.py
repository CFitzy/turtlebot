# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:01:29 2025
Shows whether the USB dongle and the turtlebot are currently connected
@author: cmf6
"""
from customtkinter import CTkFrame
from customtkinter import CTkLabel
from customtkinter import LEFT

class Connection_Display():
    #define colours
    def __init__(self):
        self.red = "red"
        self.red_bg = "#DD0000"
        self.green = "#00FF14"
        self.green_bg = "#00DD00"

    #Make layout with label, colour, label, colour to show connection states
    def make_connection_layout(self, top_bar_frame):
        #Frame to put layout in
        self.connection_frame = CTkFrame(top_bar_frame, fg_color="transparent")
        #USB dngle port connection
        CTkLabel(self.connection_frame, text="USB", text_color="white").pack(side=LEFT)
        self.usb_connection = CTkLabel(self.connection_frame, text="", fg_color=self.red, bg_color=self.red_bg, width=20, height=20)
        self.usb_connection.pack(side=LEFT, padx=3)
        #Turtlebot connection
        CTkLabel(self.connection_frame, text="Turtle", text_color="white").pack(side=LEFT)
        self.turtle_connection = CTkLabel(self.connection_frame, text="", fg_color=self.red, bg_color=self.red_bg, width=20, height=20)
        self.turtle_connection.pack(side=LEFT, padx=3)
        #return to pack in topbar
        return self.connection_frame
        
    #Update the colours if required (will function but will throw warning as operates with a thread which tkinter is not designed to do)
    def update_states(self, usb_connection, allow_writing):
        #based on state change to green or red
        if usb_connection:
            self.usb_connection.configure(fg_color=self.green, bg_color=self.green_bg)
        else:
            self.usb_connection.configure(fg_color=self.red, bg_color=self.red_bg)
                
        if allow_writing:
            self.turtle_connection.configure(fg_color=self.green, bg_color=self.green_bg)
        else:
            self.turtle_connection.configure(fg_color=self.red, bg_color=self.red_bg)
            