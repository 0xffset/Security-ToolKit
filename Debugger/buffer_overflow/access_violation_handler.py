from ctypes import *
from pydbg import *
from pydbg.defines import *
# Utility libraries included with PyDbg
import utils
# This is our access violation handler
def chech_accessv(dbg):
	# We skip first-chance exceptions
	if dbg.dbg.u.Exception.dwFirstChance:
		return DBG_EXCEPTION_NOT_HANDLED
		
	crash_bin = utils.crash_binning.crash_binning()
	cash_bin.record__crash(dbg)
	print(crash_bin.crash_synopsis())
	
	dbg.terminate_process()
	return DBG_EXCEPTION_NOT_HANDLED
	
pid = raw_input("Enter the PID: ")
dbg = pydbg()
dbg.attach(int(pid))
dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, chech_accessv)
dbg.run()
