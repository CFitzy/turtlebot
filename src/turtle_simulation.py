# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:53:43 2025
Handle the turtle simulation, running the user typed code and resets
@author: cmf6
"""
import turtle
import customtkinter as ctk
import tkinter as tk
import re
import math

class Turtle_Simulation():
    def __init__(self, root):
        self.angle = 90
        self.size_used=[0,0,0,0]
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack(side=ctk.TOP)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.terry = turtle.RawTurtle(self.screen, shape="turtle")
        self.paused = False
        self.scale = 1
        
        self.reset_button = ctk.CTkButton(root, 
                                          text="Reset", 
                                          command=self.reset, 
                                          state="normal", 
                                          width=20,
                                          fg_color="#DDDDDD",
                                          bg_color="white",
                                          text_color="black",
                                          hover_color="#BBBBBB"
                                          )
        self.reset_button.place(relx=0.99, y=2, x=0, anchor="ne")
        


    def run_code(self, code, output_label):
        if not self.paused:
            try:
                self.terry.shapesize(stretch_wid=self.scale, stretch_len=self.scale, outline=1)
                #if turtle forward resize in that direction
                split_code = re.split(r'[()]+', code)
                if split_code[0] == "turtle.forward":
                  split_code[1] = float(split_code[1])*self.scale
                  code=split_code[0]+"("+str(split_code[1])+")"
                  print(code)
                   # vertical = float(split_code[1])*math.cos(self.angle)
                    #if horizontal> self.canvas.canvwidth/2:
                     #   self.screen.screensize(canvwidth=self.screen.canvwidth +horizontal, canvheight=self.screen.canvheight)
                     #   
                        
                #if left or right change current direction
                #elif split_code[0] == "turtle.right":
               #     self.angle = (self.angle+float(split_code[1]))%360
                #elif split_code[0] == "turtle.left":
                #    self.angle = (self.angle-float(split_code[1]))%360
                    
                #Execute code
                #added, otherwise doesn't know what the turtle is
                code_turtle = "turtle = self.terry \nturtle.speed(1) \n"+code
                exec(code_turtle)
                
            except Exception as e:      #compile can't catch name errors so instead catch line by line
                #display on output
                output_label.configure(state="normal")
                output_label.insert(ctk.END, text="\n"+str(e))
                output_label.configure(state="disabled")
                output_label.see(ctk.END)
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
            display = "Syntax Error at line "+str(e.lineno-1) +str(e.msg)
            output_label.configure(state="normal")
            output_label.insert(ctk.END, text="\n"+display)
            output_label.configure(state="disabled")
            output_label.see(ctk.END)
        except Exception as e:
            output_label.configure(state="normal")
            output_label.insert(ctk.END, text="\n"+e)
            output_label.configure(state="disabled")
            output_label.see(ctk.END)
            
    def stop_turtle(self):
        self.paused =True
        
            #self.terry.home()
    def get_paused(self):
        return self.paused
            
            
    def reset(self):
        self.terry.reset()
        self.scale=1
        
    #resize turtle canvas
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        
    def work_out_scale(self, lengths):
        max_len = max(lengths)
        min_len = -1 * min(lengths)
        longest_len = max(max_len, min_len)
        print(max(lengths))
        print(min(lengths))
        print(longest_len)
        print(self.canvas.winfo_height(), self.canvas.winfo_width())
        smallest_screen_dimension = min(self.canvas.winfo_height(),self.canvas.winfo_width())
        if longest_len > smallest_screen_dimension -130:
            new_scale= (smallest_screen_dimension-130)/(longest_len)
            print(self.scale, " ", longest_len*self.scale)
            if new_scale<self.scale:
                print(new_scale)
                self.scale = new_scale
        print("boop")
        