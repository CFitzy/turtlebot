# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:50:23 2025

@author: cmf6
"""
import re
import customtkinter as ctk
from time import sleep
import tom as t

class Code_Handler():
    def __init__(self, port_manager):
        self.port_manager = port_manager
        
        
    def handle_code(self, code_input, turtle, text_output):
        try:
            text_output.configure(state="normal")
            text_output.delete(1.0, ctk.END)
            text_output.configure(state="disabled")
            turtle.paused = False
            tom = t.Tom(self.port_manager, turtle, text_output)
            #run compile mode
            exec(code_input)
            tom.find_simulation_scale()
            #run run
            exec(code_input)
            
            if self.port_manager.allow_writing:
                sleep(1)
                self.port_manager.send_command("o")
        
        except Exception as e:
            print("E:",e)
            text_output.configure(state="normal")
            text_output.insert(ctk.END, text="\n"+str(e))
            text_output.configure(state="disabled")
            pass