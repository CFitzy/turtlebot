# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:50:23 2025

@author: cmf6
"""
import re
import customtkinter as ctk
from time import sleep

class Code_Handler():
    def __init__(self, port_manager):
        self.code_dictionary = {
            "turtle.forward": "F",  #will need more
            "turtle.right": "T",
            "turtle.left": "T-",
            "print":"=",
            "turtle.up": "U",
            "turtle.down": "D"
            }
        self.port_manager = port_manager
        
    def handle_code(self, code_input, turtle, text_output):
        variables = {}
        lengths = []
        if len(code_input) >1:
            #text_output.configure(text="Compiling code")
            text_output.configure(state="normal")
            text_output.delete(1.0, ctk.END)
            text_output.insert(ctk.END, text="Compiling code")
            text_output.configure(state="disabled")
        try:
            #test if the code compiles (syntax errors)
            turtle.test_code(code_input, text_output)

            if not text_output.get(1.0, 1.14) == "Compiling code":
                return
            #split code into  lines
            code_lines = code_input.splitlines()
            for_loop =0
            processed_lines = []
            preprocessing_lines = []
            for line in code_lines:
                tabs = ""
                for_loop = line.count("\t")
                for i in range (for_loop):
                    tabs+="\t"
                #if line not just spaces, empty or starting with # aka a comment
                if not line.isspace() and not line=="" and not line[0]=="#":
                    print("b",line, line.strip())
                    #replace any vars
                    split_line = re.split(r'[()\"+]+', line)
                    #for length of line look  for and substite any variables
                    for i in range (1, len(split_line)):
                        #remove spaces
                        split_line[i] = split_line[i].replace(" ","")
                        if split_line[i] in variables:
                            print("2, replace", split_line[i], variables.get(split_line[i]))
                            line = line.replace(split_line[i], variables.get(split_line[i]))
                            print("replace", line)
                            
                    if line.strip()[:7]=="turtle." or line.strip()[:5]=="print":
                        line_processed = line.replace("\"", "\\\"")
                        preprocessing_lines.append(tabs+"processed_lines.append(\""+line_processed.strip()+"\")") 
                        
                        if line.strip()[:14]=="turtle.forward":
                            lengths.append(float(re.split(r'[()]+', line)[1]))
                            print(lengths)
                        

                    elif line.strip()[:4]=="for ":
                        for_loop+=1
                        preprocessing_lines.append(line)
                    elif "=" in line:
                        line = line.replace(" ","")
                        print(line)
                        variable = line.split("=")
                        variables[variable[0]] = variable[1]
                        print(variables)
                    else:
                        preprocessing_lines.append(line)
            #join the list together with newlines between each
            res = '\n'.join(preprocessing_lines)
        
            #run to get the list of instructions
            exec(res)
            
            #work out turtle drawing scale
            turtle.work_out_scale(lengths)
            
            turtlebot_lines, timings = self.translate_to_bot(processed_lines)
            current_line = 0
            turtle.run_code("turtle.up()", text_output)
            #run list on simulation
            for line in processed_lines:
                if turtle.get_paused():
                    break
                #display on output
                text_output.configure(state="normal")
                text_output.insert(ctk.END, text="\n"+line)
                text_output.configure(state="disabled")
                text_output.see(ctk.END)
                
                if turtlebot_lines:
                    if not turtlebot_lines[current_line][0] == "":
                        self.port_manager.send_command(turtlebot_lines[current_line])
                # Run code on the simulator
                turtle.run_code(line, text_output)
                if timings:
                    sleep(1*timings[current_line])
                current_line+=1
            # Lift pen and turn motors off at the                current_line+=1
            #lift pen and turn motors off at end
            self.port_manager.send_command("U"+str(self.port_manager.up))
            self.port_manager.send_command("o")
            if not turtle.get_paused():
                #display on output
                text_output.configure(state="normal")
                text_output.insert(ctk.END, text="\nCompleted Successfully")
                text_output.configure(state="disabled")
                text_output.see(ctk.END)
        except Exception as e:
            print("E:",e)
            pass
        
    def translate_to_bot(self, processed_lines):
        #assume speed 1 sec, for 45 degrress, or 20 forward. Would be improved by knowing speed
        bot_lines = []
        times = []
        pen_down=False
        if self.port_manager.allow_writing:
            for line in processed_lines:
                #split line by brackets
                split_line = re.split(r'[()\"]+', line)
                print(split_line)
                if split_line[0] in self.code_dictionary:
                    bot_equivalent = self.code_dictionary.get(split_line[0])
                    if bot_equivalent == "U":
                        #pen_down=False
                        #bot_lines.append(bot_equivalent+str(self.port_manager.up))
                        bot_lines.append(bot_equivalent)
                        times.append(0.25)
                    elif bot_equivalent == "D":
                        #pen_down=True
                        #bot_lines.append(bot_equivalent+str(self.port_manager.down))
                        bot_lines.append(bot_equivalent)
                        times.append(0.25)
                    elif "T" in bot_equivalent:
                        new_line=bot_equivalent+split_line[1]
                        #if pen_down:
                            #lines = ["U"+str(self.port_manager.up), new_line, "D"+str(self.port_manager.down)]
                            #times.append(float(split_line[1])/45+0.5)
                            #bot_lines.append(lines)
                        #else:
                        bot_lines.append(new_line)
                        times.append(float(split_line[1])/45)
                    else:
                        new_line=bot_equivalent+split_line[1]
                        #if a print to screen give a sec
                        if bot_equivalent=="=":
                            times.append(1)
                        else:
                            times.append(float(split_line[1])/35)
                        bot_lines.append(new_line)
                else:
                    bot_lines.append("")
                    times.append(0)
                print(bot_lines) 
        return bot_lines, times