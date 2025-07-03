# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 13:44:06 2025

@author: cmf6
"""
import tkinter as tk
from tkhtmlview import HTMLScrolledText
from tkhtmlview import RenderHTML
import webview
class Main():
    def __init__(self):
        root= tk.Tk()
        root.title("HTML window")
        root.geometry("800x600")
        
        
        my_label = HTMLScrolledText(root, html=RenderHTML('hello.html'), state="disabled")
        my_label.pack(fill="both", expand=True)
        
        # Open website - crashes if try to go to original app
        #webview.create_window('Turtlebot Info', 'hello.html')
        #webview.start()


        #frame = HtmlFrame(root) #create HTML browser

        #frame.load_website("hello.html") #load a website
        #frame.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window

        
        root.mainloop()
        
        
if __name__=="__main__":
    Main()
    