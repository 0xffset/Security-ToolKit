#!/usr/bin/python
"""
	Script to get all network-based interfaces
	connected and the same time got packets of them.
	For more information about pcapy, visit https://pypi.org/project/pcapy/

"""


import pcapy

devices = pcapy.findalldevs()
packs = pcapy.open_live("wlp1s0", 1024, False, 100)
dump = packs.dump_open("storage.pcap")
count = 1
while count:
	try:
		packs = packs.next()
	except:
		continue
	else:
		print(packs)
		count += 1
	if count == 10:
			break
