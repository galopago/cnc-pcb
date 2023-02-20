# Script to generate CNC code for cutting  PCB boards.Only support straight (not curved) segments and 90 degrees angles only !!
# supporting tabs allowed!

import argparse

#default values for optional paameters
mbd_default = 1.0		# Milling bit diameter in mm (to make corrections!)
mbs_default = 0.25		# Milling bit step in mm
tbs_default = 1.0		# Tab size in mm
tbl_num_default = 4		# Max number of tabs


parser = argparse.ArgumentParser(description='Create CNC commands for cutting polygons in PCB boards')

parser.add_argument('points',type=float, nargs='+',
                    help='X0 Y0 ... Xn Yn describing the polygon, clockwise order, approximately centered at X=0,Y=0')

parser.add_argument('--mbd',type=float,default=mbd_default,
                    help='Milling bit diameter in mm')

parser.add_argument('--mbs',type=float,default=mbs_default,
                    help='Milling bit step in mm')

parser.add_argument('--tbs',type=float,default=tbs_default,
                    help='Tab size in mm')

parser.add_argument('--tbl',type=int,nargs=4,
                    help='List of segments where tabs wil be placed')

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

print("Milling bit diameter:",args.mbd)
print("Milling bit step:    ",args.mbs)
print("Tab size:            ",args.tbs)
print("Number of points:    ",len(args.points))
print("Tab segment list:    ",args.tbl)
print("List of points:",args.points)
print("Segment list:")
length = len(segmentlist)
i = 0
  
while i < length:
    print("S",i+1,":",segmentlist[i])
    i += 1





