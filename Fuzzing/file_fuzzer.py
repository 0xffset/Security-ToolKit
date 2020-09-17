from pydbg import *
from pydbg.defines import *

import utils
import random
import sys
import struct
import threading
import os
import shutil
import time
import getopt

class file_fuzzer:

	def __init__(self, exe_path, ext, notify):
		self.exe_path = exe_path
		self.ext = ext
		self.notify_crash = notify
		self.orig_file = None
		self.mutated_file = None
		self.iteration = 0
		self.crash = None
		self.pid = None
		self.in_accessv_handler = False
		self.dbg = None
		self.running = False
		self.ready = False

		# Optional 
		self.smtpserver = 'smtp.mailgun.org'
		self.recipients = ['postmaster@sandbox13259b1718314c749a32718109743913.mailgun.org']
		self.sender = ['roggergarciadiaz.com']
		self.test_cases = ["%s%n%s%n%s%n", "\fxx", "\x00", "A"]

	def file_picker(self):
		file_list = os.listdir("examples/")
		list_length = len(file_list)
		file = file_list[random.randint(0, list_length-1)]
		print(file)
		shutil.copy("examples\\%s" % (file), "test%s" % (self.ext))

		return file

	def fuzz(self):

		while 1:
			if not self.running:
				# We first snag a file for mutation
				self.test_file = self.file_picker()
				self.mutate_file()
				

				# Start uop the debugger thread
				pydbg_thread = threading.Thread(target=self.start_debugger)
				pydbg_thread.setDaemon(0)
				pydbg_thread.start()

				while self.pid == None:
					time.sleep(1)

				# Start up the monitoring thread 
				monitor_thread = threading.Thread(target=self.monitor_debugger)
				monitor_thread.setDaemon(0)
				monitor_thread.start()

				self.iteration += 1
				
			else:
				time.sleep(1)

	# Our primary debugger thread that the application
	# runs under
	def start_debugger(self):
		print("[*] Starting debugger for iteration: %d" % (self.iteration))
		self.running = True
		self.dbg = pydbg()
		self.dbg.set_callback(EXCEPTION_ACCESS_VIOLATION, self.check_accessv)
		pid = self.dbg.load(self.exe_path, "test.%s" % (self.ext))
		self.pid = self.dbg.pid
		self.dbg.run()

	# Our access viaolation handler that traps the crash
	# information and stores it
	def check_accessv(self, dbg):
		if dbg.dbg.u.Exception.dwFirstChance:
			return DBG_CONTINUE

		print("[*] Woot! Handling an acces viaolation!")
		self.in_accessv_handler = True
		crash_bin = utils.crash_binning_crash_binning()
		crash_bin.record_crash(dbg)
		self.crash = crash_bin.crash_synopsis()

		# Now back up the files
		shutil.copy("test%s" % (self.ext, "crashes\\%d_orig%s" % (self.iterationm, self.ext)))
		self.dbg.terminate_process()
		self.in_accessv_handler = False
		self.running = False

		return DBG_EXCEPTION_NOT_HANDLED

	# This is our monitoring function that allows the application
	# to run for a few seconds and then it terminates it
	def monitor_debugger(self):
		counter = 0
		print("[*] Monitor thread for pid: %d waiting." % (self.pid))
		while counter < 3:
			time.sleep(1)
			print(counter)
			counter += 1

		if self.in_accessv_handler != True:
			time.sleep(1)
			self.dbg.terminate_process()
			self.pid = None
			self.running = False
		else:
			print("[*] The acccess viaolation handler is doing its business. Waiting.")
			while self.running:
				time.sleep(1)

	# Our emailing routine to ship out crash information
	def notify(self):
		crash_message = "From:%s\r\n\r\nTo:\r\n\r\nIteration:%d\n\nOutput:\n\n %s" % (self.sender, self.iteration, self.crash)
		session = smtplib.SMTP(smtpserver)
		session.sendmail(sender, recipients, crash_message)
		session.quit()
		return


	def mutate_file(self):
	# Pull the contents of the file into a buffer
		fd = open("test%s" % (self.ext), "rb")
		stream = fd.read()
		fd.close()

		# The fuzzing meat and potatoes, really simple
		# Take a random test case and apply it to random position
		# in the file

		test_case = self.test_cases[random.randint(0, len(self.test_cases) -1)]
		stream_length = len(stream)
		rand_offset = random.randint(0, stream_length -1)
		rand_len = random.randint(1,1000)

		# Now take the test case and repeat it
		test_case = test_case * rand_len
		# Apply it to the buffer, we are just
		# splicing in our fuzz data
		fuzz_file = stream[0:rand_offset]
		fuzz_file += str(test_case)
		fuzz_file += stream[rand_offset:]

		# Write out the file

		fd = open("test%s" % (self.ext) , "wb")
		fd.write(fuzz_file)
		fd.close()

		return

def print_usage():
	print("[*]")
	print("[*] file_fuzzer.py -e <Executable Path> -x <File Extension>")
	print("[*]")

	sys.exit(0)

if __name__ == "__main__":
	print("[*] Generic File Fuzzer.")
	# This is the path to the document parser
	# and the filename extension to use
	try:
		opts, argo = getopt.getopt(sys.argv[1:], "e:x:n")
	except getopt.GetoptError:
		print_usage()
	exe_path = None
	ext = None
	notify = False

	for o,a in opts:
		if o == "-e":
			exe_path = a
		elif o == "-x":
			ext = a
		elif o == "-n":
			notify = True

	if exe_path is not None and ext is not None:
		fuzzer = file_fuzzer(exe_path, ext, notify)
		fuzzer.fuzz()
	else:
		print_usage()

