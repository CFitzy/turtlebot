# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:47:59 2025
Class that handles all functions the user can get the turtle to do
@author: cmf6
"""
from customtkinter import END
from math import pi

class User_Turtle():
    #Initialise the class with access to the port manager and turtle simulation objects and the text output (for messages)
    def __init__(self, port_manager, turtle_sim, text_output):      
        self.port_manager = port_manager
        self.turtle_sim = turtle_sim
        self.text_output = text_output   
        #Whether object is in compile mode (for working out turtle simulation scaling purposes)
        self.compile_mode =True   
        #List of commands in sequnce so far (for working out turtle simulation scaling purposes)                         
        self.commands_list = []
       
    #Use the turtle_simulation class to work out the scale its turtle should be at so it stays in view
    def find_simulation_scale(self):
        self.turtle_sim.work_out_scale(self.commands_list)
        #Compiling finished
        self.compile_mode = False
        
    #Move the turtle forward by number of millimeters
    def forward(self, number):
        #If in compile mode put in commands list
        if self.compile_mode:
            self.commands_list.append("F"+str(int(number)))
            
        else: 
            #Send code to the turtle simulation in Python Turtle graphics code
            self.turtle_sim.run_code("turtle.forward("+str(number)+")")
            #If turtlebot connected send it the forward command
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("F"+str(number))
        
    #Turn the turtle right by number of degrees
    def right(self, number):
        #If in compile mode put in commands list
        if self.compile_mode:
            self.commands_list.append("R"+str(number))
        else: 
            #Send code to the turtle simulation in Python Turtle graphics code
            self.turtle_sim.run_code("turtle.right("+str(number)+")")
            #If turtlebot connected send it the turn command
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("T"+str(number))
       
    #Turn the turtle left by number of degrees
    def left(self, number):
        #If in compile mode put in commands list
        if self.compile_mode:
            self.commands_list.append("L"+str(number))
        else: 
            #Send code to the turtle simulation in Python Turtle graphics code
            self.turtle_sim.run_code("turtle.left("+str(number)+")")
            #If turtlebot connected send it the turn command (negative as anticlockwise)
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("T-"+str(number))
        
    #Move the turtle in a curve of length arc_len with an angle of angle
    def curve(self, arc_len, angle):
        #Work out radius from angle and arc length
        radius= (180*arc_len)/(angle*pi)
        #If in compile mode put in commands list with comma to seperate values
        if self.compile_mode:
            self.commands_list.append("C"+str(arc_len)+","+str(angle))
        else: 
            #Send code to the turtle simulation in Python Turtle graphics code
            #The radius is negative so it turns right (same way as turtlebot)
            self.turtle_sim.run_code("turtle.circle(-"+str(radius)+","+str(angle)+")", output= "turtle.curve("+str(arc_len)+","+str(angle)+")")
            #If turtlebot connected send it the curve command
            if self.port_manager.turtle_connection: 
                self.port_manager.send_command("C"+str(arc_len)+" "+str(angle))        
    

    #Move the pen down   
    def down(self):
        #If not in compile mode send the simulation the corresponding turtle library code
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.down()")
            #If turtlebot connected send it the down command
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("D")
      
    #Move the pen up
    def up(self):
        #If not in compile mode send the simulation the corresponding turtle library code
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.up()")
            #If turtlebot connected send it the up command
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("U")
      
    #Display given message
    def message(self, message):
        #If not in compile mode write the message to the output box
        if not self.compile_mode:
            self.text_output.configure(state="normal")
            self.text_output.insert(END, text=message+"\n")
            self.text_output.configure(state="disabled")
            #If turtlebot connected also send the message to its display
            if self.port_manager.turtle_connection:
                self.port_manager.send_command("="+message)
        