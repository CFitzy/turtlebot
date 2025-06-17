# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025

@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk

ranger = 5

class Top_Menu():
    def __init__(self, root, clear_text, port_manager):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.top_bar_frame= ctk.CTkFrame(root)
        self.top_bar_frame.pack(side=ctk.TOP, fill=ctk.X)
        self.port_manager = port_manager
        self.up = 0.35
        self.down=0.3
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="Settings", 
                      text_color="black", 
                      fg_color="transparent",
                      hover_color="#BBBBBB",
                      command=self.set_pen_view
                      ).pack(side=ctk.RIGHT)
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="Clear Program", 
                      command=clear_text, 
                      text_color="black", 
                      fg_color="transparent",
                      hover_color="#BBBBBB"
                      ).pack(side=ctk.RIGHT)
        
    def set_pen_view(self):
        self.pop_up = ctk.CTkToplevel()
        self.pop_up.focus_force()
        self.pop_up.grab_set()           # Stop other window interaction
        self.pop_up.focus_force()        # Set input focus to the popup
        self.pop_up.lift()               #make sure pop up is above other window
        
        self.down_view()
        
    def down_view(self):
        self.destory_in_pop_up()
        down_frame = ctk.CTkFrame(self.pop_up)
        down_frame.pack()
        down_label = ctk.CTkLabel(down_frame, text="Adjust pen height until it is just on the paper")
        down_label.pack(padx=5, pady=5)
        down_slider = ctk.CTkSlider(down_frame, from_=0, to=1, command=self.up_slider_event, number_of_steps=20)
        down_slider.pack(pady=5)
        down_slider.set(self.down)
        self.down_slider_event(self.down)
        next_button = ctk.CTkButton(down_frame, text="Next", command=self.up_view)
        next_button.pack(pady=5)
        
    def up_view(self):
        self.destory_in_pop_up()
        up_frame = ctk.CTkFrame(self.pop_up)
        up_frame.pack()
        up_label = ctk.CTkLabel(up_frame, text="Adjust pen height until it is just off the paper")
        up_label.pack(padx=5, pady=5)
        up_slider = ctk.CTkSlider(up_frame, from_=0, to=1, command=self.up_slider_event, number_of_steps=20)
        up_slider.pack(pady=5)
        up_slider.set(self.up)
        self.up_slider_event(self.up)
        ctk.CTkButton(up_frame, text="Back", command=self.up_view).pack()
        next_button = ctk.CTkButton(up_frame, text="Save", command=self.save)
        next_button.pack(pady=5)
        
    def destory_in_pop_up(self):
        for child in self.pop_up.winfo_children():
            child.destroy()
        
        
        
    def up_slider_event(self, value):
        print(value)
        #value=value/ranger
        string_value = str(round(value, 2))
        self.port_manager.send_command("U"+string_value)
        #self.port_manager.send_command("o")
        self.up=value

    def down_slider_event(self, value):
        print(value)
        #value=value/ranger
        string_value = str(round(value, 2))
        self.port_manager.send_command("D"+string_value)
        #self.port_manager.send_command("o")
        self.down=value
        
    def save(self):
        self.port_manager.send_command("o")
        self.port_manager.up = self.up
        self.port_manager.down = self.down
        print("save here")
        self.pop_up.destroy()
