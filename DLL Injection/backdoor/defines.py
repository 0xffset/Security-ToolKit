from ctypes import *


''''
ctypes is a function library for Python that provide C data types
and also capabilities low-level programming in C type in pure Python code.  
'''
# Define primitive C data types. Microsoft types.

WORD = c_ushort 			# unsigned short
DWORD = c_ulong 			# unsigned long
LPBYTE = POINTER(c_ubyte) 	# usigned byte
LPTSTR = POINTER(c_char) 	# char
HANDLE = c_void_p 			#void *

# Const
DEBUG_PROCESS = 0x00000001
CREATE_NEW_CONSOLE = 0x00000010

class STARTUPINFO(Structure):
	_fields_ = [
		("cb", DWORD),
		("lpReserved", LPTSTR),
		("lpDesktop", LPTSTR),
		("lpTitle", LPTSTR),
		("dwX", DWORD),
		("dwY", DWORD),
		("dwXSize", DWORD),
		("dwYSize", DWORD),
		("dwXCountChars", DWORD),
		("dwYCountChars", DWORD),
		("dwFillAttribute", DWORD),
		("dwFlags", DWORD),
		("wShowWindow", WORD),
		("cbReserved2", WORD),
		("lpReserved2", WORD),
		("hStdInput", HANDLE),
		("hStdOutPut", HANDLE),
		("hStdError", HANDLE),
		
]

class PROCESS_INFORMATION(Structure):
	_fields_ = [
		("hProcess", HANDLE),
		("hThread", HANDLE),
		("dwProcessId", DWORD),
		("dwThreadId", DWORD),
	
	]
	
	

