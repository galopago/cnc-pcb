# Script to translate CNC drilling codes in absolute mode to a centered mode, usefull for small home CNC drilling

# The required parameters are a 2 point pairs with X Min, Y Min ,X Max and Y Max , input file generated from kicad drilling, and an output file.

# the file assumes that the line format is XNNNNYNNNN

import argparse

parser = argparse.ArgumentParser(description='Translate CNC absolute drillings to centered at origin midpoint (aprox) ')

parser.add_argument('--pts',type=float, nargs=4,required=True,
                    help='Xmin Ymin Xmax Ymax points describing the PCB extreme points')

parser.add_argument('--ifi',type=argparse.FileType('r'),required=True,
                    help='input file with CNC commands')

parser.add_argument('--dfi',type=argparse.FileType('w'),required=True,
                    help='dest file with CNC coordinates')


args = parser.parse_args()


#Creating input file
fdi = open(args.ifi.name, "r")

#Creating output file
fdo = open(args.dfi.name, "w")

print("Input file name:       ",args.ifi.name)
print("Destination file name: ",args.dfi.name)
print("Xmin:                  ",args.pts[0])
print("Ymin:                  ",args.pts[1])
print("Xmax:                  ",args.pts[2])
print("Ymax:                  ",args.pts[3])

xmin=args.pts[0]
xmax=args.pts[2]
ymin=args.pts[1]
ymax=args.pts[3]


incount = 0
while True:
	incount += 1
  
    # Get next line from file
	line = fdi.readline()
  
	# if line is empty
	# end of file is reached
	if not line:
		break
	if line.startswith('X') :
		linex = line[0: line.index("Y"):]
		liney = line[line.index("Y")::].strip()
		valuex = float(linex[1::])
		valuey = float(liney[1::])
		translatedx = round ( valuex - xmin - ((xmax-xmin)/2) , 2)
		translatedy = round ( valuey + ymin + ((ymax-ymin)/2) , 2)
		#print(f"valuex: {valuex} -> translatedx: {translatedx}")
		#print(f"valuey: {valuey} -> translatedy: {translatedy}")
		print(f"Line{incount}: {line.strip()} -> {translatedx} {translatedy}")
		print(f"X{translatedx} Y{translatedy}",file=fdo)	
	#print("Line{}: {}".format(incount, line.strip()))
  
#finishing going to origin and stop mill
print(f"Finished!")	
fdi.close()
fdo.close()


	
	
