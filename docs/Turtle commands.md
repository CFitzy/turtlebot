# Turtle basics
In the folloqwing list *d* is a decimal value and *n* is an integer value.

## Turtle Commands
* l*n* - left wheel *n* steps (4096 per wheel rotation)
* r*n* - right wheel *n* steps (4096 per wheel rotation)
* f*n* - forward *n* steps (-*n* backward)
* t*n* - turn *n* steps (+ clockwise, -anticlockwise)
* F*d* - forward *d* milimeters (-mm backward)
* T*d* - turn *d* degrees (+ clockwise, -anticlockwise)
* C*d* *d*- forward parameter 1 degrees and simultaneously turn parameter 2 degrees
* a*n* - acceleration number of steps between slow and fast speed
* o - motors off
* u - pen up to max height
* d - pen down to min height
* U*d* - pen up to *d* height (0<*d*<=1, 0=u height, 1=d height). Note this does not persist after power down. Use s5 setting to set power up default.
* U - pen up to previously set height
* D*d* - pen down to d height (0<*d*<=1, 0=u height, 1=*d* height). Note this does not persist after power down. Use s6 setting to set power up default.
* D - pen down to previously set height
* =text - display text on OLED screen
* x*d* run step streaming program *d*
* K*n* set the acknowledgement counter (0 if no *n*) specified.
* save - save the current set of configs to the EEPROM
* get - return the list of configurations and their values

Note that the lower case commands f,t do not include backlash compensation and directly drive the motors. The normal commands (capital letters) do include backlash compensation (to reduce motor gear slop effects when motors change direction) if non zero compensation values are set.

## Settings

* s1*n* - set motor speed in nS per step (1000 default)
* s2*d* - set left wheel diameter in mm
* s3*d* - set right wheel diameter in mm
* s4*d* - set wheel spacing (axle length) in mm
* s5*d* - set default 'U' command pen up position (0.1 - 1.0)
* s6*d* - set default 'D' connamd pen down position (0.0 - 1.0)
* s7*i* - set left wheel backlash (in motor steps)
* s8*i* - set right wheel backlash (in motor steps)

###Permanent settings are

Settings values s2 - s8 are stored in EEPROM and are permanent after power cycling. They are removed after firmware update however.

#Java code

the following only applied to the  application which intercepts these commands to perform special functions for the turtle. e.g. loading/creating a file that is then used to send the commands to the turtle.


## File commands 

### send commands (ie. not step mode)

* tc filename - send command file to turtle 
* tcsvg filename - send lines and turns to turtle 

### stream steps (ie. wheel steps)
* svg filename - stream file as lines and arc'd beziers
* svgl filename - stream as lines and turns (segmented beziers)
* svga filename - stream steps only arcs (except moves)


## Settings only for the java svg code 
These are not part of the Turtle firmware, but are intercepted by the Java terminal application to set values used in the wheel step streaming protocol intended for drawing very complex curve based designs.

* j3*n* - set STEP\_DIFF for extra steps if L/R diff
* j4*n* - set EXTRA\_STEPS steps to add if STEP\_DIFF occurs

## EEPROM
* get - applies EEPROM settings and sends to the serial interface
* save - saves the current settings to the EEPROM so they will be restored on power up. This is designed for initial configuration of a new turtle or after mechanical changes. Should not be needed for 'everyday' use. ge5 

# Java code notes
The `CommandMaker` class main method creates the svg output for wheel paths (as a visualisation)

The Turtle class main method is the entry point for the terminal based Turtle controller

After updating the Turtle firmware issue a `tc cfg` command to transfer configs to the turtle and save in EEPROM. 

The `svg` command series streams motor step commands to the turtle. The configurations are irrelevant here except for the `motorSpeedFast` which must match the java`Turtle.STEP_TIME`. The Java code the generates the pattern must therefore have the correct wheel and axle lengths, as well as any backlash required. This is all done in the PatternMaker class using `stepsLinesAndCurveArcs` and related methods to convert an svg file to steps. 

Since the PatternMaker needs the correct config for the turtle to be used it is run from `CommandMaker.main` which loads cfgJ.txt and then generates steps and visualisations for the input svg file.