from ctypes import *
from structure import *

'''
According to ctype documentation,  ctypes exports cdll, on Windows windll 
and oledll objects, for loading DLLs(dynamic link libraries)    
'''
kernel32 = windll.kernel32

class debugger():
	def __init__(self):
		self.h_process = None
		self.pid = None
		self.debugger_active = False
	
	def load(self, path_to_exe):
		'''
		dwCreation flag determines how to create the process
		'''
		
		create_flags = DEBUG_PROCESS
		#calling structres
		startup_info = STARTUPINFO()
		process_information = PROCESS_INFORMATION()
		
		# Start the process showing as a separate window.
		startup_info.dwFlags = 0x1
		process_information.wShowWindow = 0x0
		
		# Initialize cb variable in the STARTUPINFO structure
		startup_info.c = sizeof(startup_info)
		
		if kernel32.CreateProcessA(path_to_exe,
									None,
									None,
									None,
									None,
									creation_flags,
									None,
									None, 
									byref(startup_info),
									byref(process_information)):
										
										print("We have successfully launched the process.")
										print("[*] PID: {} ", process_information.dwProcessId)
										
										# Get a handle to the newly creted process
										# and store it fot future access
										self.h_process = self.open_process(process_information.dwProcessId)
		else:
			print("[*] Error 0x%08x." % (kernel32.GetLastError()))
	def open_process(self, pid):
		h_process = kerne32.OpenProcess(PROCESS_INFORMATION,pid,False)
		return h_process
	def attach(self, pid):
	# Trying to attach to the process
	# If fails, raise an error
	if kernel32.DebugActiveProcess(pid):
		self.debugger_active = True
		self.pid = int(pid)
		self.run()
	else:
		raise ValueError("[*] Error to attach to the process")
	
	def run(self):
		# Loop to poll debuggee for debugging events
		while self.debugger_active == True:
			self.get_debug_event()
		
	def get_debug_event(self):
		debug_event = DEBUG_EVENT()
		continue_status = DBG_CONTINUE
		
		if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
			raw_input("Press a key to continue...")
			self.debugger_active = False
			kernel32.ContinueDebugEvent( \
				debug_event.dwProcessId, \
				debug_event.dwThreadId, \
				continue_status)
	
	def detach(self):
		if kernel32.DebugActiveProcessStop(self.pid):
			print("[*] End up debugging. Exiting....")
			return True
		else:
			raise ValueError("There was an error")
			return False
		
