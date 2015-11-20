# This function finds the area under the Normal curve 
# to the specified number of decimal points given A, B,
#  Mean, Standard Deviation, and # Decimal Points.

# It uses Riemann sums - the function automatically determines how many
# rectangles to use by trying more and more until the 
# left and right sums agree to the correct number of
# decimal places (halfup rounded), then prints that number to stdout.

# Usage: python norm_area.py  A  B  Mean  SD #DPs 
# 	 -i <init # rectangles> -s <rect # scale> -t <user alert threshold>

import sys
import math
import getopt

	# returns a list of the areas of the rectangles
def fillPointList(a, b, mean, sd, num_rects):
	areas = []
	dx = (b-a)/num_rects
	coeff = 1 / (sd * math.sqrt(2 * math.pi))
	for i in range(0,num_rects+1):
		areas.append(coeff * math.exp( -1 * math.pow(i * dx + a - mean, 2)\
		/ (2 * math.pow(sd, 2))) * dx)

	return areas





NUM_RECTS_INIT = 1	# init # rectangles: Initial number of rectangles
NUM_RECTS_SCALE = 1.15	# rect # scale: the multiplier of num_rects each iteration
ASK_THRESH = 1000000	# user alert threshold: how many rects to check in w/ user
USAGE = '\nusage: python norm_area.py  A  B  Mean  SD  #DPs  (-i <init'+\
	' # rectangles> -s <rect # scale> -t <user alert threshold>)\n'

	# handle command line options (flag arguments) for the above constants
try:
		# check to see if there's a lone -h or any combination after parameters
	opts, args = getopt.getopt(sys.argv[6:], 'hi:s:t:')
	opts2, args2 =  getopt.getopt(sys.argv[1:], 'h')
	try:
		if opts2[0][0] == '-h':
			raise getopt.GetoptError('-h flag called')

	except IndexError:
		pass

		# apply flag values to applicable constants
	for opt, arg in opts:
		if opt == '-h':
			raise getopt.GetoptError('-h flag called')

		elif opt == '-i':
			try:
				NUM_RECTS_INIT = int(arg)

			except ValueError:
				raise getopt.GetoptError('Init value not an int')

		elif opt == '-s':
			try:
				NUM_RECTS_SCALE = float(arg)

			except ValueError:
				raise getopt.GetoptError('Scale value not a float')

		elif opt == '-t':
			try:
				ASK_THRESH = int(arg)

			except ValueError:
				raise getopt.GetoptError('Thresh value not an int')

except getopt.GetoptError:	
	sys.exit(USAGE)





	# test that there are the right number of non-flag arguments
if len(sys.argv) < 6:
	sys.exit(USAGE)

	# test that the non-flag arguments are of the correct types
try:
	if float(sys.argv[1]) < float( sys.argv[2]):
		a = float(sys.argv[1])
		b = float(sys.argv[2])

	else:
		a = float(sys.argv[2])
		b = float(sys.argv[1])

	mean = float(sys.argv[3])
	sd = float(sys.argv[4])
	dec_pts = int(sys.argv[5]);
except ValueError:
	sys.exit(USAGE)





	# calculate left and right hand sums, compare them
right = 1.1
left = 0.1		# assign values to force while loop to execute at least once
num_rects = NUM_RECTS_INIT
asked = 0
while True:
	areas = fillPointList(a, b, mean, sd, num_rects)
	right = sum(areas[1:len(areas)])
	left = sum(areas[0:len(areas)-1])
		# check in with user if num_rects grows too large
	if areas[len(areas)-1] == 0:
		sys.exit('\nUpper Limit is too large!\n')

	if len(areas) > ASK_THRESH and asked == 0:
		asked = 1

		if str(raw_input('\nI am using over ' + str(ASK_THRESH) + ' rectangles' +\
			' - continue? (y/n) ')) == 'y':
			print 'Press <CTL-C> to abort at any time.'

		else:
			print '\nCurrent data:'
			print 'Number of rectangles:', num_rects
			print 'Right-hand sum:', right
			print 'Left-hand sum: ', left, '\n'
			sys.exit()

		# break the loop if the sums match up
	if round(right, dec_pts) == round(left, dec_pts):
		break

	num_rects = int(math.ceil(num_rects * NUM_RECTS_SCALE))




		
	# output final sum
print '\nAn approximation using', num_rects, 'rectangles yields a sum of',\
	('{:.' + str(dec_pts) + 'f}').format(round(right, dec_pts)), '\n'
sys.exit()
