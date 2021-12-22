# project journal for freemap

## Monday 20 December 2021

Restarting after a long, long gap with a new approach.

Like the code in my planning map generator, this will now operate directly on an `etree` representation of 
the map.

I've kept existing code under `freemap/archive` but I expect to get rid of or greatly modify all except the uuid and 
timestamp code.

## Exploring automated testting

I've got jython scripts working, and can run an init script so long as it doesn't access node which is not available at 
`init` time.

I need to find a way of closing freeplane from within a script
.
