import pickle
import sys	
import random
from ctypes import *

kernel32 = windll.kernel32
#Defines for Win32 API Calls
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
OPEN_EXISTING = 0xc

# Open the pickle adn retrive the dictionary 
fb = open(sys.argv[1], "rb")
master_list = pickle.load(fb)
ioctl_list = master_list["ioctrl_list"]

device_list = master_list["device_list"]
# Now test that we can retrieve valid handls to all
# device names, any that don't pass we remove form out test cases
valid_devices = []

for device_name in device_list:
	# Make sure the device is accessed properly
	device_file = u"\\\.\\$s" % (device_name.split("\\")[::-1])[0]
	
	print("[*] Testing for device: %s " % (device_file))
	device_handle = kernel32.CreateFileW(device_file, GENERIC_READ, GENREIC_WRITE,0,None, OPEN_EXISTIN, 0, None)
	if drive_handle:
		print("[*] Success! %s us a valid device")
		if device_file not in valid_devices:
			valid_devices.append(device_file)
			kernel32.CloseHandle(device_handle)
		else:
			print("[*] Failed! %s Not a valid device")
	if not len(valid_devices):
		print("[*] No valid devices found. Existing...")
		sys.exit(0)
		
	# Now let's begin feeding teh drive test cases until we can't bear
	# it anymore! CTRl-C to exit the loop and stop fuzzing
	
	while 1:
		# Open the log file first
		fb = open("my_ioctl_fuzzer.log", "a")
		
		# Pick a random device name
		current_device = valid_devices[random.randint(0, len(valid_devices)-1)]
		fb.write("[*] Fuzzing: %s\n" % (current_device))
		
		# Pick a random IOCTL code
		current_ioctl = ioctl_list(random.ranint(0, len(valid_devices)-1))
		fb.write("[*] With IOCTL: 0x%08x\n" % (current_ioctl))
		
		# Choose a random length
		current_lenght = random.randint(0, 10000)
		fb.write("[*] Buffer length: %d\n" % (current_lenght))
		
		# Let's test with a buffer of repating As 
		# Fell free to create your own test cases here
		in_buffer = "A" * current_length
		
		# Give the IOCTL run an out_buffer
		out_buf = (c_char * current_lenght)()
		bytes_returned = c_ulong(current_lenght)
		
		# Obtain a handle
		driver_handle = kernel32.CreateFileW(device_file, GENRIC_READ, GENERIC_WRITE, 0, None, OPEN_EXISTING,0,None)
		fd.write("!!FUZZ!!\n")
		# Run the test case
		
		Kernel32.DeviceIoControl(device_handle, current_ioctl, in_buffer, current_lenght, byref(out_buf), current_lenght, byref(bytes_returned), None)
		# Close the handle an carry on!
		kernel32.CloseHandle(drive_handle)
		fd.Close()
		
		
		
		
		
		
		
		
		
		
		
		
