# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 11:26:00 2025

@author: cmf6
"""
from customtkinter import CTkToplevel
from tkinter import Button
from tkinter import LEFT
from tkhtmlview import HTMLScrolledText
from tkhtmlview import RenderHTML

class Info_Page():
    def __init__(self, top_bar_frame):

        button = Button(top_bar_frame, 
                           text="About", 
                           background="#007D02", 
                           activebackground="#229F24", 
                           font=("12"), 
                           foreground="#FFFFFF",
                           activeforeground="#FFFFFF",
                           border=0,
                           command = self.display_page
                           )
        button.pack(side=LEFT, pady=2)
        
    def display_page(self):
        self.pop_up = CTkToplevel()
        #self.pop_up.grab_set()
        self.pop_up.attributes("-topmost", True)
        self.pop_up.focus_force() 
        self.pop_up.title("About the Turtlebot")
        #reset logo image
        self.pop_up.after(200, lambda :self.pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        self.pop_up.geometry("500x500")
        
        html = HTMLScrolledText(self.pop_up, html=RenderHTML('html_info/information_page.html'), state="disabled")
        html.pack(fill="both", expand=True)
        
