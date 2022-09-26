import sys
arguments = dict(arg.split("=") for arg in sys.argv[0])
print(arguments)