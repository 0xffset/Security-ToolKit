from ctypes import *
from PyEmu import PEPyEmu
# Commandline arguments
exename = sys.argv[1]

outputfile = sys.argv[2]
# Instantiate our emulator object
emu = PEPyEmu()
if exename:
	# Load the binary into PyEmu
	if not  emu.load(exename):
		print("[!] Problem loading %s" % (exename))
		sys.exit(2)
	else:
		print("[!] Black filename specified")
		sys.exit(3)
# Set our library handlers
emu.set_library_handler("LoadLibraryA", loadlibrary)
emu.set_library_handler("GetProcAddress", getprocaddress)
emu.set_library_handler("VirtualProtect", VirtualProtect)
# Set a breakpoint at the real entry point to dump binary
emu.set_mnemonic_handler("jmp", jmp_handler)
# Execute starting from the header entry point
emu.execute(start=emu.entry_point)