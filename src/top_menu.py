# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025

@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk
import file_handler as fh
import information_page as ip
import setup_wizard as sw
import sys


class Top_Menu():
    def __init__(self, root, port_manager, top_bar_frame, connection_frame, change_textsize, set_text, get_text, insert_text):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        
        file_handler = fh.File_Handler(get_text, set_text, insert_text)
        
        self.port_manager = port_manager
        self.up = 0.5 #stuck till can reliabily move less
        self.down=0.3
        setup_wizard = sw.setup_wizard(port_manager)
        #menubar = tk.Menu(top_bar_frame)
        root.option_add('*tearOff', False) # gets rid of ---- at start of menus
        file_button = self.make_top_menu_button(top_bar_frame, "File")
        insert_button = self.make_top_menu_button(top_bar_frame, "Insert")
        settings_button  = self.make_top_menu_button(top_bar_frame, "Settings")
        
        
        file_button.menu = tk.Menu(file_button, font=("12"))
        file_button["menu"] = file_button.menu
        
        file_button.menu.add_command(label="Save", command=lambda: file_handler.save())
        file_button.menu.add_command(label="Load", command=lambda: file_handler.load())
        
        
  
        #print(file_handler.get_available_inserts("numbers"))
        insert_button.menu = tk.Menu(insert_button, font=("12"))
        insert_button["menu"] = insert_button.menu
        menu_num = tk.Menu(insert_button)
        insert_button.menu.add_cascade(menu=menu_num, label='Number')
        numbers = file_handler.get_available_inserts("numbers")
        for i in numbers:
            print(i)
            menu_num.add_command(label=str(i), command= lambda i=i: file_handler.load_insert_text(value=i, number=True))
        
        
        #Setttings menu and buttons to select a port, open the setup wizard, pick the pen height, and pick the text size
        settings_button.menu = tk.Menu(settings_button, font=("12"))
        settings_button["menu"] = settings_button.menu
        
        settings_button.menu.add_command(label="Select port", command=self.make_connection_dropdown)
        
        settings_button.menu.add_command(label="Setup wizard", command=setup_wizard.setup_wizard)
        
        settings_button.menu.add_command(label="Pen height", command=self.set_pen_view)
        #settings_button.menu.add_command(label="Font size")
        
        menu_font = tk.Menu(settings_button)
        settings_button.menu.add_cascade(menu=menu_font, label='Font size')
        
        fonts = [8, 10, 11, 12, 14, 16, 18, 20, 24, 28, 32, 36]
        for i in fonts:
            print(i)
            menu_font.add_radiobutton(label=str(i)+" px", command=lambda i=i: change_textsize(i))
        menu_font.invoke(5)
        
        
        ip.Info_Page(top_bar_frame)
            
        #self.refresh_button.pack(side=ctk.LEFT, padx=3)
        connection_frame.pack(side=ctk.RIGHT, padx=1)
        
        #show which port is currently connected to
        self.port_label = ctk.CTkLabel(top_bar_frame, text="No port", text_color="#007D02", fg_color="white", width =100, height=20)
        if port_manager.port:
            self.port_label.configure(text=port_manager.port.name)

        self.port_label.pack(side=ctk.RIGHT, padx=3)
        
        
    def make_top_menu_button(self, top_bar_frame, text):
        button = tk.Menubutton(top_bar_frame, text=text, 
                                    background="#007D02", 
                                    activebackground="#229F24", 
                                    font=("12"), 
                                    foreground="#FFFFFF",
                                    activeforeground="#FFFFFF",
                                    border=0
                                    )
        #test if macOs? if so make the button text green as will have a white background
        if sys.platform == "darwin":
            button.configure(foreground="#007D02", activeforeground="#007D02", background = "#FFFFFF", activebackground="#FFFFFF")
            
        button.pack(side=ctk.LEFT, pady=2)
        return button
    
    
    
    def make_connection_dropdown(self):
        self.connection_pop_up = ctk.CTkToplevel()
        self.connection_pop_up.grab_set()           # Stop other window interaction
        self.connection_pop_up.focus_force()        # Set input focus to the popup
        self.connection_pop_up.lift()               #make sure pop up is above other window
        
        ctk.CTkLabel(self.connection_pop_up, text="Select a port below").pack()
        
        first_option, port_names = self.port_manager.get_port_names()
        if not port_names:
            self.port_label.configure(text="None")
        
        port_var = ctk.StringVar(value=first_option)
        self.port_menu = ctk.CTkOptionMenu(self.connection_pop_up, values=port_names,
                                         command=self.optionmenu_callback,
                                         variable=port_var)
        self.port_menu.pack(padx=5, pady=5)
        
        self.refresh_list_button = ctk.CTkButton(self.connection_pop_up, text="Refresh ports", command=self.refresh_ports_list)
        self.refresh_list_button.pack(pady=2)
        
        
    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        #send picked portname to pm
        self.port_manager.set_port(choice)
        self.port_label.configure(text=choice)
        self.connection_pop_up.destroy()
            
    def refresh_ports_list(self):
        first_option, port_names = self.port_manager.get_port_names()
        port_var = ctk.StringVar(value=first_option)
        self.port_menu.configure(values=port_names, variable=port_var)

        
        
        
    def set_pen_view(self):
        self.pop_up = ctk.CTkToplevel()
        self.pop_up.grab_set()           # Stop other window interaction
        self.pop_up.focus_force()        # Set input focus to the popup
        self.pop_up.lift()               #make sure pop up is above other window
        self.pop_up.iconbitmap('./graphics/turtle_logo.ico')
        
        down_label = ctk.CTkLabel(self.pop_up, text="Adjust pen height until it is just on the paper")
        down_label.pack(padx=5, pady=5)
        down_slider = ctk.CTkSlider(self.pop_up, from_=0, to=1, command=self.down_slider_event, number_of_steps=100)
        down_slider.pack(pady=5)
        down_slider.set(self.down)
        self.down_slider_event(self.down)
        save_button = ctk.CTkButton(self.pop_up, text="Save", command=self.save)
        save_button.pack(pady=5)
        

    def down_slider_event(self, value):
        print(value)
        #value=value/ranger
        value = round(value, 2)
        #if value<=0.8:
            #setup_value = round(value+0.2, 2)
            #self.port_manager.send_command("D"+str(setup_value))
            #self.up= setup_value
        #else:                                                           #very unlikely to occur as would mean ground is taller than wheels
            #setup_value = round(value-0.2, 2)
            #self.port_manager.send_command("D"+str(setup_value))
            #self.up= 1
        #self.port_manager.send_command("D"+string_value)
        #self.port_manager.send_command("o")
        if(abs(self.down-value)>0.02):
            self.port_manager.send_command("D"+str(value))      #never sets up
        self.down=value
        
    def save(self):
        self.port_manager.up = self.up
        self.port_manager.down = self.down
        self.port_manager.send_command("U"+str(self.up))
        print("save here")
        self.pop_up.destroy()
