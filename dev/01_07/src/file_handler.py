# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:23:46 2025

@author: cmf6
"""

import customtkinter as ctk
import tkinter as tk


class File_Handler():
    def __init__(self, get_text, set_text):
        self.set_text = set_text
        self.get_text = get_text
        
    #load a code file
    def load(self):
        #pick file
        print("load")
        
        try:
        
            filename = ctk.filedialog.askopenfilename(initialdir="/",
                                                 title = "Select file",
                                                 filetypes = (("Text files",
                                                               "*.txt*"),
                                                              ("all files",
                                                               "*.*")))
            print(filename)
        
            #get text from file
            file = open(filename)

            contents = file.read()
            print("contents: ",contents)
        
            #set to set_text
            self.set_text(contents)
        
            file.close()
        except:
            print("error loading file")
        
    def save(self):
        try:
            print("save")
            #pick filename 
            file = tk.filedialog.asksaveasfile(initialfile= "Untitled.txt", 
                                               defaultextension=".txt", 
                                               filetypes=[("All Files","*.*"),("Text Documents","*.txt")]
                                               )
            print(file.name)

            #save to file
            with open(file.name, "w") as outfile:
                outfile.write(self.get_text())
        except:
            print("error saving file")
