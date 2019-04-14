# Webb Generator
## Why I created this
I wasn't trying to code using PIC Basic so I made this instead. Named after Mr Webb.

## What is this
In tech class we needed to program an LED cube using PIC Basic and persistence of vision.
Writing code in PIC Basic was both tedious and limited so I decided to make a program that
could generate any one state ("frame") of a cube. It does this by generating PIC Basic code
that loops through each layer of the cube and turns on each layer with the requested LEDS 
individually. 

## How do I use this
The program when loaded should look a little something like this:

![alt text](https://github.com/patrickzebinghe/webb-generator/media/blank.PNG "Initial Screen")

First, set a frame time (in milliseconds) in the text box labeled Frame Time.

If you want, you can spin the cube by dragging it to get a better angle or you can click on 
the "lock" button to stop it from rotating.

Next, click the LEDs that you want on in a certain state of an animation. You can toggle them on and off by clicking
on them multiple times.

Finally, click on generate and copy/paste the generated code into a PIC Basic program. 
**Make sure to define x as a word variable at the top of the PIC Basic program!**

It should end looking like this:

![alt text](https://github.com/patrickzebinghe/webb-generator/media/on.PNG "Final Screen")


