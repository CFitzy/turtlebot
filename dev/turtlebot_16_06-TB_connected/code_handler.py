# -*- coding: utf-8 -*-
"""
Created on Mon Jun 16 13:50:23 2025

@author: cmf6
"""
import re

class Code_Handler():
    def __init__(self, port_manager):
        self.code_dictionary={
            "turtle.forward": "F",  #will need more
            "turtle.right": "T",
            "turtle.left": "T-",
            "print":"=",
            "turtle.up": "U",
            "turtle.down": "D"
            }
        self.port_manager = port_manager
        
    def handle_code(self, code_input, turtle, text_output):
        text_output.configure(text="Compiling code")
        try:
            #test if code compiles
            turtle.test_code(code_input, text_output)
            if not text_output.cget("text") == "Compiling code":
                return
            #split code into  lines
            code_lines = code_input.splitlines()
            for_loop =0
            processed_lines = []
            preprocessing_lines = []
            for line in code_lines:
                tabs = ""
                for i in range (for_loop):
                    tabs+="\t"
                if line.strip()[0]=="t" or line.strip()[0]=="p":
                    line_processed = line.replace("\"", "\\\"")
                    preprocessing_lines.append(tabs+"processed_lines.append(\""+line_processed.strip()+"\")") 

                elif line.strip()[0]=="f":
                    for_loop+=1
                    preprocessing_lines.append(line)
                else:
                    preprocessing_lines.append(line)
                if code_lines.index(line)!=len(code_lines)-1:
                    if code_lines[code_lines.index(line)+1].count("\t") < for_loop:
                        for_loop = code_lines[code_lines.index(line)+1][0].count("\t")
            #join the list together with newlines between each
            res = '\n'.join(preprocessing_lines)
        
            #run to get list of instructions
            exec(res)
            
            turtlebot_lines = self.translate_to_bot(processed_lines)
            self.port_manager.send_command("D"+str(self.port_manager.down))
            current_line = 0
            #run list on simulation
            for line in processed_lines:
                if turtle.get_paused():
                    break
                text_output.configure(text=line)
                turtle.run_code(line, text_output)
                if not turtlebot_lines[current_line][0] == "":
                    print(turtlebot_lines[current_line])
                    print("T" in turtlebot_lines[current_line])
                    if "T" in turtlebot_lines[current_line][1]:
                        print("T ", len(turtlebot_lines[current_line]))
                        for mini_line in turtlebot_lines[current_line]:
                            self.port_manager.send_command(mini_line)
                    else:
                        self.port_manager.send_command(turtlebot_lines[current_line])
                current_line+=1
            #lift pen and turn motors off at end
            self.port_manager.send_command("U"+str(self.port_manager.up))
            self.port_manager.send_command("o")
            if not turtle.get_paused():
                text_output.configure(text="Completed Successfully")
        except:
            pass
        
    def translate_to_bot(self, processed_lines):
        bot_lines = []
        for line in processed_lines:
            #split line by brackets
            split_line = re.split(r'[()\"]+', line)
            print(split_line)
            if split_line[0] in self.code_dictionary:
                bot_equivalent = self.code_dictionary.get(split_line[0])
                if bot_equivalent == "U":
                    bot_lines.append(bot_equivalent+str(self.port_manager.up))
                elif bot_equivalent == "D":
                    bot_lines.append(bot_equivalent+str(self.port_manager.down))
                elif "T" in bot_equivalent:
                    new_line=bot_equivalent+split_line[1]
                    lines = ["U"+str(self.port_manager.up), new_line, "D"+str(self.port_manager.down)]
                    bot_lines.append(lines)
                else:
                    new_line=bot_equivalent+split_line[1]
                    bot_lines.append(new_line)
            else:
                bot_lines.append("")
            print(bot_lines)
        return bot_lines