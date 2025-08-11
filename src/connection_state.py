# -*- coding: utf-8 -*-
"""
Created on Wed Jun 18 13:01:29 2025

@author: cmf6
"""
import customtkinter as ctk

class Connection_Show():

    def make_connection_layout(self, top_bar_frame):
        self.connection_frame = ctk.CTkFrame(top_bar_frame, fg_color="transparent")
        ctk.CTkLabel(self.connection_frame, text="USB", text_color="white").pack(side=ctk.LEFT)
        self.usb_connection = ctk.CTkLabel(self.connection_frame, text="", fg_color="red", bg_color="#DD0000", width=20, height=20)
        self.usb_connection.pack(side=ctk.LEFT, padx=3)
        ctk.CTkLabel(self.connection_frame, text="Turtle", text_color="white").pack(side=ctk.LEFT)
        self.turtle_connection = ctk.CTkLabel(self.connection_frame, text="", fg_color="red", bg_color="#DD0000", width=20, height=20)
        self.turtle_connection.pack(side=ctk.LEFT, padx=3)
        return self.connection_frame
        
    def update_states(self, usb_connection, allow_writing):
        if usb_connection:
            self.usb_connection.configure(fg_color="#00FF14", bg_color="#00DD00")
        else:
            self.usb_connection.configure(fg_color="red", bg_color="#DD0000")
                
        if allow_writing:
            self.turtle_connection.configure(fg_color="#00FF14", bg_color="#00DD00")
        else:
            self.turtle_connection.configure(fg_color="red", bg_color="#DD0000")
            