c.statusInfo = "Groovy's here:"
mm = new File('/home/romilly/git/active/freemap/data/test1.mm').toURL()
map = c.newMap(mm)
Thread.sleep(1000)
//c.export(map, new File('/home/romilly/git/active/freemap/data/test1.svg'), 'Scalable Vector Graphic (SVG) (.svg)',
//true)
c.export(map, new File('/home/romilly/git/active/freemap/data/test1.png'), 'Portable Network Graphic (PNG) (.png)',true)

