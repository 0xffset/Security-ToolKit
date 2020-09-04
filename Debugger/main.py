import debugger
debugger = debugger()

#debugger.load("path .exe here")
pid = raw_input("Enter the PID process program: ")
debugger.attach(int(pid))
debugger.detach()

