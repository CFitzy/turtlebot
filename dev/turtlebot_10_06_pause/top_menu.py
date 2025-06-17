# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025

@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk

class Top_Menu():
    def __init__(self, root, clear_text):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.top_bar_frame= ctk.CTkFrame(root)
        self.top_bar_frame.pack(side=ctk.TOP, fill=ctk.X)
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="Settings", 
                      text_color="black", 
                      fg_color="transparent",
                      hover_color="#BBBBBB"
                      ).pack(side=ctk.RIGHT)
        
        ctk.CTkButton(self.top_bar_frame, 
                      text="Clear Program", 
                      command=clear_text, 
                      text_color="black", 
                      fg_color="transparent",
                      hover_color="#BBBBBB"
                      ).pack(side=ctk.RIGHT)
        