f = open("vertices.out1","wb")
for line in open("vertices.out"):
	tmps = line[:-1].split(' ')
	if (len(tmps)>2):
		tmps = tmps[1:]
		f.write(tmps[0]+" "+tmps[1]+"\n")
	else:
		f.write(tmps[0]+"\n")
f.close() 

