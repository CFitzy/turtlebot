# -*- coding: utf-8 -*-
"""
Created on Mon Aug 18 13:54:37 2025
Class to handle setup wizard backend. Calculates settings based on drawings that it gets the turtlebot to make
@author: cmf6
"""
from re import split
from time import sleep
from math import pi

class Setup_Wizard_Calculations():
    def __init__(self, port_manager):
        #Define number of steps in a wheel's rotation
        self.circle_steps = 4096
        #Save instance of Port Manager to variable
        self.port_manager = port_manager
        #Turtlebot settings
        self.settings = {}
        
    #Get the settigns currently saved in the EEPROM  
    #Expected layout: 'wheelL 53.18\r\nwheelR 53.18\r\nAxle 79.04\r\nPenU  0.40\r\nPenD  0.30\r\nBacklashL 0\r\nBacklashR 0\r\n'
    def get_settings(self):
        #If the turtlebot is not connected return that settings can not be retrieved
        if not self.port_manager.turtle_connection:
            return False
        #Otherwise get
        else:
            #Get the current EEPROM settings
            settings = self.port_manager.get_settings()
            #If no current settings, save current ones then load
            if settings[:7] == "Invalid":
                self.port_manager.send_command("save")
                self.port_manager.get_settings()
            #Put settings string into a list, splitting up by a space or return character
            split_settings = split(r'[ \r\n]+', settings)
            #Stick all the settings into a dictionary, every two in list represent a key-value pair
            for i in range(0, (len(split_settings)-1), 2):
                self.settings[split_settings[i]] = split_settings[i+1]
            #Return that settings have been retrieved successfully
            return True
     
    #BACKLASH   
     
    #Begin the backlash calibration process and define its variables
    def backlash_start(self, check_wheel_diameter, configure_backlash_label, activate_back_button):  
        #Function to move onto the wheel diameter calibrations
        self.check_wheel_diameter = check_wheel_diameter
        #Function to change the backlash label which displays the current backlash value
        self.configure_backlash_label = configure_backlash_label
        #Function to activate the back button so the backlash process can be restarted
        self.activate_back_button = activate_back_button
        #Minimum backlash value (in steps)
        self.min = 0
        #Maximum backlash value (in steps)
        self.max =625
        #Current backlash value (in steps)
        self.current = 0 
        #Value currently being moved forwards by per increment (in steps)
        self.increment = 125
        # Slow down and set current backlash to zero
        self.port_manager.send_command("s1 4000")  
        self.port_manager.send_command("s7 0")
        self.port_manager.send_command("s8 0")   
        #Move turtlebot backwards
        self.port_manager.send_command("f -"+str(self.max))
        #Move turtlebot forwards
        self.backlash_forward()
        
    #Move the turtlebot forward for finding its backlash  
    def backlash_forward(self):  
        #Increase the current moved forward value
        self.current = round(self.current+self.increment)
        #If reached the maximum value move onto next calibration
        if self.current>=self.max:
            self.end_backlash()
        #Otherwise, move forward by an increment and change value label to match
        else:
            self.port_manager.send_command("f "+str(self.current))       #f lowercase
            self.configure_backlash_label(text=self.current)
            
    #If the turtlebot moved handle finishing backlash or further calibration increments
    def backlash_moved(self):
        #Get new minimum backlash value
        self.min = self.current-self.increment
        #Decrease increment by a factor of 5
        self.increment = round((self.increment/5),1)
        #If done first set of increments make back button availableto restart the backlash process   
        if self.increment <125:
            self.activate_back_button
        #If increment is less than one move onto next calibration (f is measured in steps which are integers)
        if self.increment<1:
            self.end_backlash()
        #Otherwise restart the backwards then move incrementally process
        else:
            #Move back
            self.port_manager.send_command("f -"+str(self.current))
            #Set values to current maximum and currently moved value
            self.max = self.current
            self.current = self.min
            self.configure_backlash_label(text=self.min)
            #Sleep for 1 sec so the reverse -> forward is noticeable
            sleep(1)
            #Move forward
            self.backlash_forward()
       
    #Finish backlash operations and move on
    def end_backlash(self):
        #Turn motors off and speed up
        self.port_manager.send_command("o")
        self.port_manager.send_command("s1 1100")   
        #Set values for backlash
        self.settings.update({"BacklashL": self.max})
        self.settings.update({"BacklashR": self.max})
        #Move onto checking the wheel diameters
        self.check_wheel_diameter()
      
    #WHEEL DIAMETERS
    
    #Draw a line using the turtlebot that should be 300mm long
    def draw_for_diameter(self):
        #Wheel Diameter simple calibration test 
        #Slow down
        self.port_manager.send_command("s1 4000")
        #Take up backlash by moving forward a 1cm
        self.port_manager.send_command("F 10")
        #Lower pen
        self.port_manager.send_command("D")
        #Move forward 30cm
        self.port_manager.send_command("F300")
        #Lift pen
        self.port_manager.send_command("U")
        # Reset motor speed and turn motors off
        self.port_manager.send_command("s1 1100")
        self.port_manager.send_command("o")
        
    #Calculate wheel diametera based upon the length of the line drawn and the the expected length   
    def calculate_wheel_diameter(self, length):
        #Get expected wheel diameter
        expected_diameter = self.settings.get("wheelL")
        #Actual diameter = percentage of expected line drawn*expected diameter
        #Round as turtlebot uses doubles so has a floating point threshold
        actual_diameter = round((float(length)/300)*float(expected_diameter), 6)
        #Set values for wheel diameters
        self.port_manager.send_command("s2 "+str(actual_diameter))
        self.port_manager.send_command("s3 "+str(actual_diameter))
        self.settings.update({"wheelL": actual_diameter})
        self.settings.update({"wheelR": actual_diameter})

    #AXLE LENGTH
    
    #Draw two circles to calibrate axle length using one wheel per circle, if the wheel is calibrated any error will be due to the wheel spacing    
    def draw_for_axle(self):
        #Slow down
        self.port_manager.send_command("s1 3000")
        #Lift pen in case down
        self.port_manager.send_command("U")
        #Take up backlash in left wheel
        self.port_manager.send_command("l 200")
        #Put pen down
        self.port_manager.send_command("D")

        #Draw circle with a radius of the axle length using the left wheel
        #Turn for a circle: ((2*axle)/wheel diameter)*steps for rotation
        self.port_manager.send_command("l "+str(round((((2*float(self.settings.get("Axle")))/float(self.settings.get("wheelL")))*4096))))
        
        #Lift pen and move away
        self.port_manager.send_command("U")
        self.port_manager.send_command("F 30")
        #Take up backlash in right wheel
        self.port_manager.send_command("r 200")

        #Draw circle with a radius of the axle length using the right wheel
        self.port_manager.send_command("D")
        self.port_manager.send_command("r "+str(round((((2*float(self.settings.get("Axle")))/float(self.settings.get("wheelR")))*4096))))
        #Lift pen and move away
        self.port_manager.send_command("U")
        self.port_manager.send_command("F 30")
        #Turn off motors and set the speed back to normal
        self.port_manager.send_command("s1 1100")
        self.port_manager.send_command("o")
        
    #Calculate axle length based upon the overlap or gap given and the the expected axle length
    def calculate_axle_length(self, length, length2, axle_button):
        #If all zeros then axle was correct so move to saving
        if float(length) == 0 and float(length2) == 0:
            #Save the settings values
            self.save()
            #Return that the value matched
            return True
        #Adjust axle length
        else:
            #Get average of two inputs
            avg_len = (float(length)+float(length2))/2
            #Get expected wheel diameter
            expected_axle = float(self.settings.get("Axle"))

            #Calculate the actual axle length
            #Use positive numbers for overlap and negative for gap
            #Expected*(Circumference of circle with axle as diameter - overlap)/Circumference of circle with axle as diameter
            #axle*(((axle*pi)-overlap)/(axle*pi))      
            #Simplifies to axle-(overlap/pi)
            actual_axle = round(expected_axle-(avg_len/(pi)), 6)   

            #Update values for axle
            self.settings.update({"Axle": actual_axle})
            self.port_manager.send_command("s4 "+str(actual_axle))
            #Return that the value did not match
            return False
            
    #SAVE
    
    #Save settings to the turtlebot's EEPROM
    def save(self):
        #Send wheel diameter configurations
        self.port_manager.send_command("s2 "+str(self.settings.get("wheelL")))
        self.port_manager.send_command("s3 "+str(self.settings.get("wheelR")))
        #Send axle length configuration
        self.port_manager.send_command("s4 "+str(self.settings.get("Axle")))
        #Send backlash configurations
        self.port_manager.send_command("s7 "+str(self.settings.get("BacklashL")))
        self.port_manager.send_command("s8 "+str(self.settings.get("BacklashR")))               
        #Save the configurations to the EEPROM
        self.port_manager.send_command("save")