# -*- coding: utf-8 -*-
"""
Created on Thu May 29 13:36:54 2025
Creates the main window. The application runs from this class.
@author: cmf6
"""

import customtkinter as ctk
from tkinter import messagebox
from turtle_simulation import Turtle_Simulation
from code_input import Code_Input
from top_menu import Top_Menu
from code_handler import Code_Handler
from port_manager import Port_Manager
from connection_display import Connection_Display


class Main():
    def __init__(self):
        ctk.set_appearance_mode("light")
        #Apply green turtlebot theme
        ctk.set_default_color_theme("./turtlebot_theme.json")
        # Make window
        root = ctk.CTk()
        # Specify window size
        self.width, self.height=800,600
        root.geometry(str(self.width)+"x"+str(self.height))
        #Set window title and logo image
        root.title("Turtlebot")
        root.iconbitmap('./graphics/turtle_logo.ico', default='./graphics/turtle_logo.ico')
        
        
        #Create UI inside window
        #Make top menu frame
        top_frame = ctk.CTkFrame(root, corner_radius=0)
        top_frame.pack(side=ctk.TOP, fill=ctk.X)
        #Create connections display for USB and turtlebot connections
        connection_display = Connection_Display()
        connection_layout = connection_display.make_connection_layout(top_frame)
        
        #Create instances of the Port_Manager and Code_Handler classes to pass to other classes
        self.port_manager = Port_Manager(connection_display)
        self.code_handler = Code_Handler(self.port_manager)
        
        #Create code input box
        self.code_input = Code_Input(root, self.clear_text)
        
        #Create right frame to put simulation, buttons and output in
        self.right_frame= ctk.CTkFrame(root, fg_color="transparent")
        
        #Shows output errors on label
        self.text_output = ctk.CTkTextbox(self.right_frame, width=300, corner_radius=0, state="disabled")
        
        #Create the top menu with file, insert and settings options and connection display
        self.top_menu = Top_Menu(root, 
                                          self.port_manager, 
                                          top_frame,
                                          connection_layout, 
                                          self.change_textsize,
                                          self.code_input.set_code,
                                          self.code_input.get_code,
                                          self.code_input.insert_code
                                          )
         
        self.right_frame.pack(side=ctk.LEFT, fill=ctk.Y)
        
        #Create the turtle simulation
        self.turtle_view = Turtle_Simulation(self.right_frame, self.text_output)
        
        #Create run and stop buttons in their own frame initally in horizontal layout
        self.button_frame= ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.button_frame.pack(side=ctk.TOP, pady=2)
        
        self.run_button = self.button_setup(self.button_frame, "Run", self.run_text, "normal")
        self.stop_button = self.button_setup(self.button_frame, "Stop", self.stop, "disabled")
        self.buttons_layout(True)
        
        #Pack text_output so appears below buttons
        self.text_output.pack(pady=5)  
        
        #Binding the resizing event
        root.bind("<Configure>", lambda event: self.update_window(root, event)) 
        
        #When window destroyed (with right hand window cross) close port and destroy window
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        
        #Start window
        root.mainloop()
        
        
        
    #When closing close the current port then the window
    def on_closing(self, root):
        self.port_manager.close_port()
        root.destroy()
        
        
    #Make a CustomTkinter button of set width
    def button_setup(self, frame, text, command, state):
        return ctk.CTkButton(frame, text=text, command=command, width=50, state=state)


    #Change the text size of the code input box and the output box
    def change_textsize(self, size):
        self.code_input.change_textsize(size)
        self.text_output.configure(font=("Helvetica", size))
        

    #Update window layout to match curent window size, root=current window
    #(for user experience the window is recommeded not to be smaller than (600,450))
    def update_window(self, root, event=None):
        #Resize code input box to be half of the window width and the same height
        self.code_input.resize(root.winfo_width()/2, root.winfo_height())
        #Resize turtle box to be half of the window width and half its height
        self.turtle_view.resize(root.winfo_width()/2, root.winfo_height()/2)
        #Resize turtle box to be half of the window width and less than half its height
        self.text_output.configure(width=root.winfo_width()/2, height=root.winfo_height()/2.5)
        #Layout buttons differently depending on the window width 
        if root.winfo_width()<670:
            self.buttons_layout(horizontal=False)
        else:
            self.buttons_layout(horizontal=True)
            

    #Change Run/Stop button layout depending on window size
    def buttons_layout(self, horizontal):
        #If in horizontal position pack horizontally
        if horizontal:
            self.run_button.pack(side=ctk.LEFT, padx=4)
            self.stop_button.pack(side=ctk.BOTTOM, padx=4)
        ##Otherwise pack vertically
        else:
            self.run_button.pack(side=ctk.TOP, pady=4)
            self.stop_button.pack(side=ctk.TOP, pady=4)


    #Clear the code text if confirmed
    def clear_text(self):
        #Pop up messagebox asking for confirmation
        result = messagebox.askquestion("Clear confirmation", "Are you sure you want to clear the program?")
        #If confirmed clear the code, its output and reset the turtle to its original position
        if result=="yes":
            self.code_input.clear()
            self.text_output.configure(state="normal")
            self.text_output.delete(1.0, ctk.END)
            self.text_output.configure(state="disabled")
            self.turtle_view.reset()


    #Run the code in the textbox
    def run_text(self):
        #Disable to stop spamming of run button
        self.run_button.configure(state="disabled", text="Running")
        #Disable to stop resetting mid program
        self.turtle_view.reset_button.configure(state="disabled")
        #Enable stop button
        self.stop_button.configure(state="normal")
        
        #Run code using Code_Handler class
        self.code_handler.handle_code(self.code_input.get_code(), self.turtle_view, self.text_output)
        
        #Re-enable run button
        self.run_button.configure(state="normal", text="Run")
        #Re-enable reset button
        self.turtle_view.reset_button.configure(state="normal")
        #Disable stop button
        self.stop_button.configure(state="disabled")
        
        
    #Stop the running program
    def stop(self):
        #Stop the turtle simulation
        self.turtle_view.stop_turtle()
        #Disable stop button
        self.stop_button.configure(state="disabled")
        
        
#Run from here by making insatnce of Main class        
if __name__=="__main__":
    Main()