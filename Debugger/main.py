import debugger
debugger = debugger()

#debugger.load("path .exe here")
pid = raw_input("Enter the PID process program: ")
debugger.attach(int(pid))
LIST = debugger.enumerate_threads()

# For each thread grab the value of each of the registers

for thread in LIST:
	thread_context = debugger.get_thread_context(thread)
	print("[*] Dumping registers for thread ID: 0x%08x " % (thread))
	print("[**] EIP: 0x%08x " % (thread_context.Eip))
	print("[**] ESP: 0x%08x " % (thread_context.Esp))
	print("[**] EBP: 0x%08x " % (thread_context.Ebp))
	print("[**] EAX: 0x%08x " % (thread_context.Eax))
	print("[**] EBX: 0x%08x " % (thread_context.Ebx))
	print("[**] ECX: 0x%08x " % (thread_context.Ecx))
	print("[**] EDX: 0x%08x " % (thread_context.Edx))
	print("[*] END DUMP")
	debugger.detach()
	
	
	
