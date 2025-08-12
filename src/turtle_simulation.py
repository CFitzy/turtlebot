# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:53:43 2025
Handles the turtle simulation. Runs the user code given, works out turtle scale to keep in view and reset the turtle
@author: cmf6
"""
import turtle
from tkinter import Canvas
from customtkinter import CTkButton
from customtkinter import TOP
from customtkinter import END
import re
import math

class Turtle_Simulation():
    def __init__(self, root, text_output):
        self.text_output = text_output
        self.angle = 90
        self.size_used=[0,0,0,0]
        #has to be tkinter canvas as customtkinter works coordinates based but turtle needs len
        self.canvas = Canvas(root, width=500, height=500)
        self.canvas.pack(side=TOP)
        self.screen = turtle.TurtleScreen(self.canvas)
        self.terry = turtle.RawTurtle(self.screen, shape="turtle")
        self.paused = False
        self.scale = 1
        
        self.reset_button = CTkButton(root, 
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
        


    def run_code(self, code, output=None):
        min_turtle_scale = 0.1
        
        if not self.paused:
            try:
                self.text_output.configure(state="normal")
                if output:
                    self.text_output.insert(END, text=output+"\n")
                else:
                    self.text_output.insert(END, text=code+"\n")
                self.text_output.configure(state="disabled")
                
                #shrink turtle with threshold to keep turtle visible
                if self.scale>=min_turtle_scale:
                    self.terry.shapesize(stretch_wid=self.scale, stretch_len=self.scale, outline=1)
                else:
                    self.terry.shapesize(stretch_wid=min_turtle_scale, stretch_len=min_turtle_scale, outline=1)
                #if turtle forward resize in that direction
                split_code = re.split(r'[(),]+', code)
                if split_code[0] == "turtle.forward":
                  split_code[1] = float(split_code[1])*self.scale
                  code=split_code[0]+"("+str(split_code[1])+")"
                  print(code)
                elif split_code[0] == "turtle.circle":
                  split_code[1] = float(split_code[1])*self.scale
                  code=split_code[0]+"("+str(split_code[1])+","+str(split_code[2])+")"
                  print(code)

                    
                #Execute code
                #added, otherwise doesn't know what the turtle is
                code_turtle = "turtle = self.terry \nturtle.speed(1) \n"+code
                exec(code_turtle)
                
            except Exception as e:      #compile can't catch name errors so instead catch line by line
                #display on output
                output_label.configure(state="normal")
                output_label.insert(END, text="\n"+str(e))
                output_label.configure(state="disabled")
                output_label.see(END)
                self.stop_turtle()
            
    
            
    def stop_turtle(self):
        self.paused =True
        
            #self.terry.home()
    def get_paused(self):
        return self.paused
            
            
    def reset(self):
        self.terry.reset()
        self.scale=1
        self.angle=90
        
    #resize turtle canvas
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        
    def work_out_scale(self, lines):
        offset =self.canvas.winfo_height()/3
        h_offset=self.canvas.winfo_width()/3
        padding =20
        neg_horizontal, pos_horizontal = offset, offset
        neg_vertical, pos_vertical =0,0
        angle = self.angle
        h_pos_scale, v_pos_scale, h_neg_scale, v_neg_scale= 1,1,1,1
        print(h_offset, offset)
        for line in lines:
            if line[0] == "F":
                x = int(line[1:])*math.sin(math.radians(angle))
                y = int(line[1:])*math.cos(math.radians(angle))
                if x>0:
                    pos_horizontal = pos_horizontal+x
                else:
                    neg_horizontal = neg_horizontal+x
                    
                if y>0:
                    pos_vertical = pos_vertical-y
                else:
                    neg_vertical = neg_vertical-y
                #horizontal = horizontal+x
                #vertical = vertical-y
                #print(horizontal, vertical)
                
            elif line[0] == "C":
                values = line[1:].split(",")
                print(values)
                curve_angle = int(values[1])
                arc = float(values[0])
                curve_angles = []
                loop_range = curve_angle//90
                if curve_angle%90 >0:
                    loop_range=loop_range+1
                    
                angle_left = curve_angle
                for i in range(0, loop_range):
                    if angle_left>90:
                        curve_angles.append(90)
                        angle_left= angle_left-90
                    else:
                        curve_angles.append(angle_left)
                                            
                print("ca", curve_angles)
                
                for a in curve_angles:
                    ##work out angle
                    angle = (angle+((a/90)*45))%360
                    
                    #work out dist moved
                    distance = (180*arc*math.sin(math.radians(a)))/(a*math.pi)
                    
                    ##work out angle
                    print(angle, distance)
                    
                x = int(distance)*math.sin(math.radians(angle))
                y = int(distance)*math.cos(math.radians(angle))
                if x>0:
                    pos_horizontal = pos_horizontal+x
                else:
                    neg_horizontal = neg_horizontal+x
                    
                if y>0:
                    pos_vertical = pos_vertical-y
                else:
                    neg_vertical = neg_vertical-y
              
                
            #if left or right change current direction
            elif line[0] == "R":
                angle = (angle+float(line[1:]))%360
            elif line[0] == "L":
                angle = (angle-float(line[1:]))%360
        print(neg_horizontal, pos_horizontal, neg_vertical, pos_vertical)
        #longest_len = max(vertical, horizontal)
        #min_length = min(vertical, horizontal)

        #smallest_screen_dimension = min(self.canvas.winfo_height(),self.canvas.winfo_width())
        
        if neg_horizontal < 0:
            h_neg_scale= (h_offset-padding)/(abs(neg_horizontal)+h_offset)
            print("h-", h_neg_scale)
        elif pos_horizontal > self.canvas.winfo_width()-h_offset:
            h_pos_scale= (self.canvas.winfo_width()-h_offset-padding)/(pos_horizontal)
            print("h+",h_pos_scale)
        
        #south
        if neg_vertical > self.canvas.winfo_height()-offset:
            v_neg_scale= (self.canvas.winfo_height()-offset-padding)/(neg_vertical)
            print("nv:",v_neg_scale)
        #north
        elif pos_vertical < -offset:
            v_pos_scale= (offset-padding)/(abs(pos_vertical)+offset)
            print("pv:",v_pos_scale)
        
        new_scale = min(h_neg_scale, h_pos_scale, v_neg_scale, v_pos_scale)

        if new_scale<self.scale:
            self.scale = new_scale
            print("newscale", new_scale)
        self.angle = angle

        