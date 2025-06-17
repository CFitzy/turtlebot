# -*- coding: utf-8 -*-
"""
Created on Thu May 29 16:21:34 2025
Makes UI screen so can type in python, works like import file but with syntax highlighting
@author: cathr
"""
import customtkinter as ctk
import tkinter as tk
#used as minimally faffy aka half the size (or less) than other options
import idlelib.colorizer as ic
import idlelib.percolator as ip


class Main():
    def __init__(self):
        ctk.set_appearance_mode("light")
        # make window
        root = ctk.CTk()
        # specify window size
        root.geometry("800x600")
        
        ctk.CTkLabel(master=root, text="Enter code:").pack()  
        # Text input (size by line not pixel)
        self.textbox = tk.Text(master=root, width=50, height = 10)
        self.textbox.pack(pady=5)      
        
        # borrowed from https://stackoverflow.com/questions/69102656/pygments-to-highlight-python-syntax-in-textbox-tkinter
        cdg = ic.ColorDelegator()
        #might be better have slightly brighter colours
        cdg.tagdefs['COMMENT'] = {'foreground': '#FF0000', 'background': '#FFFFFF'}
        cdg.tagdefs['KEYWORD'] = {'foreground': 'purple', 'background': '#FFFFFF'}
        cdg.tagdefs['BUILTIN'] = {'foreground': '#7F7F00', 'background': '#FFFFFF'}
        cdg.tagdefs['STRING'] = {'foreground': '#7F3F00', 'background': '#FFFFFF'}
        cdg.tagdefs['DEFINITION'] = {'foreground': '#007F7F', 'background': '#FFFFFF'}

        #not supported by ctk.CtkTextbox so switched to tk.Text
        ip.Percolator(self.textbox).insertfilter(cdg)
        
        
        ctk.CTkButton(root, text="Save/Run", command=self.run_text).pack()
        #shows output errors on label
        self.textbox2 = ctk.CTkLabel(master=root, text="Error Output here", width=500, height = 100)
        self.textbox2.pack(pady=5)  
        
        #start window
        root.mainloop()
        
    

    def run_text(self):
        #try execute, display errors on label
        try:
            exec(self.textbox.get("0.0", "end"))
            
        except Exception as e:
            self.textbox2.configure(text=e)

        
          
if __name__=="__main__":
    Main()