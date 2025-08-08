# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:06:05 2025

@author: cmf6
"""
import tkinter as tk
import customtkinter as ctk
import re
import time
import math
from PIL import Image

class setup_wizard():
    def __init__(self, port_manager):
        self.circle_steps = 4096
        self.port_manager = port_manager
        self.settings = {}
        self.main_button_height = 0.8
        self.paragraph_font = ("Roboto", 14)
        self.pop_up_size = 500
        
        path = "./graphics/"
        
        self.turtle_image = ctk.CTkImage(light_image=Image.open(path+"abstract_turtle.png"), size=(100, 100))
        self.diameter_image = ctk.CTkImage(light_image=Image.open(path+"abstract_turtle_line.png"), size=(400, 100))
        self.axle_images = [
            ctk.CTkImage(light_image=Image.open(path+"abstract_turtle_axle.png"), size=(240, 160)), 
            ctk.CTkImage(light_image=Image.open(path+"overlap.png"), size=(60, 50)), 
            ctk.CTkImage(light_image=Image.open(path+"gap.png"), size=(60, 50))
            ]
        self.axle_image_first=True
        
    def get_settings(self, settings):
        #'wheelL 53.18\r\nwheelR 53.18\r\nAxle 79.04\r\nPenU  0.40\r\nPenD  0.30\r\nBacklashL 0\r\nBacklashR 0\r\n'
        print(settings)
        split_settings = re.split(r'[ \r\n]+', settings)
        print(split_settings)
        
        #stick all the settings into a dictionary
        for i in range(0, (len(split_settings)-1), 2):
            self.settings[split_settings[i]] = split_settings[i+1]
        print(self.settings)
        
    def make_title(self, title_text):
        ctk.CTkLabel(self.frame, text=title_text, font=("Roboto", 16)).place(relx=0.5, rely=0.05, anchor=ctk.CENTER)
    
    def make_paragraph(self, label_text):
        ctk.CTkLabel(
            self.frame, text=label_text, font=self.paragraph_font, wraplength=self.pop_up_size-(0.1*self.pop_up_size)
                     ).place(relx=0.5, 
                                    rely=0.2, 
                                    anchor=ctk.CENTER
                                    )
                                    
    def make_button(self, frame, b_text, b_command):
        button = ctk.CTkButton(frame, text=b_text, command=b_command)
        button.place(relx=0.5, rely=0.8, anchor=ctk.CENTER)
        return button
    
    
    def setup_wizard(self):
        
        self.wizard_pop_up = ctk.CTkToplevel()
        self.wizard_pop_up.grab_set()           # Stop other window interaction
        self.wizard_pop_up.focus_force()        # Set input focus to the popup
        self.wizard_pop_up.lift()               #make sure pop up is above other window
        self.wizard_pop_up.title("Setup Wizard")
        self.wizard_pop_up.geometry(str(self.pop_up_size)+"x"+str(self.pop_up_size))
        
        self.wizard_pop_up.after(200, lambda :self.wizard_pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        
        self.frame = ctk.CTkFrame(self.wizard_pop_up, fg_color="transparent")
        self.frame.pack(expand=True, fill=ctk.BOTH)
        self.make_title("Setup turtlebot dimensions")
        
        if not self.port_manager.allow_writing:
            self.make_paragraph("Connect the turtlebot before setting it up")
            self.make_button(self.frame, "Close", self.wizard_pop_up.destroy)
        else:
            #get saved values
            self.get_settings(self.port_manager.get_settings())
            self.make_paragraph("You will need: \n*A ruler with mm\n*A big piece of paper (A3 or bigger recommended)")
            self.make_button(self.frame, "Start", self.check_backlash_start)
        
    def check_backlash_start(self):
        for w in self.frame.winfo_children():
            w.destroy()
            
        self.make_title("Setup turtlebot: Backlash")
        self.make_paragraph("Press start for the turtlebot to start")
        
        ctk.CTkLabel(self.frame, image=self.turtle_image, text="").place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        
        self.make_button(self.frame, "Start", self.check_backlash_main)
        
    def check_backlash_main(self):
        self.min = 0
        self.max =625
        self.current = 0 
        self.increment = 125
        for w in self.frame.winfo_children():
            w.destroy()
            
        # slow down
        self.port_manager.send_command("s1 4000")  
        self.port_manager.send_command("s7 0")
        self.port_manager.send_command("s8 0")    
        self.port_manager.send_command("f -"+str(self.max))
        
            
        self.make_title("Setup turtlebot: Backlash")
        self.make_paragraph("If the turtlebot moved forward, press Moved. Otherwise press No difference")
        
        output_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        output_frame.place(anchor=ctk.CENTER, relx= 0.5, rely=0.5)
        
        self.backlash_label = ctk.CTkLabel(output_frame, text=self.min, font=("Roboto", 14, "bold"))
        self.backlash_label.place(anchor=ctk.CENTER, relx= 0.5, rely=0.5)
        ctk.CTkLabel(output_frame, text="steps").place(anchor=ctk.CENTER, relx= 0.7, rely=0.5)
        
        self.back_button = ctk.CTkButton(self.frame, text="Restart", command=self.check_backlash_main, state=ctk.DISABLED, width=20)
        self.back_button.place(relx=0.87, rely=0.01)
        
        self.button_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.button_frame.place(rely=0.8, anchor=ctk.CENTER, relx=0.5)
        
        
        ctk.CTkButton(self.button_frame, text="No difference", command=self.backlash_forward).pack(side=ctk.LEFT)
        ctk.CTkButton(self.button_frame, text="Moved", command=self.backlash_moved).pack(side=ctk.LEFT, pady=3, padx=3)
        
        self.backlash_forward()
        
        
    def backlash_forward(self):  
        self.current = round(self.current+self.increment)
        if self.current>=self.max:
            self.end_backlash()
        else:
            self.port_manager.send_command("f "+str(self.current))       #f lowercase
            print("F:", self.min, self.increment, self.max)
            self.backlash_label.configure(text=self.current)
            
        
        
    def backlash_moved(self):
        self.min = round(self.current-self.increment, 5)
        
        self.port_manager.send_command("f -"+str(self.current))
        
        self.max = self.current
        self.current = self.min
        self.increment = round((self.increment/5),1)
        print("N:", self.min, self.increment, self.max)
            
        if self.increment <125:
            self.back_button.configure(state=ctk.NORMAL)
        if self.increment<1:
            self.end_backlash()
        else:
            self.backlash_label.configure(text=self.min)
            #sleep for 1 sec so the reverse -> forward is noticeable
            time.sleep(1)
            self.backlash_forward()
            
    def end_backlash(self):
        self.port_manager.send_command("o")
        # speed up
        self.port_manager.send_command("s1 1100")         
        #self.port_manager.send_command("s7 "+str(self.max))
        #self.port_manager.send_command("s8 "+str(self.max))
        self.settings.update({"BacklashL": self.max})
        self.settings.update({"BacklashR": self.max})
        print(self.settings)
        self.check_wheel_diameter()
    
    
    def check_wheel_diameter(self):
        for w in self.frame.winfo_children():
            w.destroy() 
            
        self.make_title("Setup turtlebot: Wheels")
        self.make_paragraph("Press Draw to draw a line. Measure the length then input the value")
        
        
        self.bottom_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.bottom_frame.place(relx=0.5)
        
        self.draw_diameter_button(True)
        
        
        
    def draw_diameter_button(self, first=False):
        self.bottom_frame.destroy()
        #self.wheel_draw_button.destroy()
        self.image_label = ctk.CTkLabel(self.frame, image=self.diameter_image, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        if not first:
            self.wheel_draw_button.destroy()
            button_text="Redraw"
        else:
            button_text="Draw"
        self.wheel_draw_button = self.make_button(self.frame, button_text, self.draw_for_diameter)
    def draw_for_diameter(self):
        for w in self.image_label.winfo_children():
            w.destroy()
        self.image_label.destroy()
        #self.wheel_draw_button.configure(text="Drawing")
        #Wheel Diameter simple calibration test 
        # slow down
        self.port_manager.send_command("s1 4000")
        # take up backlash
        
        self.port_manager.send_command("F 10")
        # lower pen
        self.port_manager.send_command("D")
        # move 30cm
        self.port_manager.send_command("F300")
        self.port_manager.send_command("U")
        # reset motor speed (uS per step, 1100 fastest @ 7Volt)
        self.port_manager.send_command("s1 1100")
        self.port_manager.send_command("o")
        #time.sleep(15)
        
        #we assume it will be straight "enough" as the wheels are most likely printed at the same time so have been effected equally
        
        self.bottom_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.bottom_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        length_frame = ctk.CTkFrame(self.bottom_frame, fg_color="transparent")
        length_frame.pack()
        ctk.CTkLabel(length_frame, text="Length:", font=self.paragraph_font).pack(side=ctk.LEFT)
        self.length_input = ctk.CTkTextbox(length_frame, height=40, width=60, font=self.paragraph_font)
        self.length_input.pack(side=ctk.LEFT, padx=2)
        ctk.CTkLabel(length_frame, text="mm", font=self.paragraph_font).pack(side=ctk.LEFT)
        self.wheel_draw_button.configure(text="Next", command=self.diameter_length_check)
        
        
    def diameter_length_check(self):
        #get length
        length = self.length_input.get("0.0",ctk.END)                         
        print(length)
        if self.validate_input(length):#input validation    
            if float(length) == 300:
                self.check_axle_length()
            else:
                self.wheel_draw_button.configure(text= "Adjusting")   #need to show user someting has happened based on their input
                self.calculate_wheel_diameter(length)
                self.draw_diameter_button()
            
    def calculate_wheel_diameter(self, length):
        #we have required distance dr and travelled distance dt
        #error distance de = dt-dr (positive if travels too far)

        # circumference of wheel, Wc= PI*Wd
        # wheel rotations = dr/Wc
        # percentage error = dt/dr
        #since wheel diameter is proportional to circumference we change the wheel diameter by a proportional amount
        #adjusted wheel diameter = dt/dr*Wd
        
        #get expected wheel diameter
        expected_diameter = self.settings.get("wheelL")
        
        actual_diameter = round((float(length)/300)*float(expected_diameter), 6)
        
        #set values for diameters
        self.port_manager.send_command("s2 "+str(actual_diameter))
        self.port_manager.send_command("s3 "+str(actual_diameter))
        self.settings.update({"wheelL": actual_diameter})
        self.settings.update({"wheelR": actual_diameter})
        print(self.settings)
        
        
    def check_axle_length(self):
        for w in self.frame.winfo_children():
            w.destroy()
            
        
            
        self.make_title("Setup turtlebot: Axle")
        self.make_paragraph("Press Draw to draw two circles. \nMeasure the distance of overlap/gap then input the values. \n(Make sure you recentre the turtlebot)")
        self.image_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.image_frame.place(relx=0.5, rely=0.5, anchor=ctk.CENTER)
        self.set_axle_image()
        self.axle_button = self.make_button(self.frame, "Draw", self.draw_for_axle)
        
    def set_axle_image(self):
        for w in self.image_frame.winfo_children():
            for wc in w.winfo_children():
                wc.destroy()
            w.destroy()
        if self.axle_image_first:
            ctk.CTkLabel(self.image_frame, image=self.axle_images[0], text="").pack()
            self.axle_image_first = False
        else:
            ctk.CTkLabel(self.image_frame, text="If a gap is formed, \nwrite the number as a negative", font=("Roboto", 13)).pack(side=ctk.LEFT,padx=5)
            ctk.CTkLabel(self.image_frame, image=self.axle_images[1], text="").pack(side=ctk.LEFT,padx=20)
            ctk.CTkLabel(self.image_frame, image=self.axle_images[2], text="").pack(side=ctk.LEFT, padx=20)
            self.axle_image_first = True
        
        
        
    def make_axle_length_inputs(self):
        #we assume it will be straight "enough" as the wheels are most likely printed at the same time so have been effected equally
        self.length_frame = ctk.CTkFrame(self.frame, fg_color="transparent")
        self.length_frame.place(relx=0.5, rely=0.65, anchor=ctk.CENTER)
        #Input view for first length
        ctk.CTkLabel(self.length_frame, text="Length:", font=self.paragraph_font).pack(side=ctk.LEFT)
        self.length_input = ctk.CTkTextbox(self.length_frame, height=40, width=60, font=self.paragraph_font)
        self.length_input.pack(side=ctk.LEFT, padx=2)
        ctk.CTkLabel(self.length_frame, text="mm", font=self.paragraph_font).pack(side=ctk.LEFT)
        #spacer
        ctk.CTkLabel(self.length_frame, fg_color="transparent",width=40, text="").pack(side=ctk.LEFT)
        #Input view for second length
        ctk.CTkLabel(self.length_frame, text="Length2:", font=self.paragraph_font).pack(side=ctk.LEFT)
        self.length_input2 = ctk.CTkTextbox(self.length_frame, height=40, width=60, font=self.paragraph_font)
        self.length_input2.pack(side=ctk.LEFT, padx=2)
        ctk.CTkLabel(self.length_frame, text="mm", font=self.paragraph_font).pack(side=ctk.LEFT)
        
    def draw_for_axle(self):
        #Axle length simple calibration test turn using only one wheel, if the wheel is calibrated any error will be due to the wheel spacing

        #   slow down
        self.port_manager.send_command("s1 3000")
        # remove backlash compensation settings
        self.port_manager.send_command("s7 0")
        self.port_manager.send_command("s8 0")

    # if Ar is Axle length (radius) and Wd is wheel diameter
    # then circumference is Ac = 2*Ar*PI
    # Wheel circumference Wc = Wd*PI 
    # so we need Ac/Wc rotation of the wheel
    # or (with 4096 steps per rotation) Ac/Wc*4096
    # so Ws = Ad/Wd

        self.port_manager.send_command("U")
    # Take up backlash
        self.port_manager.send_command("l 200")

        self.port_manager.send_command("D")

    #turn for a circle: ((2*axle)/wheel diameter)*steps for rotation
        self.port_manager.send_command("l "+str(round((((2*float(self.settings.get("Axle")))/float(self.settings.get("wheelL")))*4096))))

        self.port_manager.send_command("U")
        
        self.port_manager.send_command("F 30")

    #Take up backlash
        self.port_manager.send_command("r 200")

        self.port_manager.send_command("D")
    #r ((2*79.6)/53.02)*4096
    #r 12299
        self.port_manager.send_command("r "+str(round((((2*float(self.settings.get("Axle")))/float(self.settings.get("wheelR")))*4096))))
        self.port_manager.send_command("U")

    # turn off motors
        self.port_manager.send_command("F 30")
        self.port_manager.send_command("s1 1100")
        self.port_manager.send_command("o")
        self.set_axle_image()
        self.make_axle_length_inputs()
        self.axle_button.configure(text="Done", command=self.calculate_axle_length)

    def calculate_axle_length(self):
    # the circle ends either overlap or have a gap.
    # if they overlap reduce the axle length setting by 2mm until there is a gap 
    # (a gap is easier to measure)
    # to adjust axle take the average axle circumference error (Ace) of the two directions 
    # using the set Ad (axle length)
    # axle circumference is Ac = 2*Ad*PI
    # the percentage error Ace = (Ac+Ace)/Ac
    # so the axle is longer than the code thinks (calculated c is too small)
    # new axle length is Ace*Ad.

    # axle*(((2*axle*pi)-overlap)/(2*axle*pi))      
    #+gap for gap and -overlap
    #simplifies to axel-(overlap/2*pi) or axle+(gap/2*pi)
        print("calc")
        self.gap=False #remove
        #get length
        length = self.length_input.get("0.0",ctk.END)
        #get length2
        length2 = self.length_input2.get("0.0",ctk.END)
        #check input is a valid number
        if self.validate_input(length) and self.validate_input(length2):
            #if correct axel found
            if float(length) == 0 and float(length2) == 0:
                self.save_all()
            else:
                self.axle_button.configure(text= "Adjusting")
                avg_len = (float(length)+float(length2))/2
    
                #get expected wheel diameter
                expected_axle = float(self.settings.get("Axle"))
    
                #actual_axle = round(expected_axle -(avg_len/2*math.pi), 3)
                #actual_axle = round(expected_axle-(avg_len/(2*math.pi)), 6)     
                actual_axle = round(expected_axle-(avg_len/(math.pi)), 6)   
    
                #set values for axle
                self.settings.update({"Axle": actual_axle})
                self.port_manager.send_command("s4 "+str(actual_axle))
                print(self.settings)
                self.set_axle_image()
                self.axle_button.configure(text= "Redraw", command=self.draw_for_axle)
                self.length_frame.destroy()
            
            
        
    def validate_input(self, length):
        length = length.replace("\n", "")
        length_numeric = length.replace("-","")
        if len(length)==0:
            tk.messagebox.showerror("Wrong input", "Please fill in all values") 
            return False
        elif not length_numeric.replace(".", "").isnumeric():
            print(length)
            tk.messagebox.showerror("Wrong input", "Please enter a valid number") 
            return False
        else:
            return True
    
    def save_all(self):
        self.port_manager.send_command("s2 "+str(self.settings.get("wheelL")))
        self.port_manager.send_command("s3 "+str(self.settings.get("wheelR")))
        self.port_manager.send_command("s4 "+str(self.settings.get("Axle")))
        
        self.port_manager.send_command("s7 "+str(self.settings.get("BacklashL")))
        self.port_manager.send_command("s8 "+str(self.settings.get("BacklashR")))               
        #save the new settings
        self.port_manager.send_command("save")
        
        for w in self.frame.winfo_children():
            w.destroy()
            
        self.make_title("Setup complete")
        
        self.make_button(self.frame, "Finish", self.wizard_pop_up.destroy)
        