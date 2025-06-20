# -*- coding: utf-8 -*-
"""
Created on Thu May 29 13:36:54 2025
Makes UI screen so can type in python, press button to run (display on console) and display error messages on app
@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk
import turtle_simulation as ts
import code_input
import top_menu
import code_handler
import port_manager
import connection_state

class Main():
    def __init__(self):
        self.port_manager = port_manager.port_manager()
        self.code_handler = code_handler.Code_Handler(self.port_manager)
        ctk.set_appearance_mode("light")
        # make window
        root = ctk.CTk()
        # specify window size
        self.width, self.height=800,600
        root.geometry(str(self.width)+"x"+str(self.height))
        root.title("Turtlebot")
        #set logo image
        root.iconbitmap('./graphics/turtle_logo.ico')

        #Binding the resizing event
        root.bind("<Configure>", lambda event: self.update_window(root, event)) 
        
        self.top_menu = top_menu.Top_Menu(root, self.port_manager)
         
        self.code_input = code_input.Code_Input(root, self.clear_text)
        
        self.right_frame= ctk.CTkFrame(root, fg_color="transparent")
        self.right_frame.pack(side=ctk.LEFT, fill=ctk.Y)
        
        self.connection_frame = ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.usb_connection = ctk.CTkLabel(self.connection_frame, text="USB connection", text_color="red")
        self.usb_connection.pack(side=ctk.LEFT)
        self.turtle_connection = ctk.CTkLabel(self.connection_frame, text="Turtle connection", text_color="red")
        self.turtle_connection.pack(side=ctk.LEFT)
        self.refresh_button = ctk.CTkButton(self.connection_frame, text="Reset", command=self.port_manager.change_port, width=50)
        self.refresh_button.pack(side=ctk.LEFT)
        self.connection_frame.pack(side=ctk.TOP)
        connection_state.Connection_State(self.port_manager, self.usb_connection, self.turtle_connection)
        
        
        self.turtle = ts.Turtle_Simulation(self.right_frame)
        self.button_frame= ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.button_frame.pack(side=ctk.TOP)
        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset Turtle", command=self.turtle.reset, width=50)
        self.run_button = ctk.CTkButton(self.button_frame, text="Run", command=self.run_text, width=50)
        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop, width=50, state="disabled")
        self.buttons_layout(True)
        
        
        #shows output errors on label
        self.text_output = ctk.CTkLabel(master=self.right_frame, text="Error Output here", width=500, wraplength=200, height = 100)
        self.text_output.pack(pady=5)  
        #start window
        root.mainloop()
        

        
    #update window to meet current size requirements (for user experience the window is recommeded not to be smaller than (600,450))
    def update_window(self, root, event=None):
        self.code_input.resize(root.winfo_width()/2, root.winfo_height())
        self.turtle.resize(root.winfo_width()/2, root.winfo_height()/2)
            
        if root.winfo_width()<670:
            self.buttons_layout(horizontal=False)
        else:
            self.buttons_layout(horizontal=True)
            

        
    def buttons_layout(self, horizontal):
        if horizontal:
            self.reset_button.pack(side=ctk.LEFT, padx=4)
            self.run_button.pack(side=ctk.LEFT, padx=4)
            self.stop_button.pack(side=ctk.BOTTOM, padx=4)
        else:
            self.reset_button.pack(side=ctk.TOP, pady=4)
            self.run_button.pack(side=ctk.TOP, pady=4)
            self.stop_button.pack(side=ctk.TOP, pady=4)

        
    def clear_text(self):
        result = tk.messagebox.askquestion("Clear confirmation", "Are you sure you want to clear the program", )
        if result=="yes":
            self.code_input.clear()
            self.text_output.configure(text="")
            self.turtle.reset()


    def run_text(self):
        #disable to stop spamming of run button
        self.run_button.configure(state="disabled", text="Running")
        #disable to stop resetting mid program
        self.reset_button.configure(state="disabled")
        #enable stop button
        self.stop_button.configure(state="normal")
        
        self.code_handler.handle_code(self.code_input.get_code(), self.turtle, self.text_output)
        
        #reenable run button
        self.run_button.configure(state="normal", text="Run")
        #reenable reset button
        self.reset_button.configure(state="normal")
        #disable stop button
        self.stop_button.configure(state="disabled")
        
        

    def stop(self):
        #hide turtle
        self.turtle.stop_turtle()
        self.text_output.configure(text="Stopped")
        #disable stop button
        self.stop_button.configure(state="disabled")
        
        
          
if __name__=="__main__":
    Main()