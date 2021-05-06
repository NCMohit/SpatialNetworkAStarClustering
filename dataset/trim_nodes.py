edges = open("cal.cnode","r")
actualedges = []
for edge in edges:
	actualedges.append(edge.split())

newedges = open("newcal.cnode","a")

def get_string(array):
	string = ""
	for i in array:
		string += i
		string += " "
	return string

for edge in actualedges:
	newedges.write(get_string(edge[1:])+"\n")