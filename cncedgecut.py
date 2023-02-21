# Script to generate CNC code for cutting  PCB boards.Only support straight (not curved) segments and 90 degrees angles only !!
# supporting tabs allowed!

import argparse

#default values for optional paameters
mbd_default = 1.0		# Milling bit diameter in mm (to make corrections!)
mbs_default = 0.25		# Milling bit step in mm
tbs_default = 1.0		# Tab size in mm
tbl_num_default = 4		# Max number of tabs
pct_default = 1.6		# PCB Thickness


parser = argparse.ArgumentParser(description='Create CNC commands for cutting polygons in PCB boards')

parser.add_argument('points',type=float, nargs='+',
                    help='X0 Y0 ... Xn Yn describing the polygon, clockwise order, approximately centered at X=0,Y=0')

parser.add_argument('--mbd',type=float,default=mbd_default,
                    help='Milling bit diameter in mm')

parser.add_argument('--mbs',type=float,default=mbs_default,
                    help='Milling bit step in mm')

parser.add_argument('--tbs',type=float,default=tbs_default,
                    help='Tab size in mm')

parser.add_argument('--pct',type=float,default=pct_default,
                    help='PCB thickness in mm')

parser.add_argument('--tbl',type=int,nargs=4,
                    help='List of segments where tabs wil be placed')

args = parser.parse_args()
#funcs defs
def drb_correction(point,mbitdi):
	if point < 0:
		point = point - (mbitdi/2)
	else:
		point = point + (mbitdi/2)	
	return point
	
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
print("PCB thickness:       ",args.pct)
print("Number of points:    ",len(args.points))
print("Tab segment list:    ",args.tbl)
print("List of points:",args.points)
print("Segment list:")
seglistlength = len(segmentlist)
i = 0
  
while i < seglistlength:
	print(f"S{i+1}:{segmentlist[i]}")
	i += 1

#Startup code milling speed
print(f"G21 G90 G94")	
print(f"F250")	
print(f"G1 Z1")	
print(f"M3")
print(f"S1000")
print(f"G1 Z1")	

#processing segments
zmill = 0.0;
zstep = args.mbs
pcbtick = args.pct
mbitdia = args.mbd
segstbl = args.tbl

while zmill < pcbtick:
	#print(f"zmill:{zmill}")
	i = 0
	while i < seglistlength:
		#print(f"S{i+1}:{segmentlist[i]}")

		#Drilling bit corrections only valid for 0,90,180, 270 degree segments !!!
		xa=drb_correction(segmentlist[i][0],mbitdia)
		ya=drb_correction(segmentlist[i][1],mbitdia)
			
		xb=drb_correction(segmentlist[i][2],mbitdia)
		yb=drb_correction(segmentlist[i][3],mbitdia)
		
		
		# searchig for a tab in this segment
		if (i+1) in segstbl:
			print(F"The segment {i+1} have a tab")
			# calculating tabs
    
			# Tab in horizontal line
			if ya == yb:
				midx = (xa + xb) / 2.0
				print(f"G1 X{xa} Y{ya}")
				print(f"G1 Z{zmill}")
				# direction of movement
				if xa < xb:
					print(f"G1 X{midx-(mbitdia/2.0)} Y{ya}")
					print(f"G1 Z{1}")
					print(f"G1 X{midx+(mbitdia/2.0)} Y{ya}")
					print(f"G1 Z{zmill}")
					print(f"G1 X{xb} Y{yb}")
				else:
					print(f"G1 X{midx+(mbitdia/2.0)} Y{ya}")
					print(f"G1 Z{1}")
					print(f"G1 X{midx-(mbitdia/2.0)} Y{ya}")
					print(f"G1 Z{zmill}")
					print(f"G1 X{xb} Y{yb}")
			# Tab in vertical line
			if xa == xb:
				midy = (ya + yb) / 2.0
				print(f"G1 X{xa} Y{ya}")
				print(f"G1 Z{zmill}")
				# direction of movement
				if ya < yb:
					print(f"G1 X{xa} Y{midy-(mbitdia/2.0)}")
					print(f"G1 Z{1}")
					print(f"G1 X{xa} Y{midy+(mbitdia/2.0)}")
					print(f"G1 Z{zmill}")
					print(f"G1 X{xb} Y{yb}")
				else:
					print(f"G1 X{xa} Y{midy+(mbitdia/2.0)}")
					print(f"G1 Z{1}")
					print(f"G1 X{xa} Y{midy-(mbitdia/2.0)}")
					print(f"G1 Z{zmill}")
					print(f"G1 X{xb} Y{yb}")
																
		else:		    		
    		# NO tabs
			print(f"G1 X{xa} Y{ya}")
			print(f"G1 Z{zmill}")
			print(f"G1 X{xb} Y{yb}")
		i += 1	 
	zmill = zmill + zstep

#finishing going to origin and stop mill
print(f"G1 Z1")	
print(f"G1 X0 Y0")	
print(f"S0")	
print(f"M5")


	
	
