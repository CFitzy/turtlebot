# Turtlebot application

## Description
A Python application to control a virtual turtle and a turtlebot by having a user write their own Python code.
The project consists of Python files and uses CustomTkinter and Tkinter to construct the UI elements.

## Required installs
To run the code the following installs are required which can be done via the pip install command:
* customtkinter -for the UI elements
* tkhtmlview -for the HTML about page
* pyserial -for serial library

Pillow also needs to be uninstalled

## Directory structure

### dev
This folder holds any files created for the creation of graphics or during spike work.

### docs
This folder contains the pdf version pdf version of the final report.
It also contains a user manual for using and developing the application and the possible commands that can be sent to the turtlebot.

### output
This contians the folder Turtlebot. Within this an executable version of the application that can be run. It must be kept within the Turtlebot subfolder it is found in as it relies on the directory structure within to work.

### src
This folder contains the final versions of the code. The application runs from the main.py file.
The other eleven Python fies are uses by this class.
These Python files are:
* main
* code_handler
* code_input
* connection_display
* file_handler
* information_page
* port_manager
* setup_wizard
* setup_wizard_calculator
* top_menu
* turtle_simulation
* user_turtle

This folder also contains a JSON file to define the CustomTkinter theme for the application

#### src/characters
This folder includes the text files that contain code that can be inserted into the user's program

#### src/graphics
This folder contains all the grpahics that are used by the application

#### src/html_info
This folder contains the html file (information_page.html) that contians the information about the project to the user when requested through the application. It also contains any images used by this file.