# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 11:06:05 2025
Create setup wizard pop up and process for calibrating the turtlebot
@author: cmf6
"""
from tkinter import messagebox
from customtkinter import CTkImage
from customtkinter import CTkFrame
from customtkinter import CTkButton
from customtkinter import CTkLabel
from customtkinter import CTkToplevel
from customtkinter import CTkTextbox
from customtkinter import CENTER
from customtkinter import NORMAL
from customtkinter import DISABLED
from customtkinter import BOTH
from customtkinter import LEFT
from customtkinter import END
from time import sleep
from PIL import Image
from setup_wizard_calculator import Setup_Wizard_Calculator

class Setup_Wizard():
    def __init__(self, port_manager):
        #Create instance of the Setup Wizard Calculator to do the backend steps for the UI elements (turtlebot movements and calculations)
        self.backend_magic = Setup_Wizard_Calculator(port_manager)
        #Define main font size for the pop up
        self.paragraph_font = ("Roboto", 14)
        #Define the pop up size
        self.pop_up_size = 500
        #Path to all graphics in the project
        path = "./graphics/"
        #First image
        self.turtle_image = CTkImage(light_image=Image.open(path+"abstract_turtle.png"), size=(100, 100))
        #Image to demonstrate how the turtlebot moves during wheel diameter calibrations
        self.diameter_image = CTkImage(light_image=Image.open(path+"abstract_turtle_line.png"), size=(400, 100))
        #Image to demonstrate how the turtlebot moves during axle length calibrations and what is meant by an overlap or gap
        self.axle_images = [
            CTkImage(light_image=Image.open(path+"abstract_turtle_axle.png"), size=(240, 160)), 
            CTkImage(light_image=Image.open(path+"overlap.png"), size=(60, 50)), 
            CTkImage(light_image=Image.open(path+"gap.png"), size=(60, 50))
            ]
        #Whether the first set of axle images or second should be shown
        self.axle_image_first=True
    
    #Create the setup wizard pop up
    def setup_wizard(self):
        #Create pop up
        self.wizard_pop_up = CTkToplevel()
        self.wizard_pop_up.grab_set()           # Stop other window interaction
        self.wizard_pop_up.focus_force()        # Set input focus to the popup
        self.wizard_pop_up.lift()               #make sure pop up is above other window
        self.wizard_pop_up.title("Setup Wizard")
        self.wizard_pop_up.geometry(str(self.pop_up_size)+"x"+str(self.pop_up_size))
        #Stops icon being overwritten by the default
        self.wizard_pop_up.after(200, lambda :self.wizard_pop_up.iconbitmap('./graphics/turtle_logo.ico'))
        #Create frame to put items onto  the wizard pop up
        self.frame = CTkFrame(self.wizard_pop_up, fg_color="transparent")
        self.frame.pack(expand=True, fill=BOTH)
        #Create initial title
        self.make_title("Setup turtlebot dimensions")
        #If the turtlebot is not connected prompt the user to connect it first
        if not self.backend_magic.get_settings():
            self.make_paragraph("Connect the turtlebot before setting it up")
            self.make_button(self.frame, "Close", self.wizard_pop_up.destroy)
        #If the turtlebot is connected, brief the user with the equipment they will need and give them a button to start
        else:
            self.make_paragraph("You will need: \n*A ruler with mm\n*A big piece of paper (A3 or bigger recommended)")
            self.make_button(self.frame, "Start", self.calibrate_backlash)
        
    #Create a title for the setup wizard
    def make_title(self, title_text):
        CTkLabel(self.frame, text=title_text, font=("Roboto", 16)).place(relx=0.5, rely=0.05, anchor=CENTER)
    
    #Create a paragraph for the setup wizard to provide instructions
    def make_paragraph(self, label_text):
        CTkLabel(
            self.frame, text=label_text, font=self.paragraph_font, wraplength=self.pop_up_size-(0.1*self.pop_up_size)
                     ).place(relx=0.5, rely=0.2, anchor=CENTER)
           
    #Create a button for the setup wizard, places near the bottom                      
    def make_button(self, frame, b_text, b_command):
        button = CTkButton(frame, text=b_text, command=b_command)
        button.place(relx=0.5, rely=0.8, anchor=CENTER)
        return button
    
    
    #Create basic layout for each setup wizard process
    def basic_layout(self, layout):
        #Clear previous layout
        for w in self.frame.winfo_children():
            w.destroy()
        #Set and make title 
        title = "Setup turtlebot: "+layout
        self.make_title(title) 
        #Based on required layout make paragraph or button
        match layout:
            case "Backlash":
                self.make_paragraph("If the turtlebot moved forward, press Moved. Otherwise press No difference")
            case "Backlash In Progress":   
                self.make_paragraph("Press start for the turtlebot to start")
                
            case "Wheels":
                self.make_paragraph("Press Draw to draw a line. Measure the length then input the value")
            
            case "Axle":
                self.make_paragraph("Press Draw to draw two circles. \nMeasure the distance of overlap/gap then input the values. \n(Make sure you recentre the turtlebot)")
            case "Complete":
                self.make_button(self.frame, "Finish", self.wizard_pop_up.destroy)
        #Create bottom frrame for other contents
        self.bottom_frame = CTkFrame(self.frame, fg_color="transparent")
        self.bottom_frame.place(relx=0.5, rely=0.5, anchor=CENTER, relwidth=1)
        
        
    #Validate user input for a distance
    def validate_input(self, length):
        #Remove any newlines and negatives
        length = length.replace("\n", "")
        length_numeric = length.replace("-","")
        #If no value was entered, show error messagebox (warning pop up) telling user to fill in all values
        if len(length)==0:
            messagebox.showerror("Wrong input", "Please fill in all values") 
            #Return that values were not valid
            return False
        #If values that were non numerical were entered, show error message telling user to fill in numbers (remove point as can handle decimals)
        elif not length_numeric.replace(".", "").isnumeric():
            messagebox.showerror("Wrong input", "Please enter a valid number") 
            #Return that values were not valid
            return False
        else:
            #Return that values were valid
            return True
        
        
    #Create inputs for length (used for wheels and axle)
    def make_length_inputs(self, two):
        #Create frame to place inputs into
        self.length_frame = CTkFrame(self.frame, fg_color="transparent")
        self.length_frame.place(relx=0.5, rely=0.6, anchor=CENTER)
        #Input view for first length with units
        CTkLabel(self.length_frame, text="Length:", font=self.paragraph_font).pack(side=LEFT)
        self.length_input = CTkTextbox(self.length_frame, height=40, width=60, font=self.paragraph_font)
        self.length_input.pack(side=LEFT, padx=2)
        CTkLabel(self.length_frame, text="mm", font=self.paragraph_font).pack(side=LEFT)
        #If second input required
        if two:
            #Spacer
            CTkLabel(self.length_frame, fg_color="transparent",width=40, text="").pack(side=LEFT)
            #Input view for second length
            CTkLabel(self.length_frame, text="Length2:", font=self.paragraph_font).pack(side=LEFT)
            self.length_input2 = CTkTextbox(self.length_frame, height=40, width=60, font=self.paragraph_font)
            self.length_input2.pack(side=LEFT, padx=2)
            CTkLabel(self.length_frame, text="mm", font=self.paragraph_font).pack(side=LEFT)
    
    #BACKLASH
    
    #Begin the process of calibrating the backlash
    def calibrate_backlash(self):
        #Create UI with title and explanation
        self.basic_layout("Backlash")
        #Show abstract turtle image
        CTkLabel(self.bottom_frame, image=self.turtle_image, text="").place(relx=0.5, rely=0.5, anchor=CENTER)
        #Make start button to start backlash process
        self.make_button(self.frame, "Start", self.check_backlash_main)
        
        
    #Create the UI for the user to enter whether the turtlebot moves or not when testing the backlash
    def check_backlash_main(self):
        #Create UI with title and explanation
        self.basic_layout("Backlash In Progress")
        
        #Create label showing current backlash value being tested
        self.backlash_label = CTkLabel(self.bottom_frame, text="0", font=("Roboto", 14, "bold"))
        self.backlash_label.place(anchor=CENTER, relx= 0.5, rely=0.5)
        CTkLabel(self.bottom_frame, text="steps").place(anchor=CENTER, relx= 0.7, rely=0.5)
        
        #Create back button to restart backlash calibration process in case of user error
        self.back_button = CTkButton(self.frame, text="Restart", command=self.check_backlash_main, state=DISABLED, width=20)
        self.back_button.place(relx=0.87, rely=0.01)
        
        #Create buttons for the user to enter whether the turtlebot moves or not and at accordingly
        self.button_frame = CTkFrame(self.frame, fg_color="transparent")
        self.button_frame.place(rely=0.8, anchor=CENTER, relx=0.5)
        CTkButton(self.button_frame, text="No difference", command=self.backend_magic.backlash_forward).pack(side=LEFT)
        CTkButton(self.button_frame, text="Moved", command=self.backend_magic.backlash_moved).pack(side=LEFT, pady=3, padx=3)
        #Start the process
        self.backend_magic.backlash_start(self.calibrate_wheel_diameter, self.backlash_label.configure, lambda: self.back_button.configure(state=NORMAL))
       
     
    #WHEEL DIAMETER
       
    #Create the UI for the user to calibrate the wheel diameters
    def calibrate_wheel_diameter(self):
        #Create UI with title and explanation
        self.basic_layout("Wheels")
        #Create button to draw line
        self.draw_diameter_button(True)
        
        
    #Create the button to draw the line to calibrate the diameter
    def draw_diameter_button(self, first=False):
        #Destroy frame in way
        self.bottom_frame.destroy()
        #Add image of what the turtlebot will do
        self.image_label = CTkLabel(self.frame, image=self.diameter_image, text="")
        self.image_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        #If the first time drawing the line have the button say Draw
        if first:
            button_text="Draw"
        #Else remove the button and have text say Redraw (to acknowledge that the process is not starting from the beginning)
        else:
            self.wheel_draw_button.destroy()
            button_text="Redraw"
        #Create the button to draw the line
        self.wheel_draw_button = self.make_button(self.frame, button_text, self.draw_for_diameter)
      
        
    #Create the UI for the user to use once the line have been drawn and draw the line
    def draw_for_diameter(self):
        #Clear previous image
        for w in self.image_label.winfo_children():
            w.destroy()
        self.image_label.destroy()
        #Wheel diameter simple calibration test 
        self.backend_magic.draw_for_diameter()
        
        #Clear length input area
        self.bottom_frame = CTkFrame(self.frame, fg_color="transparent")
        self.bottom_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
        #Make an input textbox to enter the length drawn and button to move to next stage
        self.make_length_inputs(two=False)
        
        self.wheel_draw_button.configure(text="Next", command=self.diameter_length_check)
        
        
    #Check the length against the expecteed value and caibrate if necessary
    def diameter_length_check(self):
        #Get length
        length = self.length_input.get("0.0",END)  
        #If valid numerical value is given                       
        if self.validate_input(length):  
            #If the length was correct move onto calibrating the axle length
            if float(length) == 300:
                self.calibrate_axle_length()
            #Otherwise, calculate new values and create draw button
            else:
                self.wheel_draw_button.configure(text= "Adjusting")   #need to show user someting has happened based on their input
                self.backend_magic.calculate_wheel_diameter(length)
                self.draw_diameter_button()
        
        
    #AXLE LENGTH 
        
    #Create initial UI for calibrating the axle length
    def calibrate_axle_length(self):
        #Create UI with title and explanation
        self.basic_layout("Axle")
        #Set the axle image
        self.set_axle_image()
        #Create button to draw the two axle circles
        self.axle_button = self.make_button(self.frame, "Draw", self.draw_for_axle)
        
    #Set axle image depending on if on first view or second   
    def set_axle_image(self):
        #Destroy current images
        for w in self.bottom_frame.winfo_children():
            for wc in w.winfo_children():
                wc.destroy()
            w.destroy()
            
        #If on first view show image with full expected turtlebot path
        if self.axle_image_first:
            CTkLabel(self.bottom_frame, image=self.axle_images[0], text="").pack()
            self.axle_image_first = False
        #Otherwise show gap/overlap instructions and images
        else:
            CTkLabel(self.bottom_frame, text="If a gap is formed, \nwrite the number as a negative", font=("Roboto", 13)).pack(side=LEFT,padx=5)
            CTkLabel(self.bottom_frame, image=self.axle_images[1], text="").pack(side=LEFT,padx=20)
            CTkLabel(self.bottom_frame, image=self.axle_images[2], text="").pack(side=LEFT, padx=20)
            self.axle_image_first = True


    #Create the UI for the user to use once the two circles have been drawn
    def draw_for_axle(self):
        #Calibrate axle length using one wheel per circle 
        self.backend_magic.draw_for_axle()
        #Show images for guidance
        self.set_axle_image()
        #Create inputs for the user to put in the gap/overlap values
        self.make_length_inputs(two=True)
        self.axle_button.configure(text="Done", command=self.calculate_axle_length)


    #Calculate the axle length based on two inputs given
    def calculate_axle_length(self):
        #Get length
        length = self.length_input.get("0.0",END)
        #Get length2
        length2 = self.length_input2.get("0.0",END)
        #Check inputs are valid numbers
        if self.validate_input(length) and self.validate_input(length2):
            #Send to see if axle length correct or needs changing
            calibrated = self.backend_magic.calculate_axle_length(length, length2)
            #If correct show that the setup wizard is complete
            if calibrated:
                self.basic_layout("Complete")
                #Wait a moment before trying to save
                sleep(1)
                #Save the settings values
                self.backend_magic.save()
            #If not yet correct change UI to allow the user to redraw the axle circles with the newly calculated values
            else:
                self.set_axle_image()
                self.axle_button.configure(text= "Redraw", command=self.draw_for_axle)
                self.length_frame.destroy()