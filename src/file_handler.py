# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:23:46 2025

@author: cmf6
"""

import customtkinter as ctk
import tkinter as tk
import glob
import re


class File_Handler():
    def __init__(self, get_text, set_text, insert_text):
        self.set_text = set_text
        self.get_text = get_text
        self.insert_text  = insert_text
        
    #load a code file
    def load(self):
        #pick file
        print("load")
        
        try:
        
            filename = ctk.filedialog.askopenfilename(initialdir="/",
                                                 title = "Select file",
                                                 filetypes = [("Text files",
                                                               "*.txt"),
                                                              ("All files",
                                                               "*.*")])
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
            
            
    
    def get_available_inserts(self, shape_type):
        path = "./characters/"+shape_type+"/*.txt"
        #get all the filepaths in the folder
        file_paths = glob.glob(path)
        filenames = []
        for f in file_paths:
            #put * into a match object
            filename= re.search("./characters/"+shape_type+"\\\\(.*).txt", f)
            #retrieve from match object and place just name into filenames list
            filenames.append(filename.group(1))
        return filenames
            
    #load a code file
    def load_insert_text(self, value, number=False, letter=False, shape=False):
        #pick file
        print("load")
        
        try:
        
            if number:
                folder = "numbers"
            elif letter:
                folder = "letters"
            elif shape:
                folder = "shapes"
                
            path = "./characters/"+folder+"/"+str(value)+".txt"
            print(path)   
            #read from file
            with open(path, "r") as infile:
                contents=infile.read()
            
            print("contents: ",contents)
        
            #set to set_text
            self.insert_text(contents)
        
        except:
            print("error loading file")
