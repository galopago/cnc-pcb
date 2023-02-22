# CNC EDGE CUT

## Script to generate CNC code for cutting PCB boards. Only supports straight (not curved) segments and angles of 0, 90, 180, and 270 degrees are allowed! Supporting tabs are allowed, but only one per segment in the middle.

The required parameters are a point list (with at least 3 pairs) and an output file. All other parameters have default values.

Example:

To mill a rectangle with coordinates X,Y of the upper left (-10.0, 20.0), upper right (10.0, 20.0), lower right (-20.0, 10.0), and lower left (-20.0, -10.0), use a tab size of 1.5 mm and a milling bit diameter of 1 mm. Add tabs in segments 2 and 4, and store the CNC commands in the out.nc file.

~~~
python3 cncedgecut.py  --tbs 1.5 --mbd 1 --tbl 2 4 --dfi out.nc --pts -10.0 20.0 10.0 20.0 10.0 -20.0 -10.0 -20.0 -10.0 20.0
~~~


usage: cncedgecut.py [-h] --pts PTS [PTS ...] --dfi DFI [--mbd MBD] [--mbs MBS] [--mms MMS] [--sps SPS]
                     [--tbs TBS] [--pct PCT] [--tbl TBL [TBL ...]]

Create CNC commands for cutting polygons in PCB boards

optional arguments:
  -h, --help           show this help message and exit
  --pts PTS [PTS ...]  X0 Y0 ... Xn Yn points describing the polygon, clockwise order, approximately centered at
                       X=0,Y=0
  --dfi DFI            dest file with CNC commands
  --mbd MBD            Milling bit diameter in mm
  --mbs MBS            Milling bit step in mm
  --mms MMS            Milling movement speed
  --sps SPS            Spindle rotation speed
  --tbs TBS            Tab size in mm
  --pct PCT            PCB thickness in mm
  --tbl TBL [TBL ...]  List of segments where tabs wil be placed
