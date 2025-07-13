# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:06:05 2025

@author: cmf6
"""
import tkinter as tk
import customtkinter as ctk
import re

class setup_wizard():
    def __init__(self, port_manager):
        self.circle_steps = 4096
        self.port_manager = port_manager
        self.settings = {}
        
    def get_settings(self, settings):
        #'wheelL 53.18\r\nwheelR 53.18\r\nAxle 79.04\r\nPenU  0.40\r\nPenD  0.30\r\nBacklashL 0\r\nBacklashR 0\r\n'
        print(settings)
        split_settings = re.split(r'[ \r\n]+', settings)
        print(split_settings)
        
        #stick all the settings into a dictionary
        for i in range(0, (len(split_settings)-1), 2):
            self.settings[split_settings[i]] = split_settings[i+1]
        print(self.settings)
        
    def setup_wizard(self):
        #get saved values
        self.get_settings(self.port_manager.get_settings())
        
        
        self.wizard_pop_up = ctk.CTkToplevel()
        self.wizard_pop_up.grab_set()           # Stop other window interaction
        self.wizard_pop_up.focus_force()        # Set input focus to the popup
        self.wizard_pop_up.lift()               #make sure pop up is above other window
        self.wizard_pop_up.geometry("500x500")
        
        self.frame = ctk.CTkFrame(self.wizard_pop_up, fg_color="transparent")
        self.frame.pack(expand=True, fill=ctk.BOTH)
        ctk.CTkLabel(self.frame, text="Setup turtlebot dimensions").pack(pady=1)
        
        
        if not self.port_manager.allow_writing:
            ctk.CTkLabel(self.frame, text="Connect the turtlebot before setting it up").pack(pady=10)
            ctk.CTkButton(self.frame, text="Close", command=self.wizard_pop_up.destroy).pack(side=ctk.BOTTOM, pady=3)
        else:
            ctk.CTkLabel(self.frame, text="You will need: \n*A ruler\n*A big piece of paper (A3 or bigger recommended)").pack(pady=10)
            ctk.CTkButton(self.frame, text="Start", command=self.check_backlash_start).pack(side=ctk.BOTTOM, pady=3)
        
    def check_backlash_start(self):
        for w in self.frame.winfo_children():
            w.destroy()
            
        ctk.CTkLabel(self.frame, text="Setup turtlebot: Backlash").pack(pady=1)
        ctk.CTkLabel(self.frame, text="Press start for the turtlebot to draw a line").pack(pady=10)
        
        ctk.CTkButton(self.frame, text="Start", command=self.check_backlash_main).pack(side=ctk.BOTTOM)
        
    def check_backlash_main(self):
        self.current = 0 
        self.increment = 10
        for w in self.frame.winfo_children():
            w.destroy()
            
        self.port_manager.send_command("F-50")
            
        ctk.CTkLabel(self.frame, text="Setup turtlebot: Backlash").pack(pady=1)
        ctk.CTkLabel(self.frame, text="Press forward to move the turtlebot forward, if you see it move press next").pack(pady=10)
        
        self.button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.button_frame.pack(side=ctk.BOTTOM)
        
        ctk.CTkButton(self.button_frame, text="Forward", command=self.backlash_forward).pack(side=ctk.LEFT)
        ctk.CTkButton(self.button_frame, text="Next", command=self.backlash_next_increment).pack(side=ctk.LEFT, pady=3, padx=3)
        self.back_button = ctk.CTkButton(self.button_frame, text="Back", command=self.backlash_last_increment, state=ctk.DISABLED)
        self.back_button.pack(side=ctk.LEFT)
        
        
    def backlash_forward(self):
        self.current = self.current + self.increment
        self.port_manager.send_command("F"+str(self.increment))
        print("F:", self.current, self.increment)
        
    def backlash_last_increment(self):
        print("BB", self.current, self.increment)
        self.increment = self.increment*5
        self.current = self.current + self.increment
        print("AB", self.current, self.increment)
        if self.increment ==10:
            print("destroy")
            self.back_button.configure(state=ctk.DISABLED)
        self.backlash_next_increment()
        
        
        
    def backlash_next_increment(self):
        if self.increment/5<0.01:
            #set backlash
            self.port_manager.send_command("o")
            self.port_manager.send_command("s7 "+str(self.current-self.increment))
            self.port_manager.send_command("s8 "+str(self.current-self.increment))
            self.check_wheel_diameter_start()
        
        else:
            print(self.back_button in self.frame.winfo_children())
            
            self.port_manager.send_command("F-"+str(self.current))
            self.current = self.current - self.increment
            self.increment = self.increment/5
            print("N:", self.current, self.increment)
            
            if self.increment <10:
                self.back_button.configure(state=ctk.NORMAL)
            
        
    
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
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
        self.port_manager.send_command("F300")
        self.port_manager.send_command("U")
        self.port_manager.send_command("o")
            
        ctk.CTkLabel(self.frame, text="Setup turtlebot wheels").pack(pady=1)
        ctk.CTkLabel(self.frame, text="Measure the line").pack(pady=10)
        
        #we assume it will be straight "enough" as the wheels are most likely printed at the same time so have been effected equally
        
        ctk.CTkButton(self.frame, text="300mm").pack(side=ctk.BOTTOM)
        ctk.CTkButton(self.frame, text="Not 300mm").pack(side=ctk.BOTTOM)
        
    