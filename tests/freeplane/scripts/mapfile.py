import os

current_nodes = {}

for n in node.getMap().getRoot().getChildren():
    current_nodes[n.getLink().getText()] = n

file_loc = str(node.map.getFile())
directory, _ = os.path.split(file_loc)
for pdf in os.listdir(directory):
    _, name = os.path.split(pdf)
    if not name.endswith('.pdf') or name in current_nodes:
        continue
    new_node = node.createChild(name)
    new_node.getLink().setText(pdf)


