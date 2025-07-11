# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:06:05 2025

@author: cmf6
"""
import tkinter as tk
import customtkinter as ctk

class setup_wizard():
    def __init__(self, port_manager):
        self.circle_steps = 4096
        self.port_manager = port_manager
        
    def setup_wizard(self):
        #get saved values
        #self.port_manager.get
        
        
        
        
        self.wizard_pop_up = ctk.CTkToplevel()
        self.wizard_pop_up.grab_set()           # Stop other window interaction
        self.wizard_pop_up.focus_force()        # Set input focus to the popup
        self.wizard_pop_up.lift()               #make sure pop up is above other window
        self.wizard_pop_up.geometry("500x500")
        
        self.frame = ctk.CTkFrame(self.wizard_pop_up, fg_color="transparent")
        self.frame.pack()
        ctk.CTkLabel(self.frame, text="Setup turtlebot dimensions").pack(pady=1)
        ctk.CTkLabel(self.frame, text="You will need: \n*A ruler").pack(pady=10)
        
        ctk.CTkButton(self.frame, text="Start", command=self.check_wheel_diameter_start).pack(side=ctk.BOTTOM)
        
    def check_wheel_diameter_start(self):
        for w in self.frame.winfo_children():
            w.destroy()
            
        ctk.CTkLabel(self.frame, text="Setup turtlebot wheels").pack(pady=1)
        ctk.CTkLabel(self.frame, text="Press start for the turtlebot to draw a line").pack(pady=10)
        
        ctk.CTkButton(self.frame, text="Start", command=self.check_wheel_diameter_main).pack(side=ctk.BOTTOM)
        
    def check_wheel_diameter_main(self):
        for w in self.frame.winfo_children():
            w.destroy()
            
        self.port_manager.send_command("D")
        self.port_manager.send_command("f4096")
        self.port_manager.send_command("U")
        #self.port_manager.send_command("F10")
        self.port_manager.send_command("o")
            
        ctk.CTkLabel(self.frame, text="Setup turtlebot wheels").pack(pady=1)
        ctk.CTkLabel(self.frame, text="Press start for the turtlebot to draw a line").pack(pady=10)
        
        ctk.CTkButton(self.frame, text="Start").pack(side=ctk.BOTTOM)
        
    