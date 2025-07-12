# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 13:47:59 2025

@author: cmf6
"""
import customtkinter as ctk

class Tom():
    def __init__(self, port_manager, turtle_sim, text_output):
        self.code_dictionary = {
            "turtle.forward": "F",  #will need more
            "turtle.right": "T",
            "turtle.left": "T-",
            "print":"=",
            "turtle.up": "U",
            "turtle.down": "D"
            }       
        self.port_manager = port_manager
        self.turtle_sim = turtle_sim
        self.text_output = text_output   
        self.compile_mode =True                           #compile mode to work out scaling?
        self.commands_list = []
        
    def find_simulation_scale(self):
        self.turtle_sim.work_out_scale(self.commands_list)
        self.compile_mode = False
        
    def forward(self, number):
        if self.compile_mode:
            self.commands_list.append("F"+str(number))
        else: 
            print(number)
            self.turtle_sim.run_code("turtle.forward("+str(number)+")", self.text_output)
            if self.port_manager.allow_writing:
                self.port_manager.send_command("F"+str(number))
        
        
    def right(self, number):
        if self.compile_mode:
            self.commands_list.append("R"+str(number))
        else: 
            print(number)
            self.turtle_sim.run_code("turtle.right("+str(number)+")", self.text_output)
            if self.port_manager.allow_writing:
                self.port_manager.send_command("T"+str(number))
        
    def left(self, number):
        if self.compile_mode:
            self.commands_list.append("L"+str(number))
        else: 
            print(number)
            self.turtle_sim.run_code("turtle.left("+str(number)+")", self.text_output)
            if self.port_manager.allow_writing:
                self.port_manager.send_command("T-"+str(number))
        
    def down(self):
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.down()", self.text_output)
            if self.port_manager.allow_writing:
                self.port_manager.send_command("D")
        
    def up(self):
        if not self.compile_mode:
            self.turtle_sim.run_code("turtle.up()", self.text_output)
            if self.port_manager.allow_writing:
                self.port_manager.send_command("U")
            
    def message(self, message):
        if not self.compile_mode:
            self.text_output.configure(state="normal")
            self.text_output.insert(ctk.END, text=message+"\n")
            self.text_output.configure(state="disabled")
            if self.port_manager.allow_writing:
                self.port_manager.send_command("="+message)
        