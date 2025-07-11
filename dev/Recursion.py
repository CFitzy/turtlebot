# -*- coding: utf-8 -*-
"""
Created on Wed Jul  9 15:02:20 2025

@author: cmf6
"""
import re

line = "turtle(y)"
variables = {"x":"1", "y": "x+x"}



def get(line):

    split_line = re.split(r'[()\"+]+', line)

    #for length of line look  for and substite any variables
    for i in range (1, len(split_line)):
        #remove spaces
        split_line[i] = split_line[i].replace(" ","")
        print(split_line)
        if split_line[i] in variables:
            print("2, replace", split_line[i], variables.get(split_line[i]))
            second_half = line[len(split_line[0]):]
            print(second_half)
            line = line[:len(split_line[0])] + recurse_line(second_half)
            print("replace", line)
    return line
                
def recurse_line(line):
    split_line = re.split(r'[()\"+]+', line)

    #for length of line look  for and substite any variables
    for i in range (1, len(split_line)):
        print(split_line)
        if split_line[i] in variables:
            print("2, replace", split_line[i], variables.get(split_line[i]))
            line = recurse_line(line.replace(split_line[i], variables.get(split_line[i])))
            print("replace", line)
            
    return line

line = get(line)
print(line)