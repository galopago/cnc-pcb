# Script to generate CNC code for drilling holes using helical pattern.


import argparse

#default values for optional parameters
mbd_default = 0.0		# Milling bit diameter in mm (to make corrections!)
mbs_default = 0.25		# Milling bit step in mm
mms_default = 250		# Milling movement speed
sps_default = 1000		# Spindle speed
tbs_default = 1.0		# Tab size in mm
tgd_default = 0.0		# Tab groove depth in mm
pct_default = 1.6		# PCB Thickness
tbn_default = 1			# Number of tabs


parser = argparse.ArgumentParser(description='Create CNC commands for cutting holes using helical pattern')

parser.add_argument('--pts',type=float, nargs='+',required=True,
                    help='X0 Y0 R0 ... Xn Yn Rn points describing center of holes and radius')

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

parser.add_argument('--tgd',type=float,default=tgd_default,
                    help='Tab groove depth in mm')

parser.add_argument('--pct',type=float,default=pct_default,
                    help='PCB thickness in mm')

parser.add_argument('--tbn',type=int,nargs=1,default=tbn_default,
                    help='Number of tabs')


args = parser.parse_args()

#funcs defs
def drb_correction(point,mbitdi):
	if point < 0:
		point = point - (mbitdi/2.0)
	else:
		point = point + (mbitdi/2.0)	
	return point




	
#Checking for even number of points (triplet!)
if (len(args.pts) % 3) != 0: parser.error("Invalid number of points")

#Creating output file
fd = open(args.dfi.name, "w")

#Creating segment list
tmpslist=args.pts.copy()

segmentlist = []

i = 0
while i < (len(args.pts)/3):
	segmentlist.append(tmpslist[(i*3):3+(i*3)])
	i = i + 1

print("Destination file name: ",args.dfi.name)
print("Milling bit diameter:  ",args.mbd)
print("Milling bit step:      ",args.mbs)
print("Milling movement speed:",args.mms)
print("Spindle speed:         ",args.sps)
print("Tab size:              ",args.tbs)
print("Tab groove depth:      ",args.tgd)
print("PCB thickness:         ",args.pct)
print("Number of points:      ",len(args.pts))
print("Number of tabs:        ",args.tbn)
print("List of points:        ",args.pts)
print("Segment list:          ",segmentlist)

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
#segstbl = args.tbl
spspeed = args.sps
mmspeed = args.mms
tabsize = args.tbs
tabgroove = args.tgd
tabnumber = args.tbn

#Startup code milling speed
print(f"Writting CNC commands to dest file..")	
print(f"G21 G90 G94",file=fd)	
print(f"F{mmspeed}",file=fd)	
print(f"G1 Z1",file=fd)	
print(f"M3",file=fd)
print(f"S{spspeed}",file=fd)
print(f"G1 Z1",file=fd)	

i = 0
while i < seglistlength:	
	print(f"Segment:{i}")
	zmill = 0.0;
	while zmill < pcbtick:
		print(f"G2 X{segmentlist[i][0]} Y{segmentlist[i][1]}")
		zmill = zmill + zstep
	i += 1	 
	
while zmill < pcbtick:
	#print(f"zmill:{zmill}")
	i = 0
	while i < seglistlength:

		

		
		# searchig for tabs						
		if tabnumber == 0 :
			print(F"No tabs in segment {i+1}")					
		else:
			print(F"Found tags in segment {i+1}")	
		
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
					if tabgroove == 0.0:
						print(f"G1 Z{1}",file=fd)
					else :
						if -1*zmill > -1*tabgroove :
							print(f"G1 Z{-1*zmill}",file=fd)
						else :
							print(f"G1 Z{-1*tabgroove}",file=fd)								
					print(f"G1 X{midx+(tabsize/2.0)+(mbitdia/2.0)} Y{ya}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
				else:
					print(f"G1 X{midx+(tabsize/2.0)+(mbitdia/2.0)} Y{ya}",file=fd)
					if tabgroove == 0.0:
						print(f"G1 Z{1}",file=fd)
					else :
						if -1*zmill > -1*tabgroove :
							print(f"G1 Z{-1*zmill}",file=fd)
						else :
							print(f"G1 Z{-1*tabgroove}",file=fd)								
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
					if tabgroove == 0.0:
						print(f"G1 Z{1}",file=fd)
					else :
						if -1*zmill > -1*tabgroove :
							print(f"G1 Z{-1*zmill}",file=fd)
						else :
							print(f"G1 Z{-1*tabgroove}",file=fd)								
					print(f"G1 X{xa} Y{midy+(tabsize/2.0)+(mbitdia/2.0)}",file=fd)
					print(f"G1 Z{-1*zmill}",file=fd)
					print(f"G1 X{xb} Y{yb}",file=fd)
				else:
					print(f"G1 X{xa} Y{midy+(tabsize/2.0)+(mbitdia/2.0)}",file=fd)
					if tabgroove == 0.0:
						print(f"G1 Z{1}",file=fd)
					else :
						if -1*zmill > -1*tabgroove :
							print(f"G1 Z{-1*zmill}",file=fd)
						else :
							print(f"G1 Z{-1*tabgroove}",file=fd)								

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
print(f"Finished!")	
fd.close()

	
	
