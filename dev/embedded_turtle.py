# -*- coding: utf-8 -*-
"""
Created on Thu May 29 20:20:58 2025

@author: cathr
"""
import turtle
import customtkinter as ctk
import threading

def do_stuff(turtle, colours):
 for colour in colours:
  turtle.color(colour)
  turtle.right(120)

  
def press():
 t1 = threading.Thread(target=lambda: do_stuff(alice, ["red", "yellow", "green"]))
 t1.start()
 t2 = threading.Thread(target=lambda: do_stuff(bob, ["yellow", "green", "blue"]))
 t2.start()
 
 
 
if __name__ == "__main__":
 root = ctk.CTk()
 canvas = ctk.CTkCanvas(root)
 canvas.config(width=200, height=200)
 canvas.pack(side=ctk.LEFT)
 screen = turtle.TurtleScreen(canvas)
 alice = turtle.RawTurtle(screen, shape="turtle")
 
 button = ctk.CTkButton(root, text="Press me", command=press)
 button.pack(side=ctk.LEFT)
 
 canvas2 = ctk.CTkCanvas(root)
 canvas2.config(width=200, height=200)
 canvas2.pack(side=ctk.LEFT)
 screen2 = turtle.TurtleScreen(canvas2)
 bob = turtle.RawTurtle(screen2, shape="turtle")
 bob.color("blue")
 
 
 root.mainloop()

