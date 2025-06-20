# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025

@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk


class Top_Menu():
    def __init__(self, root, port_manager):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.top_bar_frame= ctk.CTkFrame(root, fg_color="#007D02", corner_radius=0) #10B135
        self.top_bar_frame.pack(side=ctk.TOP, fill=ctk.X)
        self.port_manager = port_manager
        self.up = 0.35
        self.down=0.3
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="File", 
                      text_color="white", 
                      fg_color="transparent",
                      hover_color="#BBBBBB",
                      width=40,
                      #command=
                      ).pack(side=ctk.LEFT, pady=2)
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="Settings", 
                      text_color="white", 
                      fg_color="transparent",
                      hover_color="#BBBBBB",
                      width=40,
                      command=self.set_pen_view
                      ).pack(side=ctk.LEFT, pady=2)
        
        
    def set_pen_view(self):
        self.pop_up = ctk.CTkToplevel()
        self.pop_up.focus_force()
        self.pop_up.grab_set()           # Stop other window interaction
        self.pop_up.focus_force()        # Set input focus to the popup
        self.pop_up.lift()               #make sure pop up is above other window
        
        self.down_view()
        
    def down_view(self):
        down_frame = ctk.CTkFrame(self.pop_up)
        down_frame.pack()
        down_label = ctk.CTkLabel(down_frame, text="Adjust pen height until it is just on the paper")
        down_label.pack(padx=5, pady=5)
        down_slider = ctk.CTkSlider(down_frame, from_=0, to=1, command=self.down_slider_event, number_of_steps=20)
        down_slider.pack(pady=5)
        down_slider.set(self.down)
        self.down_slider_event(self.down)
        next_button = ctk.CTkButton(down_frame, text="Save", command=self.save)
        next_button.pack(pady=5)
        

    def down_slider_event(self, value):
        print(value)
        #value=value/ranger
        value = round(value, 2)
        string_value = str(value)
        if value<=0.8:
            setup_value = round(value+0.2, 2)
            self.port_manager.send_command("D"+str(setup_value))
            self.up= setup_value
        else:                                                           #very unlikely to occur as would mean ground is taller than wheels
            setup_value = round(value-0.2, 2)
            self.port_manager.send_command("D"+str(setup_value))
            self.up= 1
        self.port_manager.send_command("D"+string_value)
        self.port_manager.send_command("o")
        self.down=value
        
    def save(self):
        self.port_manager.up = self.up
        self.port_manager.down = self.down
        self.port_manager.send_command("U"+str(self.up))
        print("save here")
        self.pop_up.destroy()
