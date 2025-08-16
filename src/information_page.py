# -*- coding: utf-8 -*-
"""
Created on Mon Jun 30 11:26:00 2025
Display the About HTML pages with button to access them
@author: cmf6
"""
from customtkinter import CTkToplevel
from tkinter import Button
from tkinter import LEFT
from tkhtmlview import HTMLScrolledText
from tkhtmlview import RenderHTML

class Info_Page():
    #Create About button to access the information pages
    def __init__(self, top_bar_frame):
        button = Button(top_bar_frame, 
                           text="About", 
                           background="#007D02", 
                           activebackground="#229F24", 
                           font=("Roboto, 14"), 
                           foreground="#FFFFFF",
                           activeforeground="#FFFFFF",
                           border=0,
                           command = self.display_page
                           )
        button.pack(side=LEFT, pady=2)
        
    #Open window containing the About page
    def display_page(self):
        #Make pop up above the main window
        self.pop_up = CTkToplevel()
        self.pop_up.attributes("-topmost", True)
        #Set window title and size
        self.pop_up.title("About the Turtlebot")
        self.pop_up.geometry("500x500")
        #Reset logo image as it is replaced with the default tkinter one otherwise
        self.pop_up.after(200, lambda :self.pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        
        #Put contents of HTML file into a ScrolledText and pack into TopLevel
        html = HTMLScrolledText(self.pop_up, html=RenderHTML('html_info/information_page.html'), state="disabled")
        html.pack(fill="both", expand=True)
        
