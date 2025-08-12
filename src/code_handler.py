# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:50:23 2025
Run user code via the User_Turtle class and the Turtle_Simulation class
@author: cmf6
"""

from customtkinter import END
from time import sleep
from user_turtle import User_Turtle

class Code_Handler():
    #Initialise class with variable for Port_manager instance
    def __init__(self, port_manager):
        self.port_manager = port_manager
        
    #Run the given code and output any exceptions 
    def handle_code(self, code_input, turtle, text_output):
        try:
            #Delete the current output
            text_output.configure(state="normal")
            text_output.delete(1.0, END)
            text_output.configure(state="disabled")
            #Unpause the turtle simulation
            turtle.paused = False
            #Make an instance of the User_Turtle class that can run the commands
            turtle = User_Turtle(self.port_manager, turtle, text_output)
            #Run compile mode to work out turtle simulation scaling
            exec(code_input)
            turtle.find_simulation_scale()
            #Run the code
            exec(code_input)
            
            #If the turtle is connected, send it a command to turn the motor off now that the code is done
            if self.port_manager.allow_writing:
                #Delay in case of message to allow time to view
                sleep(4)
                self.port_manager.send_command("o")
                
        #If exception, output it to the output area
        except Exception as e:
            print("E:",e)
            text_output.configure(state="normal")
            text_output.insert(END, text="\n"+str(e))
            text_output.configure(state="disabled")
            pass