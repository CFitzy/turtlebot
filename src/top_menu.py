# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025
Create top menu buttons and handle insert, font size, pen and port selection functions
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
    #Create the top menu and define additional variables
    def __init__(self, root, port_manager, top_bar_frame, connection_frame, change_textsize, set_text, get_text, insert_text):
        #Create a File_Handler instance for reading and writing files (give functions to interact with the code textbox)
        file_handler = File_Handler(get_text, set_text, insert_text)
        #Save variable containing port manager instance
        self.port_manager = port_manager
        #Initial pen down value
        self.down=0.3
        #Create setup wizard instance
        setup_wizard = Setup_Wizard(port_manager)
        
        #Create top_menu
        root.option_add('*tearOff', False) # gets rid of ---- at start of menus
        
        #FILE
        #Create the file top menu button
        file_button = self.make_top_menu_button(top_bar_frame, "File")
        #Create the file menu
        file_button.menu = Menu(file_button, font=("12"))
        file_button["menu"] = file_button.menu
        #Add the Save and Load command options
        file_button.menu.add_command(label="Save", command=lambda: file_handler.save())
        file_button.menu.add_command(label="Load", command=lambda: file_handler.load())
        
        #INSERT
        #Create the insert top menu button
        insert_button = self.make_top_menu_button(top_bar_frame, "Insert")
        #Create the insert menu
        insert_button.menu = Menu(insert_button, font=("12"))
        insert_button["menu"] = insert_button.menu
        #Insert a command for each given type
        insert_types = ["numbers", "letters", "shapes"]
        #For each type
        for it in insert_types:
            #Make it a menu
            menu_insert = Menu(insert_button)
            #Put that menu into a cascade of the same name (with the first letter capitalised)
            insert_button.menu.add_cascade(menu=menu_insert, label=it[0].capitalize()+it[1:])
            #Get the available options of that type
            inserts = file_handler.get_available_inserts(it)
            #For each option, add it to the submenu
            for i in inserts:
                menu_insert.add_command(label=str(i), command= lambda i=i, it=it: file_handler.load_insert_text(i, it))
        
        #SETTINGS
        #Create the settings top menu button
        settings_button  = self.make_top_menu_button(top_bar_frame, "Settings")
        #Create the settings menu and buttons to select a port, open the setup wizard, pick the pen height, and pick the text size
        settings_button.menu = Menu(settings_button, font=("12"))
        settings_button["menu"] = settings_button.menu
        #Add option of Select port to the settings menu to open a pop up to change the port for the turtlebot
        settings_button.menu.add_command(label="Select port", command=self.make_connection_dropdown)
        #Add option of Setup wizard to the settings menu to open a pop up to change the turtlebot's EEPROM settings
        settings_button.menu.add_command(label="Setup wizard", command=setup_wizard.setup_wizard)
        #Add option of Pen height to the settings menu to open a pop up to change the turtlebot's pen height
        settings_button.menu.add_command(label="Pen height", command=self.set_pen_view)
        
        #FONT SIZE
        #Menu to list font size options
        menu_font = Menu(settings_button)
        #Create Font size option within Settings button
        settings_button.menu.add_cascade(menu=menu_font, label='Font size')
        #Code text/Output text font sizes
        fonts = [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36]
        #Make cascade of radio button options for code text and output text size to be changed
        for i in fonts:
            menu_font.add_radiobutton(label=str(i)+" px", command=lambda i=i: change_textsize(i))
        #Set current text size to fifth option(14)
        menu_font.invoke(5)
        
        #Create information/about page button to access the page
        Info_Page(top_bar_frame)
            
        connection_frame.pack(side=RIGHT, padx=1)
        
        #Display the current connected port. Show "No port" by default and replace with port name if one exists
        self.port_label = CTkLabel(top_bar_frame, text="No port", text_color="#007D02", fg_color="white", width =100, height=20)
        if port_manager.port:
            self.port_label.configure(text=port_manager.port.name)

        self.port_label.pack(side=RIGHT, padx=3)
        
    #Create a button for the top menu with given text (for File, Settings and Insert)
    def make_top_menu_button(self, top_bar_frame, text):
        #Create a menu button 
        button = Menubutton(top_bar_frame, text=text, 
                                    background="#007D02", 
                                    activebackground="#229F24", 
                                    font=("Roboto, 14"), 
                                    foreground="#FFFFFF",
                                    activeforeground="#FFFFFF",
                                    border=0
                                    )
        #If using macOS (platform darwin), make the text green as it displays the buttons with a white background (even when not set here)
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