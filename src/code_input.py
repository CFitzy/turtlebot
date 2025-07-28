# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 14:15:39 2025
Create place for user to input text code with syntax highlighting
@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk
import idlelib.colorizer as ic
import idlelib.percolator as ip
from tkinter import scrolledtext


class Code_Input():
    def __init__(self, root, clear_text):
        self.code_frame= ctk.CTkFrame(root, fg_color="transparent")
        self.code_frame.pack(side=ctk.LEFT, fill=ctk.Y)
        
        #ctk.CTkLabel(master=self.code_frame, text="Enter code:").pack(side=ctk.TOP)  
        # Text input (size by line not pixel)
        self.textbox = scrolledtext.ScrolledText(master=self.code_frame, font=("Helivetica, 14"), yscrollcommand=True, undo=True)
        self.set_code("turtle.down()\nturtle.forward(20)\nturtle.right(90)\nturtle.up()\nturtle.forward(20)")
        #self.textbox.pack(side=ctk.TOP, pady=5, expand=True, fill=ctk.BOTH)    
        self.textbox.place(x=0, y=0, relwidth=1, relheight=1)
        
        
        ctk.CTkButton(self.textbox, 
                      text="Clear Program", 
                      command=clear_text, 
                      text_color="black", 
                      fg_color="#DDDDDD",
                      bg_color="white",
                      hover_color="#BBBBBB",
                      width=20
                      ).place(relx=0.99, y=2, x=0, anchor="ne")

        
        #checks every second
        cdg = ic.ColorDelegator()
        #might be better have slightly brighter colours
        cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
        #e.g. def, class
        cdg.tagdefs['KEYWORD'] = {'foreground': 'purple', 'background': '#FFFFFF'}
        #e.g. print
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        #FUNCTION definition
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

        #not supported by ctk.CtkTextbox so switched to tk.Text
        ip.Percolator(self.textbox).insertfilter(cdg)
        
    def get_code(self):
        return self.textbox.get("0.0", tk.END)
    
    def set_code(self, new):
        self.clear()
        self.textbox.insert(tk.INSERT, new)
    
    def change_textsize(self, size):
        self.textbox.configure(font=("Helvetica, "+str(size)))
        
    
    def clear(self):
        self.textbox.delete("0.0", tk.END)
        
    #resize code elements to meet new window size requirements
    def resize(self, new_width, new_height):
        self.code_frame.configure(width=new_width, height=new_height)
        self.textbox.configure(width=new_width, height=new_height)
        
        