# Script to generate CNC code for cutting  PCB boards.Only support straight (not curved) segments and 90 degrees angles only !!

import argparse

parser = argparse.ArgumentParser(description='Create CNC commands for cutting polygons in PCB boards')
parser.add_argument('points',type=float, nargs='+',
                    help='X0 Y0 ... Xn Yn describing the polygon')

args = parser.parse_args()

#Checking for even number of points (pairs!)
if (len(args.points) % 2) != 0: parser.error("Invalid number of points")

#Checking for at least 3 pair  of points
if (len(args.points) < 6) != 0: parser.error("Needs at least 3 pairs of points ")

#Creating segment list
tmpslist=args.points.copy()
tmpslist.append(tmpslist[0]);
tmpslist.append(tmpslist[1]);

segmentlist = []

i = 0
while i < (len(args.points)/2):
	segmentlist.append(tmpslist[(i*2):4+(i*2)])
	i = i + 1

print("Number of points:",len(args.points))
print("List of points:",args.points)
print("Segment list:")
length = len(segmentlist)
i = 0
  
while i < length:
    print("S",i+1,":",segmentlist[i])
    i += 1
#print("Segmentlist:",segmentlist)




