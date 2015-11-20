import sys, getopt

a = 0;	b = 1;	c = 2;

try:
	opts = getopt.getopt(sys.argv[1:], 'ha:b:c:')
except getopt.GetoptError:
	print 'test.py -a <a> -b <b> -c <c>'

print opts
