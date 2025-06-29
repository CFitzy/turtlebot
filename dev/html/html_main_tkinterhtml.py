# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 13:44:06 2025

@author: cmf6
"""
import tkinter as tk
from tkhtmlview import HTMLScrolledText
from tkinterhtml import HtmlFrame



class Main():
    def __init__(self):
        root= tk.Tk()
        root.title("HTML window")
        root.geometry("500x600")
        
        #file = open("hello.html")

        #contents = file.read()
        #print("contents: ",contents)
        
        frame = HtmlFrame(root, horizontal_scrollbar="auto")
        frame.set_content("<html><head><title>Turtlebot</title></head><body><h2>Introduction</h2></body></html>")
        #my_label = HTMLScrolledText(root, html=contents, height=600, width=500)
        #my_label.pack(pady=20)
        frame.pack()
        
        root.mainloop()
        
        
if __name__=="__main__":
    Main()
    