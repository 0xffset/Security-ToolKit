import sys
from pydbg import *
from pydbg.defines import *
sys.path.insert(0, '..')
import structure 
import random

# callback function
def printf_randomizer(dbg):
	# Get counter value at ESP + 0x8 as d DWORD 
	param_addr = dbg.context.Esp + 0x8
	counter = dbg.read_process_memory(param_addr, 4)
	
	# read_process_memory returns a packed binary string
	# We must first unpack it before
	
	counter = structure.unpack("L",counter)[0]
	print("Counter: %d " % (int(counter)))
	
	# Generate a random number and pack it into binary format
	# so that it is written correctly back into the process
	rand_counter = rando.randint(1,100)
	rand_counter = structure.pack(param_addr, rand_counter)
	
	# Now swap in our random number and resume the process
	dbg.write_process_memory(param_addrs, rand_counter)
	
	return DBG_CONTINUE

# Start pydbg class
dbg = pydbg()

# Now enter the PID process
pid = raw_input("ENTER the PID: ")

# Attach debugger
dbg.attach(int(pid))

# Set breakpoint with printf_randomizer function
printf_address = dbg.func_resolve("msvcrt", "printf")
dbg.bp_set(printf_address, description="printf_address", handler=printf_randomizer)

# Resume process
dbg.run()
