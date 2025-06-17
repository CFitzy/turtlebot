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
        #try execute, display errors on label
        try:
            self.terry.pendown()
            self.play=True
            output_label.configure(text="Running")
            #added, otherwise doesn't know what the turtle is
            code_turtle = "turtle = self.terry \n"+code
            exec(code_turtle)
            
            #self.play = False
            if self.paused:
                self.terry.setpos(self.pause_pos)
                self.terry.setheading(self.pause_angle)
                self.stop_label.destroy()
            else:
                output_label.configure(text="Completed Successfully")
            self.terry.showturtle()
            
        
        except NameError as e:
            output_label.configure(text="Spelling Error: "+str(e))
        except SyntaxError as e:
            #+str(e.text)
            #-1 as automatically starts at 2(?)
            display = "Syntax Error at line "+str(e.lineno-1) +"\n "+str(e.msg)
            output_label.configure(text=display)
        except Exception as e:
            output_label.configure(text=e)
            
    def hide_drawing(self, output_label):
        self.paused =True
        self.pause_pos = self.terry.pos()
        self.pause_angle = self.terry.heading()
        self.terry.penup()
        self.terry.hideturtle()
        self.stop_label = ctk.CTkLabel(self.canvas, text="Stopping simulation",bg_color="white",width=self.canvas.winfo_width(), height=self.canvas.winfo_height(), font=("Arial", 12, "bold"))
        self.stop_label.place(relx=0.5,rely=0.5, anchor=tk.CENTER)
        output_label.configure(text="Stopped")
            #self.terry.home()
            
            
    def reset(self):
        self.terry.reset()
        
    #resize turtle canvas
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        