import re

my_str = "Hello your ip is 192.168.0.1, please keep it safe"


# Expression to match an ip address:
expression = '\b(?:\d{1,3}\.){3}\d{1,3}\b'
