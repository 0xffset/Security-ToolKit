from ctypes import *
msvcrt = cdll.msvcrt
# Give the debbuger time to attach, then hiy a button 
raw_input("Once debugger is attached, press enter") 

# Create the 5-byte destination buffer
buffer = c_char_p("AAAAA")

# The overflow string
overflow = "A" * 100

#Run overflow
msvcrt.strcpy(buffer, overflow)
