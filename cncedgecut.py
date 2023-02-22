# Script to generate CNC code for cutting  PCB boards.Only support straight (not curved) segments and 0,90,180,270 degrees angles only !!
# supporting tabs allowed, only one per segment in the middle
# 
# required parameters: point list (at least 3 pairs) and output file. All other parameters have default values
#
# Example:
# Mill a rectangle with coordenates X,Y upper left -10.0 20.0 , upper right 10.0 20.0 lower right -20.0 10.0 and lower left
# tab size 1.5 mm, milling bit diameter 1 mm, tabs in segments 2 and 4 , CNC commands stores in out.nc file
#
# python3 cncedgecut.py  --tbs 1.5 --mbd 1 --tbl 2 4 --dfi out.nc --pts -10.0 20.0 10.0 20.0 10.0 -20.0 -10.0 -20.0 -10.0 20.0


import argparse

#default values for optional parameters
mbd_default = 1.0		# Milling bit diameter in mm (to make corrections!)
mbs_default = 0.25		# Milling bit step in mm
mms_default = 250		# Milling movement speed
sps_default = 1000		# Spindle speed
tbs_default = 1.0		# Tab size in mm
pct_default = 1.6		# PCB Thickness


parser = argparse.ArgumentParser(description='Create CNC commands for cutting polygons in PCB boards')

parser.add_argument('--pts',type=float, nargs='+',required=True,
                    help='X0 Y0 ... Xn Yn points describing the polygon, clockwise order, approximately centered at X=0,Y=0')

parser.add_argument('--dfi',type=argparse.FileType('w'),required=True,
                    help='dest file with CNC commands')

parser.add_argument('--mbd',type=float,default=mbd_default,
                    help='Milling bit diameter in mm')

parser.add_argument('--mbs',type=float,default=mbs_default,
                    help='Milling bit step in mm')

parser.add_argument('--mms',type=int,default=mms_default,
                    help='Milling movement speed')

parser.add_argument('--sps',type=int,default=sps_default,
                    help='Spindle rotation speed')

parser.add_argument('--tbs',type=float,default=tbs_default,
                    help='Tab size in mm')

parser.add_argument('--pct',type=float,default=pct_default,
                    help='PCB thickness in mm')

parser.add_argument('--tbl',type=int,nargs='+',
                    help='List of segments where tabs wil be placed')


args = parser.parse_args()

#funcs defs
def drb_correction(point,mbitdi):
	if point < 0:
		point = point - (mbitdi/2.0)
	else:
		point = point + (mbitdi/2.0)	
	return point




	
#Checking for even number of points (pairs!)
if (len(args.pts) % 2) != 0: parser.error("Invalid number of points")

#Checking for at least 3 pair  of points
if (len(args.pts) < 6) != 0: parser.error("Needs at least 3 pairs of points ")

#Creating output file
fd = open(args.dfi.name, "w")

#Creating segment list
tmpslist=args.pts.copy()
tmpslist.append(tmpslist[0]);
tmpslist.append(tmpslist[1]);

segmentlist = []

i = 0
while i < (len(args.pts)/2):
	segmentlist.append(tmpslist[(i*2):4+(i*2)])
	i = i + 1

print("Destination file name: ",args.dfi.name)
print("Milling bit diameter:  ",args.mbd)
print("Milling bit step:      ",args.mbs)
print("Milling movement speed:",args.mms)
print("Spindle speed:         ",args.sps)
print("Tab size:              ",args.tbs)
print("PCB thickness:         ",args.pct)
print("Number of points:      ",len(args.pts))
print("Tab segment list:      ",args.tbl)
print("List of points:        ",args.pts)
print("Segment list:")
seglistlength = len(segmentlist)
i = 0
  
while i < seglistlength:
	print(f"S{i+1}:{segmentlist[i]}")
	i += 1

#processing segments
zmill = 0.0;
zstep = args.mbs
pcbtick = args.pct
mbitdia = args.mbd
segstbl = args.tbl
spspeed = args.sps
mmspeed = args.mms
tabsize = args.tbs

#Startup code milling speed
print(f"Writting CNC commands to dest file..")	
print(f"G21 G90 G94",file=fd)	
print(f"F{mmspeed}",file=fd)	
print(f"G1 Z1",file=fd)	
print(f"M3",file=fd)
print(f"S{spspeed}",file=fd)
print(f"G1 Z1",file=fd)	


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
			print(F"Tab in segment {i+1}")
			# calculating tabs
    
			# Tab in horizontal line
			if ya == yb:
				midx = (xa + xb) / 2.0
				print(f"G1 X{xa} Y{ya}",file=fd)
				print(f"G1 Z{-1*zmill}",file=fd)
				# direction of movement
				if xa < xb:
					print(f"G1 X{midx-(tabsize/2.0)-(mbitdia/2.0)} Y{ya}",file=fd)
					print(f"G1 Z{1}",file=fd)
					print(f"G1 X{midx+(tabsize/2.0)+(mbitdia/2.0)} Y{ya}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
				else:
					print(f"G1 X{midx+(tabsize/2.0)+(mbitdia/2.0)} Y{ya}",file=fd)
					print(f"G1 Z{1}",file=fd)
					print(f"G1 X{midx-(tabsize/2.0)-(mbitdia/2.0)} Y{ya}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
			# Tab in vertical line
			if xa == xb:
				midy = (ya + yb) / 2.0
				print(f"G1 X{xa} Y{ya}",file=fd)
				print(f"G1 Z{-1*zmill}")
				# direction of movement
				if ya < yb:
					print(f"G1 X{xa} Y{midy-(tabsize/2.0)-(mbitdia/2.0)}",file=fd)
					print(f"G1 Z{1}",file=fd)
					print(f"G1 X{xa} Y{midy+(tabsize/2.0)+(mbitdia/2.0)}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
				else:
					print(f"G1 X{xa} Y{midy+(tabsize/2.0)+(mbitdia/2.0)}",file=fd)
					print(f"G1 Z{1}",file=fd)
					print(f"G1 X{xa} Y{midy-(tabsize/2.0)-(mbitdia/2.0)}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
																
		else:		    		
    		# NO tabs
			print(f"G1 X{xa} Y{ya}",file=fd)
			print(f"G1 Z{-1*zmill}",file=fd)
			print(f"G1 X{xb} Y{yb}",file=fd)
		i += 1	 
	zmill = zmill + zstep

#finishing going to origin and stop mill
print(f"G1 Z1",file=fd)	
print(f"G1 X0 Y0",file=fd)	
print(f"S0",file=fd)	
print(f"M5",file=fd)
fd.close()

	
	
