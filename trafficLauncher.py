import sys
import getopt
import time
from os import popen
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import sendp, IP, UDP, Ether, TCP
from random import randrange
import json

config = None

def generate_source_ip():
	not_valid = config["trafficConfig"]["notValidFirstOctet"]
	first = randrange(1,256)
	while first in not_valid:
	    	first = randrange(1,256)
	ip = ".".join([str(first),str(randrange(1,256)),str(randrange(1,256)),str(randrange(1,256))])
	return ip
def generate_destination_ip():
	first = 10
	second =0; third =0;
	range_str = config["trafficConfig"]["destinationLastOctetRange"]
	range_str = str(range_str)
	start , end = range_str.split(':')
	start = int(start)
	end = int(end)
	ip = ".".join([str(first),str(second),str(third),str(randrange(start, end))])

	return ip
def simulate_network_traffic():
	iterations = config["trafficConfig"]["networkTrafficSize"]
	interface = popen('ifconfig | awk \'/eth0/ {print $1}\'').read()
	for i in range(iterations):
		packets = Ether()/IP(dst=generate_destination_ip(),src=generate_source_ip())/UDP(dport=80,sport=2)
		print(repr(packets))
		if interface != '':
			sendp(packets,iface=interface.rstrip(),inter=0.1)
		else:
			sendp(packets,inter=0.1)
def load_configurations():
	with open('config.json') as j_file:
		config = json.load(j_file)
		return config
if __name__ == '__main__':
	config = load_configurations()
	simulate_network_traffic()
