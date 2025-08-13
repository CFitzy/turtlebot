# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 14:15:39 2025
Creates place for user to input text code with syntax highlighting
@author: cmf6
"""
from customtkinter import CTkFrame
from customtkinter import CTkButton
from customtkinter import LEFT
from customtkinter import Y
from tkinter import scrolledtext
from tkinter import END
from tkinter import INSERT
from idlelib.colorizer import ColorDelegator
from idlelib.percolator import Percolator



class Code_Input():
    def __init__(self, root, clear_text):
        #Make a frame to place textbox and button within
        self.code_frame= CTkFrame(root, fg_color="transparent")
        self.code_frame.pack(side=LEFT, fill=Y)
        
          
        #Make text input as a scrollable textbox which can have actions undone
        self.textbox = scrolledtext.ScrolledText(master=self.code_frame, font=("Helivetica, 14"), yscrollcommand=True, undo=True)
        self.textbox.place(x=0, y=0, relwidth=1, relheight=1)
        #Set default code
        self.set_code("turtle.down()\nturtle.forward(20)\nturtle.right(90)\nturtle.up()\nturtle.forward(20)") 
        
        #Make clear program button to remove textbox contents        
        CTkButton(self.textbox, 
                      text="Clear Program", 
                      command=clear_text, 
                      text_color="black", 
                      fg_color="#DDDDDD",
                      bg_color="white",
                      hover_color="#BBBBBB",
                      width=20
                      ).place(relx=0.99, y=2, x=0, anchor="ne")

        #SYNTAX HIGHLIGHTING (Checks every second)
        cdg = ColorDelegator()
        #Define colours for tags. Done for comments, keywords (i.e def, class etc), bultin in functions (e.g. print), strings and funciton definitions
        cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
        cdg.tagdefs['KEYWORD'] = {'foreground': 'purple', 'background': '#FFFFFF'}
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

        #Apply filter to textbox
        Percolator(self.textbox).insertfilter(cdg)
        
    #Return the code currently in the textbox
    def get_code(self):
        return self.textbox.get("0.0", END)
    
    #Clear and set the new code (for loading in a file)
    def set_code(self, new):
        self.clear()
        self.textbox.insert(INSERT, new)
        
    #Insert a chunk of code at current position
    def insert_code(self, new):
        self.textbox.insert(INSERT, "\n"+new)
    
    #Change the textsize of the textbox
    def change_textsize(self, size):
        self.textbox.configure(font=("Helvetica, "+str(size)))
        
    #Clear (delete) the contents of the textbox
    def clear(self):
        self.textbox.delete("0.0", END)
        
    #Resize code input elements to meet new window size requirements
    def resize(self, new_width, new_height):
        self.code_frame.configure(width=new_width, height=new_height)
        self.textbox.configure(width=new_width, height=new_height)
        
        