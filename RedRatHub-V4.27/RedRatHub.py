#
# Simple Python script to send commands to the RedRatHubCmd application via a socket.
#
# Ethan Johnson, David Blight, Chris Dodge - RedRat Ltd.
#
import socket
import time


class Client():
    def __init__(self):
        self.sock = socket.socket()
        self.socketOpen = False

	#
	# Opens the socket to RedRatHubCmd.
	#
    def OpenSocket(self, ip, port):
        self.sock.connect((ip, port))
        self.socketOpen = True

	#
	# Closes the RedRatHubCmd socket.
	#
    def CloseSocket(self):
        if self.socketOpen:
            self.sock.close()
            self.socketOpen = False
        else:
            print("Socket failed to close.")

	#
	# Sends a message to the ReadData() function
	#
    def SendMessage(self, message):
        self.ReadData(message)


	#
	# Reads data back from RedRatHub.
	#
    def ReadData(self, message):
        if not self.socketOpen:
            print("\tSocket has not been opened. Call 'OpenSocket()' first.")
            exit
            
        # Send message
        self.sock.send((message + '\n').encode())
        received = ""
		
        # Check response. This is either a single line, e.g. "OK\n", or a multi-line response with 
        # '{' and '}' start/end delimiters.
        while True:
            # Receives data
            received += self.sock.recv(64).decode()
            if self.CheckEOM(received):
                return received

                
    #
	# Checks for the end of a message
	#
    def CheckEOM(self, message):
        # Multi-line message
        if ('{' in message):
            return ('}' in message)
        
        # Single line message
        if ("\n" in message):
            return True
            
