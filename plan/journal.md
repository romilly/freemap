# project journal for freemap

## Monday 20 December 2021

Restarting after a long, long gap with a new approach.

Like the code in my planning map generator, this will now operate directly on an `etree` representation of 
the map.

I've kept existing code under `freemap/archive` but I expect to get rid of or greatly modify all except the uuid and 
timestamp code.

## Exploring automated testing

I've got jython scripts working, and can run an init script so long as it doesn't access node which is not available at 
`init` time.

I need to find a way of closing freeplane from within a script.


## Monday 27 December 2021

After lots of experimenting, I've abandoned the use of freeplane scripts for testing. I could not find a way of 
opening windows/exporting pngs from inside an `init` script, and I could not see how to automate the running of 
any other script from the command line.

Instead I am exploring the use of `xdotool`.

This too has its problems, and I've also encountered problems running freeplane 1.7.2 via sub-process.

I now have a reliable way of opening and closing a freeplane session using subprocess. The next step is to automate 
the opening of maps and capturing `png` images.

