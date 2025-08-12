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
       
    
    def find_simulation_scale(self):
        self.turtle_sim.work_out_scale(self.commands_list)
        self.compile_mode = False
        
    def forward(self, number):
        if self.compile_mode:
            self.commands_list.append("F"+str(int(number)))
            
        else: 
            number = int(round(number))
            self.turtle_sim.run_code("turtle.forward("+str(number)+")")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("F"+str(number))
        
        
    def right(self, number):
        if self.compile_mode:
            self.commands_list.append("R"+str(number))
        else: 
            self.turtle_sim.run_code("turtle.right("+str(number)+")")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("T"+str(number))
        
    def left(self, number):
        if self.compile_mode:
            self.commands_list.append("L"+str(number))
        else: 
            
            self.turtle_sim.run_code("turtle.left("+str(number)+")")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("T-"+str(number))
                
    def curve(self, arc_len, angle):      #not cir, arc dist
        #radius= (180*arc_len)/(angle*pi)
        radius= (180*arc_len)/(angle*pi)
        if self.compile_mode:
            self.commands_list.append("C"+str(arc_len)+","+str(angle))
        else: 
            #turtle.circle(radius, extent(how much of circle does), steps=None)
            #minus so turns right
            self.turtle_sim.run_code("turtle.circle(-"+str(radius)+","+str(angle)+")", output= "turtle.curve("+str(arc_len)+","+str(angle)+")")
            if self.port_manager.allow_writing:
                
                self.port_manager.send_command("C"+str(arc_len)+" "+str(angle))        
    
    
    
        
    def down(self):
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.down()")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("D")
        
    def up(self):
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.up()")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("U")
            
    def message(self, message):
        if not self.compile_mode:
            self.text_output.configure(state="normal")
            self.text_output.insert(END, text=message+"\n")
            self.text_output.configure(state="disabled")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("="+message)
        