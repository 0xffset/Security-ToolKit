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
		self.h_thread = None
		self.context = None
		self.exception = None
		self.exception_address = None
		self.breakpoints = {}



	def read_process_memory(self, address, length):
		data = ""
		read_buf = create_string_buffer(length)
		count = c_ulong()

		if not kerne32.readProcessMemory(self.h_process, address,read_buf, length, byref(count)):
			return False
		else:
			data += read_buf.raw
			return data
	def write_process_memory(self, address, data):
		count = c_ulong(0)
		length = len(data)
		if not kerne32.WriteProcessMenory(self.h_process, address, c_data, length, byref)):
			return False
		else:
			return True
	def bp_set(self, address):
		if not self.breakpoints.has_key(address)
		try:
			# Storage the original byte
			original_byte = self.read_process_memory(address, 1)
			# write the INT3 opcode
			self.write_process_memory(address, "\xCC")
			# register the breakpoint in out internal internal list
			self.breakpoint[address] = (address, original_byte)
		except:
			return False
		return True


	def open_thread(self, thread_id):
		h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, Nonem thread_id)
		if h_thread is not None:
			return h_thread
		else:
			print("[*] Not obtain a valid thread handle")
			return False

	def enumerate_threads(self):
		thread_entry = THREADENTRY()
		thread_list = []
		snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHEREAD, self.pid)

		if snapshot is not None:
			# Set the size of the struct
			# or the call will fail
			thread_entry.dwSize = sizeof(thread_entry)
			success = kernel32.Thread32First(snapshot, byref(thread_entry))

			while success:
				if thread_entry.th32OwnerProcessID == self.pid:
					thread_list.append(thread_entry.th32ThreadID)
					success = kernel32.Thread32Next(snapshot, byref(thread_entry))
				kernel32.CloseHandle(snapshot)
				return thread_list
		else:
			return False

	def get_thread_context(self, thread_id):
		context = CONTEXT()
		context.ContextFlags = CONTEXT_FULL | CONTEXT_DEGUG_REGISTERS


		# Get a handle to thread
		h_thread = self.open_thread(thread_id)
		if kernel32.GetThreadContext(h_thread, byref(context)):
			kernel32.CloseHandle(h_thread)
			return Context
		else:
			return False


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
			# Get the thread and the context information
			self.h_thread = self.open_thread(debug_event.dwThreadId)
			self.context = self.get_thread_context(self.h_thread)
			print("Event Code %d Thread ID: %d" % (debug_event.dwDebugEventCode, debug_event.dwThreadId))

			# If the event code is an exception, is needed to
			# examine it

			if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
				# Get the exception code
				exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
				self.exception_address = debug_event.u.ExceptionRecord.ExceptionAddress

			if exception == EXCEPTION_ACCESS_VIOLATION:
				print("Access Violation Detected")
			# If a breakpoint
			elif exception == EXCEPTION_BREAKPOINT:
				 continue_status = self.exception_handle_breakpoint()

			elif ec == EXCEPTION_SINGLE_STEP:
				print("Single Stepping")

			kernel32.ContinueDebugEvent(
				debug_event.dwProcessId,
				debug_event.dwThreadId,
				continue_status)
	def exception_handle_breakpoint():
		print("[*] Inside the breakpoint handler")
		print("[Exception Address: 0x%08x " % (self.exception_adress))
		return DBG_CONTINE

	def detach(self):
		if kernel32.DebugActiveProcessStop(self.pid):
			print("[*] End up debugging. Exiting....")
			return True
		else:
			raise ValueError("There was an error")
			return False
