# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:53:43 2025
Handle the turtle simulation, running the user typed code and resets
@author: cmf6
"""
import turtle
import customtkinter as ctk
import tkinter as tk

class Turtle_Simulation():
    def __init__(self, root):
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.canvas = tk.Canvas(root, width=425, height=425)
        self.canvas.pack(side=ctk.TOP)
        screen = turtle.TurtleScreen(self.canvas)
        self.terry = turtle.RawTurtle(screen, shape="turtle")
        self.paused = False
        self.pause_pos = self.terry.pos()
        self.pause_angle = self.terry.tiltangle()
        


    def run_code(self, code, output_label):
        if not self.paused:
            try:
                #added, otherwise doesn't know what the turtle is
                code_turtle = "turtle = self.terry \n"+code
                exec(code_turtle)
            except Exception as e:      #compile can't catch name errors so instead catch line by line
                output_label.configure(text=output_label.cget("text")+"\n"+str(e))
                self.stop_turtle()
            
            
    def test_code(self, code, output_label):
        #try compile, display errors on label
        try:
            #added, otherwise doesn't know what the turtle is
            code_turtle = "turtle = self.terry \n"+code
            #can't throw name errors
            compile(code_turtle, 'test', 'exec')
            self.paused=False
        except SyntaxError as e:
            #-1 as automatically starts at 2
            display = "Syntax Error at line "+str(e.lineno-1) +"\n "+str(e.msg)
            output_label.configure(text=display)
        except Exception as e:
            output_label.configure(text=e)
            
    def stop_turtle(self):
        self.paused =True
        
            #self.terry.home()
    def get_paused(self):
        return self.paused
            
            
    def reset(self):
        self.terry.reset()
        
    #resize turtle canvas
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        