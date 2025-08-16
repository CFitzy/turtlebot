# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025
Create top menu buttons and handle insert, fontsize, pen and port selection functions
@author: cmf6
"""

from customtkinter import CTkToplevel
from customtkinter import CTkSlider
from customtkinter import CTkLabel
from customtkinter import CTkButton
from customtkinter import CTkOptionMenu
from customtkinter import StringVar
from customtkinter import LEFT
from customtkinter import RIGHT
from tkinter import Menu
from tkinter import Menubutton
from file_handler import File_Handler
from information_page import Info_Page
from setup_wizard import Setup_Wizard
from sys import platform


class Top_Menu():
    def __init__(self, root, port_manager, top_bar_frame, connection_frame, change_textsize, set_text, get_text, insert_text):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        
        file_handler = File_Handler(get_text, set_text, insert_text)
        
        self.port_manager = port_manager
        self.down=0.3
        setup_wizard = Setup_Wizard(port_manager)
        root.option_add('*tearOff', False) # gets rid of ---- at start of menus
        file_button = self.make_top_menu_button(top_bar_frame, "File")
        insert_button = self.make_top_menu_button(top_bar_frame, "Insert")
        settings_button  = self.make_top_menu_button(top_bar_frame, "Settings")
        
        
        file_button.menu = Menu(file_button, font=("12"))
        file_button["menu"] = file_button.menu
        
        file_button.menu.add_command(label="Save", command=lambda: file_handler.save())
        file_button.menu.add_command(label="Load", command=lambda: file_handler.load())
        
        
        insert_types = ["numbers", "letters", "shapes"]
        
        insert_button.menu = Menu(insert_button, font=("12"))
        insert_button["menu"] = insert_button.menu
        
        
        for it in insert_types:
            menu_ins = Menu(insert_button)
            insert_button.menu.add_cascade(menu=menu_ins, label=it[0].capitalize()+it[1:])
            inserts = file_handler.get_available_inserts(it)
            for i in inserts:
                menu_ins.add_command(label=str(i), command= lambda i=i, it=it: file_handler.load_insert_text(i, it))
        
        
        #Setttings menu and buttons to select a port, open the setup wizard, pick the pen height, and pick the text size
        settings_button.menu = Menu(settings_button, font=("12"))
        settings_button["menu"] = settings_button.menu
        
        settings_button.menu.add_command(label="Select port", command=self.make_connection_dropdown)
        
        settings_button.menu.add_command(label="Setup wizard", command=setup_wizard.setup_wizard)
        
        settings_button.menu.add_command(label="Pen height", command=self.set_pen_view)
        #settings_button.menu.add_command(label="Font size")
        
        menu_font = Menu(settings_button)
        settings_button.menu.add_cascade(menu=menu_font, label='Font size')
        
        fonts = [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36]
        for i in fonts:
            menu_font.add_radiobutton(label=str(i)+" px", command=lambda i=i: change_textsize(i))
        menu_font.invoke(5)
        
        
        Info_Page(top_bar_frame)
            
        connection_frame.pack(side=RIGHT, padx=1)
        
        #show which port is currently connected to
        self.port_label = CTkLabel(top_bar_frame, text="No port", text_color="#007D02", fg_color="white", width =100, height=20)
        if port_manager.port:
            self.port_label.configure(text=port_manager.port.name)

        self.port_label.pack(side=RIGHT, padx=3)
        
        
    def make_top_menu_button(self, top_bar_frame, text):
        button = Menubutton(top_bar_frame, text=text, 
                                    background="#007D02", 
                                    activebackground="#229F24", 
                                    font=("Roboto, 14"), 
                                    foreground="#FFFFFF",
                                    activeforeground="#FFFFFF",
                                    border=0
                                    )
        #test if macOs? if so make the button text green as will have a white background
        if platform == "darwin":
            button.configure(foreground="#007D02", activeforeground="#007D02", background = "#FFFFFF", activebackground="#FFFFFF")
            
        button.pack(side=LEFT, pady=2)
        return button
    
    
    #CONNECTING TO PORTS
    #Make pop up for the user to pick the port that the USB dongle is connected via to then establish a connection bettween it and the turtlebot
    def make_connection_dropdown(self):
        #Create pop up
        self.connection_pop_up = CTkToplevel()
        self.connection_pop_up.grab_set()           # Stop other window interaction
        self.connection_pop_up.focus_force()        # Set input focus to the popup
        self.connection_pop_up.lift()               #make sure pop up is above other window
        self.connection_pop_up.title("Select a port")
        
        #Stops icon being overwritten by the default (overwrites the overwrite)
        self.connection_pop_up.after(200, lambda :self.connection_pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        
        CTkLabel(self.connection_pop_up, text="Select a port below").pack()
        
        #Create port options drop down
        self.port_menu = CTkOptionMenu(self.connection_pop_up,
                                         command=self.select_port)
        self.port_menu.pack(padx=5, pady=5)
        #Get and set list
        self.refresh_ports_list()
        #Create refresh button
        self.refresh_list_button = CTkButton(self.connection_pop_up, text="Refresh ports", command=self.refresh_ports_list)
        self.refresh_list_button.pack(pady=2)
        
    #Select and open picked port
    def select_port(self, choice):
        #Send picked portname to the port manager to open it
        self.port_manager.set_port(choice)
        #Close port picking pop up
        self.connection_pop_up.destroy()
            
    #Refresh the dropdown options to reflect current connections available
    def refresh_ports_list(self):
        #Get names of available ports
        port_names = self.port_manager.get_port_names()
        #If no ports available say so
        if not port_names:
            port_var = StringVar(value="No ports")
        #Otherwise prompt to pick one
        else:
            port_var = StringVar(value="Select port")
        
        #Add first value to dropdown and the list of port names
        self.port_menu.configure(values=port_names, variable=port_var)

        
    #ADJUSTING PEN HEIGHT
    #Create a pop up to adjust the pen height so a height where the pen just touches the paper underneath can be found
    def set_pen_view(self):
        #Create pop up window
        self.pop_up = CTkToplevel()
        self.pop_up.grab_set()           # Stop other window interaction
        self.pop_up.focus_force()        # Set input focus to the popup
        self.pop_up.lift()               #make sure pop up is above other window
        #Set pop up title
        self.pop_up.title("Set pen height")
        #Stops icon being overwritten by the default
        self.pop_up.after(201, lambda :self.pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        
        #Create pen slider and label to explain
        down_label = CTkLabel(self.pop_up, text="Adjust pen height until it is just on the paper")
        down_label.pack(padx=5, pady=5)
        down_slider = CTkSlider(self.pop_up, from_=0, to=1, command=self.down_slider_event, number_of_steps=100)
        down_slider.pack(pady=5)
        #Set to last saved down position
        down_slider.set(self.down)
        #Move pen down to start position
        self.down_slider_event(self.down)
        #Create save button
        save_button = CTkButton(self.pop_up, text="Save", command=self.save)
        save_button.pack(pady=5)
        
    #Move pen down (or up depending on value)
    def down_slider_event(self, value):
        #Round value to 2D.P. then send to port as down value
        value = round(value, 2)
        self.port_manager.send_command("D"+str(value))
        #Set value to current down
        self.down=value
        
    #Save up pen value and finish
    def save(self):
        #Move pen back up so not touching paper
        self.port_manager.send_command("U"+str(self.down+0.2))
        #Close pop up
        self.pop_up.destroy()