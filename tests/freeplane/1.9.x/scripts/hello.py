from time import sleep

c.statusInfo = "Jython's here:"
sleep(1)
mm = getURL('/home/romilly/git/active/freemap/data/test1.mm')
map = c.newMap(mm)
sleep(5)



