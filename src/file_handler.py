# -*- coding: utf-8 -*-
"""
Created on Wed Jun 25 16:23:46 2025
Handle file-related functions to load from and save to files
@author: cmf6
"""
from customtkinter import filedialog
from glob import glob
from re import search


class File_Handler():
    # Initialise class with access to methods to put code into/retrieve from the code box
    def __init__(self, get_text, set_text, insert_text):
        self.set_text = set_text
        self.get_text = get_text
        self.insert_text  = insert_text
        
    #Load a code file and put the contents inside the code box
    def load(self):
        #Pick a file via opening a dialogue
        try:
            filename = filedialog.askopenfilename(initialdir="/",
                                                 title = "Select file",
                                                 filetypes = [("Text files",
                                                               "*.txt"),
                                                              ("All files",
                                                               "*.*")])
            #Get text from file
            with open(filename) as file:
                contents = file.read()
                #Put contents inside the code box
                self.set_text(contents)
        
        except:
            print("error loading file")
        
    #Save the code in the code box into a file    
    def save(self):
        try:
            #Pick filename 
            file = filedialog.asksaveasfile(initialfile= "Untitled.txt", 
                                               defaultextension=".txt", 
                                               filetypes=[("All Files","*.*"),("Text Documents","*.txt")]
                                               )
            #Save to file
            with open(file.name, "w") as outfile:
                outfile.write(self.get_text())
        except:
            print("error saving file")
            
    #Shape/Insert types = ["numbers", "letters", "shapes"]
            
    #Get all available filenames within the given insert folder
    def get_available_inserts(self, shape_type):
        path = "./characters/"+shape_type+"/*.txt"
        #Get all the filepaths in the folder
        file_paths = glob(path)
        #Get all the filenames 
        filenames = []
        for f in file_paths:
            #Put * into a match object
            filename= search("./characters/"+shape_type+"\\\\(.*).txt", f)
            #Retrieve from match object and place just name into filenames list
            filenames.append(filename.group(1))
        return filenames
      
    #Load a code file based on folder name and filename, and insert the text into the code box
    def load_insert_text(self, value, folder):
        try:
            path = "./characters/"+folder+"/"+str(value)+".txt"   
            #Read from file
            with open(path, "r") as infile:
                contents=infile.read()
            #Insert file contents into the code box
            self.insert_text(contents)
        
        except:
            print("error loading file")
