# -*- coding: utf-8 -*-
"""
Created on Thu May 29 13:36:54 2025
Makes UI screen so can type in python, press button to run (display on console) and display error messages on app
(Can handle multiple lines of code)
@author: cathr
"""
import customtkinter as ctk

"""Subprocess seems to do but not clear where to (console and UI)
    Tried for its call, run and Popen
- can do checkoutput and print to get "b'hello world\r\n'
    Seems to be more for running command line stuff etc"""
#import subprocess
#subprocess.call('python hello_world.py')
#out = subprocess.check_output('python hello_world.py')
#print(out)

"""os system executes the command visibly Errors in file give a traceback and nameerror , or no such file: file keeps running after
    Doesn't seem to like doing it in this file, fine in one without tkinter"""
#import os 
#os.system('python hello_world.py')

"""read and exec executes the command to console Errors are major and stop execution, not in UI though
    Easiest to go for (and works with UI). Could just do on own without having to save file or with file saving depending when saving required"""
#with open("hello_world.py") as f:
#  exec(f.read())

class Main():
    def __init__(self):
        ctk.set_appearance_mode("light")
        # make window
        root = ctk.CTk()
        # specify window size
        root.geometry("800x600")
        
        ctk.CTkLabel(master=root, text="Enter code:").pack()  
        # Text input 
        self.textbox = ctk.CTkTextbox(master=root, width=500, height = 100)
        self.textbox.pack(pady=5)         

        ctk.CTkButton(root, text="Save/Run", command=self.save_text).pack()
        #shows output rrors on label
        self.textbox2 = ctk.CTkLabel(master=root, text="Error Output here", width=500, height = 100)
        self.textbox2.pack(pady=5)   
        
        #start window
        root.mainloop()
        
    

    def save_text(self):
        #write textbox contents to file
        with open("hello_world.py", "w") as f:
          f.write(self.textbox.get("0.0", "end"))
          f.close()
        
        #try read and execute, display errors on label
        try:
            with open("hello_world.py", "r") as f:
                exec(f.read())
                f.close()
            
        except Exception as e:
            self.textbox2.configure(text=e)
          
        #exec(self.textbox.get("0.0", "end"))   #Just works on it's own
        
        
          
if __name__=="__main__":
    Main()