# -*- coding: utf-8 -*-
"""
Created on Thu May 29 13:36:54 2025
Makes UI screen so can type in python, press button to run (display on console) and display error messages on app
@author: cmf6
"""
import customtkinter as ctk
import tkinter as tk
import turtle_simulation as ts
import code_input
import top_menu
import code_handler
import port_manager
import connection_state


class Main():
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
        # make window
        root = ctk.CTk()
        # specify window size
        self.width, self.height=800,600
        root.geometry(str(self.width)+"x"+str(self.height))
        root.title("Turtlebot")
        #set logo image
        root.iconbitmap('./graphics/turtle_logo.ico', default='./graphics/turtle_logo.ico')
        

        

        
        
        top_frame = ctk.CTkFrame(root, fg_color="#007D02", corner_radius=0)
        top_frame.pack(side=ctk.TOP, fill=ctk.X)
        connection_states = connection_state.Connection_Show()
        connection_layout = connection_states.make_connection_layout(top_frame)
        self.port_manager = port_manager.port_manager(connection_states)
        self.code_handler = code_handler.Code_Handler(self.port_manager)
        
        self.code_input = code_input.Code_Input(root, self.clear_text)
        
        self.top_menu = top_menu.Top_Menu(root, 
                                          self.port_manager, 
                                          top_frame,connection_layout, 
                                          self.code_input.change_textsize,
                                          self.code_input.set_code,
                                          self.code_input.get_code
                                          )
         
        #self.code_input = code_input.Code_Input(root, self.clear_text)
        
        self.right_frame= ctk.CTkFrame(root, fg_color="transparent")
        self.right_frame.pack(side=ctk.LEFT, fill=ctk.Y)
        
                
        
        self.turtle_view = ts.Turtle_Simulation(self.right_frame)
        self.button_frame= ctk.CTkFrame(self.right_frame, fg_color="transparent")
        self.button_frame.pack(side=ctk.TOP)
        
        self.run_button = self.button_setup(self.button_frame, "Run", self.run_text, "normal")
        self.stop_button = self.button_setup(self.button_frame, "Stop", self.stop, "disabled")
        self.buttons_layout(True)
        
        
        #shows output errors on label
        #self.text_output = ctk.CTkLabel(master=self.right_frame, text="Error Output here", width=500, wraplength=200, height = 100)
        self.text_output = ctk.CTkTextbox(self.right_frame, width=300, corner_radius=0, state="disabled")
        self.text_output.pack(pady=5)  
        
        #Binding the resizing event
        root.bind("<Configure>", lambda event: self.update_window(root, event)) 
        
        #when window destroyed close port and destroy window
        root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(root))
        
        #start window
        root.mainloop()
        
    def on_closing(self, root):
        self.port_manager.close_port()
        root.destroy()
        
        
    def button_setup(self, frame, text, command, state):
        return ctk.CTkButton(frame, text=text, command=command, width=50, fg_color="#00b335", text_color="white", hover_color="#007300", state=state)

        
    #update window to meet current size requirements (for user experience the window is recommeded not to be smaller than (600,450))
    def update_window(self, root, event=None):
        self.code_input.resize(root.winfo_width()/2, root.winfo_height())
        self.turtle_view.resize(root.winfo_width()/2, root.winfo_height()/2)
        self.text_output.configure(width=root.winfo_width()/2, height=root.winfo_height()/2.5)
            
        if root.winfo_width()<670:
            self.buttons_layout(horizontal=False)
        else:
            self.buttons_layout(horizontal=True)
            

        
    def buttons_layout(self, horizontal):
        if horizontal:
            #self.reset_button.pack(side=ctk.LEFT, padx=4)
            self.run_button.pack(side=ctk.LEFT, padx=4)
            self.stop_button.pack(side=ctk.BOTTOM, padx=4)
        else:
            #self.reset_button.pack(side=ctk.TOP, pady=4)
            self.run_button.pack(side=ctk.TOP, pady=4)
            self.stop_button.pack(side=ctk.TOP, pady=4)

        
    def clear_text(self):
        result = tk.messagebox.askquestion("Clear confirmation", "Are you sure you want to clear the program", )
        if result=="yes":
            self.code_input.clear()
            self.text_output.configure(state="normal")
            self.text_output.delete(1.0, ctk.END)
            self.text_output.configure(state="disabled")
            self.turtle_view.reset()


    def run_text(self):
        #disable to stop spamming of run button
        self.run_button.configure(state="disabled", text="Running")
        #disable to stop resetting mid program
        #self.reset_button.configure(state="disabled")
        #enable stop button
        self.stop_button.configure(state="normal")
        
        self.code_handler.handle_code(self.code_input.get_code(), self.turtle_view, self.text_output)
        
        #reenable run button
        self.run_button.configure(state="normal", text="Run")
        #reenable reset button
        #self.reset_button.configure(state="normal")
        #disable stop button
        self.stop_button.configure(state="disabled")
        
        

    def stop(self):
        #hide turtle
        self.turtle_view.stop_turtle()
        #self.text_output.configure(text="Stopped")
        self.text_output.configure(state="normal")
        self.text_output.insert(ctk.END, text="\nStopped")
        self.text_output.configure(state="disabled")
        self.text_output.see(ctk.END)
        
        #disable stop button
        self.stop_button.configure(state="disabled")
        
        
          
if __name__=="__main__":
    Main()