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
        self.canvas = tk.Canvas(root)
        self.canvas.config(width=425, height=425)
        self.canvas.pack(side=ctk.TOP)
        screen = turtle.TurtleScreen(self.canvas)
        self.terry = turtle.RawTurtle(screen, shape="turtle")
        self.terry.write("hello")
    

    def run_code(self, code, outputLabel):
        #try execute, display errors on label
        try:
            outputLabel.configure(text="Running")
            self.terry.showturtle()
            self.terry.pendown()
            #added, otherwise doesn't know what the turtle is
            code_turtle = "turtle = self.terry \n"+code
            exec(code_turtle)
            outputLabel.configure(text="Completed Successfully")
        
        except NameError as e:
            outputLabel.configure(text="Spelling Error: "+str(e))
        except SyntaxError as e:
            #+str(e.text)
            #-1 as automatically starts at 2(?)
            display = "Syntax Error at line "+str(e.lineno-1) +"\n "+str(e.msg)
            outputLabel.configure(text=display)
        except Exception as e:
            outputLabel.configure(text=e)
            
    def reset(self):
        self.terry.reset()
        
    #resize turtle canvas
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        
    def stop(self):
        #effectively stop turtle
        self.terry.penup()
        self.terry.hideturtle()
        