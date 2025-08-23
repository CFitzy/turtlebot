# -*- coding: utf-8 -*-
"""
Created on Mon Jun  2 11:53:43 2025
Handles the turtle simulation. Runs the user code given, works out turtle scale to keep in view and reset the turtle
@author: cmf6
"""

from turtle import TurtleScreen
from turtle import RawTurtle
#Tkinter Canvas required as Customtkinter is coordinates based but turtle needs length based
from tkinter import Canvas
from customtkinter import CTkButton
from customtkinter import TOP
from customtkinter import END
from re import split
from math import sin
from math import cos
from math import radians
from math import pi
from math import ceil 


class Turtle_Simulation():
    def __init__(self, root, text_output):
        self.text_output = text_output
        #Angle the turtle is currently facing
        self.angle = 90
        #Start maximum size that the canvas has been
        self.max_canvheight, self.max_canvwidth = 200,200
        #Create Canvas to place turtle on
        self.canvas = Canvas(root, width=self.max_canvwidth, height=self.max_canvheight)
        self.canvas.pack(side=TOP)
        #Create turtle's screen
        self.screen = TurtleScreen(self.canvas)

        #Create turtle
        self.turtle = RawTurtle(self.screen, shape="turtle")
        #Whether system is currently stopped/running
        self.stopped = True
        #Current scale of the turtle
        self.scale = 1
        
        
        
        #Create reset turtle simulation button in the top right corner
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
        

    #Run the given code (will be a line at a time). Output for if there is a different output text to be shown then the code being run
    def run_code(self, code, output=None):
        #If the code is not stopped
        if not self.stopped:
            try:
                #Set output textbox to editable, print code wanting to be shown and then set to not editable.
                self.text_output.configure(state="normal")
                if output:
                    self.text_output.insert(END, text=output+"\n")
                else:
                    self.text_output.insert(END, text=code+"\n")
                self.text_output.configure(state="disabled")
                
                #SCALING   
                #Split code into sections
                split_code = split(r'[(),]+', code)
                #If command to go forward, scale the line size to the current scale and then reassemble into code line
                if split_code[0] == "turtle.forward":
                  split_code[1] = float(split_code[1])*self.scale
                  code=split_code[0]+"("+str(split_code[1])+")"

                #If command circle, scale the arc length(radius) size to the current scale and then reassemble into code line
                elif split_code[0] == "turtle.circle":
                  split_code[1] = float(split_code[1])*self.scale
                  code=split_code[0]+"("+str(split_code[1])+","+str(split_code[2])+")"

                #EXECUTING
                #Add "self." so does to premade turtle
                code_turtle = "self."+code
                #Execute code
                exec(code_turtle)
            #If an exception is thrown   
            except Exception as e:      
                #Display exception to the output
                self.text_output.configure(state="normal")
                self.text_output.insert(END, text="\n"+str(e))
                self.text_output.configure(state="disabled")
                #Stop the turtle from moving further
                self.stop_turtle()
        #Raise a stopped exception to stop the program
        else:
            raise Exception("Stopped")
            
    
    #Set the turtle to the stopped state  
    def stop_turtle(self):
        self.stopped =True
        
    #Set the turtle to the running state  
    def start_turtle(self):
        self.stopped =False

    #Get if the turtle is in the stopped state
    def get_stopped(self):
        return self.stopped
            
    #Reset the turtle simulation into the starting position       
    def reset(self):
        self.turtle.reset()
        #Reset the values for the dirction the turtle is facing and its scale
        self.scale=1
        self.angle=90
        
    #Resize turtle canvas to match window size
    def resize(self, width, height):
        self.canvas.configure(width=width, height=height)
        if height>self.max_canvheight:
            self.max_canvheight = height
        if width> self.max_canvwidth:
            self.max_canvwidth = width
        
        
    #Turn a given vector (direction and angle) into vertical and horizntal components and add to appropriate direction
    def turn_vector_into_components(self, angle, line):
        #Get horizontal distance
        x = float(line)*sin(radians(angle))
        #Get vertical distance
        y = float(line)*cos(radians(angle))
        #Horizontal: If positive add to the positive direction, else add to the negative
        if x>0:
            self.pos_horizontal = self.pos_horizontal+x
        else:
            self.neg_horizontal = self.neg_horizontal+x
        #Vertical: If positive add to the positive direction, else add to the negative
        if y>0:
            self.pos_vertical = self.pos_vertical+y
        else:
            self.neg_vertical = self.neg_vertical+y

        
    #Calculate required turtle scale for the turtle drawings to stay on screen
    def work_out_scale(self, lines):
        #Work out rough starting spot of the turtle
        width_scale= self.max_canvwidth/1700
        height_scale = self.max_canvheight/1500
        v_offset =self.canvas.winfo_height()*height_scale
        h_offset=self.canvas.winfo_width()*width_scale
        
        #Padding to keep turtle from edges
        padding =20
        #Distance travelled by the turtle in each direction
        self.neg_horizontal, self.pos_horizontal = 0,0
        self.neg_vertical, self.pos_vertical =0,0
        #Angle the turtle is currently facing
        angle = self.angle
        #Scale required by the turtle in each direction to stay on screen
        h_pos_scale, v_pos_scale, h_neg_scale, v_neg_scale= 1,1,1,1
        
        #For each code line, treat as required
        for line in lines:
            #If a curve movement   
            if line[0] == "C":
                #Split into angle and arc length
                values = line[1:].split(",")
                curve_angle = float(values[1])
                arc = float(values[0])
                #Test if either value is zero
                #If angle is zero treat as forward
                if curve_angle == 0:
                    line="F"+str(arc)
                #If arc is zero treat as right turn
                elif arc == 0:
                    line="R"+str(curve_angle)
                #Otherwise treat as curve
                else:
                    #Hold the angles
                    curve_angles = []
                    #Set angle amount left to process
                    angle_left = curve_angle
                    
                    #Split the given angle into 90 degree segments of angle and put in list
                    for i in range(0, ceil(abs(curve_angle)/90)):
                        if angle_left>90:
                            curve_angles.append(90)
                            angle_left= angle_left-90
                        elif angle_left<-90:
                            curve_angles.append(-90)
                            angle_left= angle_left+90
                        else:
                            curve_angles.append(angle_left)
                    print(curve_angles)
                                                
                    #For angles in the segment's angle list
                    for a in curve_angles:
                        #Calculate angle
                        angle = (angle+((a/90)*45))%360
                        
                        #Calculate arc length for segment (proportion of total arc length)
                        sector_arc = (a/curve_angle)*arc
                        #Calculate distance moved (chord length)
                        distance = (180*sector_arc*sin(radians(a)))/(a*pi)
                        #Break line into vertical and horizontal components
                        self.turn_vector_into_components(angle, distance)
            #If a forward movement, break line into components for the angle the turtle is currently moving
            if line[0] == "F":
                self.turn_vector_into_components(angle, line[1:])
                   
            #If left or right change current angle direction
            elif line[0] == "R":
                angle = (angle+float(line[1:]))%360
            elif line[0] == "L":
                angle = (angle-float(line[1:]))%360
        
        #Calculate required scaling in each direction
        #If moved West
        if self.neg_horizontal < 0:
            #Turtle start position(-padding) divided by the distance moved West
            h_neg_scale= (h_offset-padding)/(abs(self.neg_horizontal))
            
        #If moved East
        if self.pos_horizontal > self.canvas.winfo_width()-h_offset:
            #Width of canvas -Turtle start position(-padding) divided by the distance moved East
            h_pos_scale= (self.canvas.winfo_width()-h_offset-padding)/(self.pos_horizontal)
            
        #If moved South
        if self.neg_vertical <0:
            #Height of canvas -Turtle start position(-padding) divided by the distance moved South
            v_neg_scale= (self.canvas.winfo_height()-v_offset-padding)/(abs(self.neg_vertical))

        #If moved North
        if self.pos_vertical >0:
            #Turtle start position(-padding) divided by the distance moved North
            v_pos_scale= (v_offset-padding)/(abs(self.pos_vertical))
            print(v_pos_scale, (v_offset-padding), abs(self.pos_vertical))
        
        #New scale is set to the smallest scale required
        new_scale = min(h_neg_scale, h_pos_scale, v_neg_scale, v_pos_scale)
        
        #If the newscale is smaller than the current scale, set it to the current scale
        if new_scale<self.scale:
            self.scale = new_scale
        #Set the angle to the current angle
        self.angle = angle
        
        
        #Minimum turtle scale for it to still be visibly a turtle
        min_turtle_scale = 0.1
        
        #Shrink turtle the same as the lines are scaled down with threshold to keep it visible
        if self.scale>=min_turtle_scale:
            self.turtle.shapesize(stretch_wid=self.scale, stretch_len=self.scale, outline=1)
        else:
            self.turtle.shapesize(stretch_wid=min_turtle_scale, stretch_len=min_turtle_scale, outline=1)
            
        