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

Instead, I am exploring the use of `xdotool`.

This too has its problems, and I've also encountered problems running freeplane 1.7.2 via sub-process.

I now have a reliable way of opening and closing a freeplane session using subprocess. The next step is to automate 
the opening of maps and capturing `png` images.

Aaand it's finally working!


## Friday 31 December 2021

After a day of uncertainty I am going to continue with the current approach:

1. Map and Branches as objects.
2. a reader
3. a writer (as yet unwritten) and 

I need more reader tests and more freeplane-built maps.


## Sunday 02 January 2022

Ideally the reading and writing operations should be inverses; if you read a `.mm` file as a Map object, and then 
write it, the output file should be _the same_: certainly representing the same XML document, and ideally containing 
the identical text in the file.

## Monday 03 January 2022

The xml diffing approach to e2e (end-to-end) testing looks workable, so I am going to ignore `xdotool` and 
`appraise` for now.

At the moment, reading an xml freeplane file creates objects but does not connect the objects to the XML that 
generated them.

A freeplane map has lots of format-related XML. It's necessary, but I have no deed to interpret or modify it.

However, a Map object needs to hold it so that it can be included in the XML if the Map object is serialised.

My current plan, then, is to hold the XML corresponding to a Map within the Map object. 
The Map constructor should build the map by reading a default map file (`Mindmal.mm`)
Code that manipulates a map or its branches should make corresponding changes to the XML.
Writing a Map then reduces to serialising the internal XML.

I'll
1. create a node from an element, or create a default element if none is provided
2. hold all the attributes of the node in the element's attribute dictionary and also 
3. create node properties for the commonly accessed attributes, which will update the MODIFIED entry in the dictionary.

Some properties (markdown_text, description, note) will need to create, modify or access child elements.

## Thursday 06 January 2022

After several days I've got working tests for some map updating.

I'm trying to simplify the API for accessing and setting node text.

First step: replace getters and setters by properties.
Next step: replace `TEXT` by `LOCALIZED_TEXT` in existing test data.

It looks as if `LOCALIZED_TEXT` is now used to hold branch text instead of `TEXT`.

If branch text is created via a dialog, the freeplane holds it in a `RICH_TEXT` node.

I'm going to define the API like this:

1. If  a value is assigned to `Branch.text`,
   1. If the value is a `Markdown` object,  `TEXT` and `LOCALIZED_TEXT` will be 
      deleted if present and a `RICH_TEXT` node will be created or updated.
   2. If the value is a string, `TEXT` and any `RICH_TEXT` node will be deleted and `LOCALIZED_TEXT` will be set.
2. iF a value is obtained from `Branch.text`,
   1. Any value in `TEXT` or `LOCALIZED_TEXT` will be returned (with `LOCALIZED_TEXT` taking priority).
   2. If neither is present the contents of the `RICH_TEXT` node wil be returnsd as a Markdown object.
   3. If neither is present, and there is no `RICH_TEXT` node a ``ValueRerror` will be raised.

Node details and node notes are always held as rich text if present.

## Friday 07 January 2022

I'm going to create a RichText class instances of which can hold and interconvert markdown and html.

That will allow me to get more useful results from retrievals of text, notes and descriptions, and to set branch 
rich text.

Done. A great day's work!



