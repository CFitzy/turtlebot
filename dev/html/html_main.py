# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 13:44:06 2025

@author: cmf6
"""
import tkinter as tk
from tkhtmlview import HTMLScrolledText
from tkhtmlview import HTMLText
from tkhtmlview import RenderHTML

class Main():
    def __init__(self):
        root= tk.Tk()
        root.title("HTML window")
        root.geometry("800x600")
        
        
        my_label = HTMLScrolledText(root, html=RenderHTML('hello.html'))
        my_label.pack(fill="both", expand=True)
        
        root.mainloop()
        
        
if __name__=="__main__":
    Main()
    