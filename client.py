import socket
import json
import thread
import hashlib

class MMOProtocolClient:
    
    """

        This module handles and sorts the data received from the server and allows for it to be called by a game in an easy way.
    

    """

    def __init__(self, host, port, packet):
        requiredFields = [("moving", bool), 
                ("direction", str), 
                ("stats", dict), 
                ("sessionid", str), 
                ("username", str), 
                ("class", str), 
                ("animationon", int), 
                ("lastanimation", float), 
                ("health", int), 
                ("energy", int), 
                ("attacking", bool), 
                ("object", list), 
                ("password", str)]
        
        for x in requiredFields:
            if x[0] not in packet:
                print x
                print "Invalid or malformed packet, try again."
                return
            packet[x[0]] = x[1](packet[x[0]]) # Casts everything to correct data type
        
        packet['password'] = hashlib.sha256(packet['password']).hexdigest()
        self.host = host
        self.port = port
        self.sock = socket.socket()
        self.sock.connect((self.host, self.port))
        self.packet = packet
        self.returnedData = {"users":{}} # <username>:<data>
        self.send(packet) # The login packet
        self.getUsers()
        thread.start_new_thread(self.recv, ())

    def userUpdate(self):
        self.send({"cmd":"userUpdate", "data":self.packet})


    def send(self, packet):
        self.sock.send(json.dumps(packet)+"\n")

    def getUsers(self):
        self.send({"cmd":"getUsers", "data":self.packet})

    def close(self):
        self.send({"cmd":"close", "data":self.packet})
        self.sock.close()
    
    def whisper(self, message, to):
        self.send({"cmd":"whisper", "data":{"to":to, "message":message, "sessionid":self.packet['sessionid']}})

    def message(self, message):
        self.send({"cmd":"message", "data":{"message":message, "sessionid":self.packet['sessionid']}})
    
    def recv(self):
        out = ""
        while True:
            while "\n" not in out:
                data = self.sock.recv(1024)
                out += data
            try:
                data = json.loads(out)
            except:
                print "Malformed packet {} ignoring".format(data)
                out = ""
                continue
            
            # This is where all of the commands are being processed and dealt with.
            
            if data['type'] == "users":
                self.returnedData['users'][data['data']['username']] = data['data']
            elif data['type'] == "removeUser":
                del self.returnedData['users'][data['data']]
            elif data['type'] == "allUsers":
                self.returnedData['users'] = data['data']
            elif data['type'] == "message" or data['type'] == "whisper":
                self.returnedData['messages'] = data['data'] # {"from":<from>, "type":<message type>, "message":<test>}
            out = ""

