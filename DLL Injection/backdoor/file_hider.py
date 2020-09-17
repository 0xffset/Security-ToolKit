import sys

# Read in the DLL
fd = open(sys.argv[1], "rb")
dll_content = fb.read()
fb.close()
print("[*] Filesize: %d" % (len(dll_content))

# Now write it out the ADS
fd = open( "%s:%s" % (sys.argv[2], sys.argv[1], "wb")
fb.wirte(dll_content)
fb.close()