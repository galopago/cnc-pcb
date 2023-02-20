import argparse

parser = argparse.ArgumentParser(description='Create CNC commands for cutting polygons in PCB boards')
parser.add_argument('points',type=float, nargs='+',
                    help='X0 Y0 ... Xn Yn describing the polygon')

args = parser.parse_args()

#Checking for even number of points (pairs!)
if (len(args.points) % 2) != 0: parser.error("Invalid number of points")

#Checking for at least 3 pair  of points
if (len(args.points) < 6) != 0: parser.error("Needs at least 3 pairs of points ")

print("Number of points:",len(args.points))
print("List of points:",args.points)


