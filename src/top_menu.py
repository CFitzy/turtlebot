# -*- coding: utf-8 -*-
"""
Created on Thu Jun  5 15:04:28 2025

@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk
from PIL import Image
import file_handler as fh
import information_page as ip


class Top_Menu():
    def __init__(self, root, port_manager, top_bar_frame, connection_frame, change_textsize, set_text, get_text):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        
        file_handler = fh.File_Handler(get_text, set_text)
        self.port_manager = port_manager
        self.up = 0.35
        self.down=0.3
        
        #menubar = tk.Menu(top_bar_frame)
        file_button = self.make_top_menu_button(top_bar_frame, "File")
        settings_button  = self.make_top_menu_button(top_bar_frame, "Settings")
        
        
        file_button.menu = tk.Menu(file_button, tearoff=0, font=("12"))
        file_button["menu"] = file_button.menu
        
        file_button.menu.add_command(label="Save", command=lambda: file_handler.save())
        file_button.menu.add_command(label="Load", command=lambda: file_handler.load())
        
        
        settings_button.menu = tk.Menu(settings_button, tearoff=False, font=("12"))
        settings_button["menu"] = settings_button.menu
        
        settings_button.menu.add_command(label="Select port", command=self.make_connection_dropdown)
        
        settings_button.menu.add_command(label="Pen height", command=self.set_pen_view)
        #settings_button.menu.add_command(label="Font size")
        
        menu_font = tk.Menu(settings_button)
        settings_button.menu.add_cascade(menu=menu_font, label='Font size')
        #if in for loop will always default to last size
        menu_font.add_radiobutton(label=str(8)+" px", command=lambda: change_textsize(8))
        menu_font.add_radiobutton(label=str(10)+" px", command=lambda: change_textsize(10))
        menu_font.add_radiobutton(label=str(11)+" px", command=lambda: change_textsize(11))
        menu_font.add_radiobutton(label=str(12)+" px", command=lambda: change_textsize(12))
        menu_font.add_radiobutton(label=str(14)+" px", command=lambda: change_textsize(14))
        menu_font.add_radiobutton(label=str(16)+" px", command=lambda: change_textsize(16))
        menu_font.add_radiobutton(label=str(18)+" px", command=lambda: change_textsize(18))
        menu_font.add_radiobutton(label=str(20)+" px", command=lambda: change_textsize(20))
        menu_font.add_radiobutton(label=str(24)+" px", command=lambda: change_textsize(24))
        menu_font.add_radiobutton(label=str(28)+" px", command=lambda: change_textsize(28))
        menu_font.add_radiobutton(label=str(32)+" px", command=lambda: change_textsize(32))
        menu_font.add_radiobutton(label=str(36)+" px", command=lambda: change_textsize(36))
        menu_font.invoke(5)
        
        ip.Info_Page(top_bar_frame)
        
        
        reset_image = ctk.CTkImage(light_image=Image.open("./graphics/reset.png"), size=(20, 20))
        
        self.refresh_button = ctk.CTkButton(
                connection_frame, 
                image =reset_image, 
                text="", 
                fg_color="transparent", 
                hover_color="#007300", 
                command=self.port_manager.change_port, 
                width=20
                )
        
            
        self.refresh_button.pack(side=ctk.LEFT, padx=3)
        connection_frame.pack(side=ctk.RIGHT)
        
        #show which port is currently connected to
        self.port_label = ctk.CTkLabel(top_bar_frame, text="No port", text_color="#007D02", fg_color="white", width =50, height=20)
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
        button.pack(side=ctk.LEFT, pady=2)
        return button
    
    
    
    
    def make_connection_dropdown(self):
        self.connection_pop_up = ctk.CTkToplevel()
        self.connection_pop_up.grab_set()           # Stop other window interaction
        self.connection_pop_up.focus_force()        # Set input focus to the popup
        self.connection_pop_up.lift()               #make sure pop up is above other window
        
        ctk.CTkLabel(self.connection_pop_up, text="Select a port below").pack()
        
        port_names = []
        ports = self.port_manager.get_ports()
        
        for p in ports:
            port_names.append(p.name)
        
        if not ports:
            port_var = ctk.StringVar(value="No ports")
        else:
            port_var = ctk.StringVar(value="Select port")
        self.port_menu = ctk.CTkOptionMenu(self.connection_pop_up, values=port_names,
                                         command=self.optionmenu_callback,
                                         variable=port_var)
        self.port_menu.pack(padx=5, pady=5)
        
        self.refresh_list_button = ctk.CTkButton(self.connection_pop_up, text="Refresh ports", command=self.refresh_ports_list)
        self.refresh_list_button.pack()
        
        
    def optionmenu_callback(self, choice):
        print("optionmenu dropdown clicked:", choice)
        #send picked portname to pm
        self.port_manager.set_port(choice)
        self.port_label.configure(text=choice)
        self.connection_pop_up.destroy()
            
    def refresh_ports_list(self):
        port_names = []
        ports = self.port_manager.get_ports()
        
        for p in ports:
            port_names.append(p.name)
        
        if not ports:
            port_var = ctk.StringVar(value="No ports")
        else:
            port_var = ctk.StringVar(value="Select port")
        self.port_menu.configure(values=port_names, variable=port_var)

        
        
        
    def set_pen_view(self):
        self.pop_up = ctk.CTkToplevel()
        self.pop_up.grab_set()           # Stop other window interaction
        self.pop_up.focus_force()        # Set input focus to the popup
        self.pop_up.lift()               #make sure pop up is above other window
        
        self.down_view()
        
    def down_view(self):
        down_frame = ctk.CTkFrame(self.pop_up)
        down_frame.pack()
        down_label = ctk.CTkLabel(down_frame, text="Adjust pen height until it is just on the paper")
        down_label.pack(padx=5, pady=5)
        down_slider = ctk.CTkSlider(down_frame, from_=0, to=1, command=self.down_slider_event, number_of_steps=20)
        down_slider.pack(pady=5)
        down_slider.set(self.down)
        self.down_slider_event(self.down)
        next_button = ctk.CTkButton(down_frame, text="Save", command=self.save)
        next_button.pack(pady=5)
        

    def down_slider_event(self, value):
        print(value)
        #value=value/ranger
        value = round(value, 2)
        string_value = str(value)
        if value<=0.8:
            setup_value = round(value+0.2, 2)
            self.port_manager.send_command("D"+str(setup_value))
            self.up= setup_value
        else:                                                           #very unlikely to occur as would mean ground is taller than wheels
            setup_value = round(value-0.2, 2)
            self.port_manager.send_command("D"+str(setup_value))
            self.up= 1
        self.port_manager.send_command("D"+string_value)
        self.port_manager.send_command("o")
        self.down=value
        
    def save(self):
        self.port_manager.up = self.up
        self.port_manager.down = self.down
        self.port_manager.send_command("U"+str(self.up))
        print("save here")
        self.pop_up.destroy()
