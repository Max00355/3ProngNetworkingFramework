import socket
import thread
import json
import globalData
import mongo
import copy
import messaging
import send

class MMOProtocolServer:

    """
        
        This file consists of the code for managing human controlled users, as well ass the main server code and listener.


    """
        

    def __init__(self):
        self.users = globalData.users # {<connection>:<dict>}
        self.ai = globalData.ai # {<AIObject:<list of dicts of AI>}
        self.host = "0.0.0.0"
        self.port = 8080
        self.cmds = { # This is a dictionary containing all of the commands the protocol understands. 
            
                "userUpdate":self.userUpdate,
                "getUsers":self.getUsers,
                "message":messaging.message,
                "whisper":messaging.whisper,
        }
    def main(self):
        sock = socket.socket()
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.host, self.port))
        sock.listen(5)
        for ai in self.ai:
            thread.start_new_thread(ai, ())
        while True:
            obj,conn = sock.accept()
            thread.start_new_thread(self.handle, (obj, conn))


    def handle(self, obj, conn):
        data = obj.recv(102400)
        data = json.loads(data)
        while True:
            if "password" in data and "username" in data:
                if not mongo.db.players.find_one({"username":data['username'], "password":data['password']}): # The first command sent by the client will consist of the standard packet along with a "password" field. The password field is a sha256 hashed field and is removed after this loop.
                    obj.close()
                    break
            
            try: # Sometimes there is a dictionary resize error                                                                                                                                        
                for x in self.users: # Logs out other client with the same username.
                    if self.users[x]['username'] == data['username'] or self.users[x]['sessionid'] == data['sessionid']:

                        d = self.users[x]
                        del self.users[x]
                        self.removeUser(d['username'], x)
                        x.close()

                break
            except:
                continue
        
        data.pop("password")
        self.users[obj] = data
        self.userUpdate(data)

        while True:
            try:
                data = obj.recv(102400)
            except:
                print "Either the login failed, a session/username duplicate, or something just broke. The bottom line is that the object was closed {}".format(data)
                break
            if not data:
                try:
                    d = self.users[obj]
                    del self.users[obj]
                    self.removeUser(d['username'], obj)
                    obj.close()
                except:
                    pass
                break
            
            data = data.split("\n")
            data = filter(None, data)
            for x in data:
                x = json.loads(x)
                self.cmds[x['cmd']](x['data']) # Does one command at a time to keep things safe.

    def getUsers(self, data):
        new = {}
        obj = None
        for x in self.users:
            if self.users[x]['sessionid'] == data['sessionid']:
                obj = x
            else:
                c = copy.copy(self.users[x])
                c.pop("sessionid")
                new[self.users[x]['username']] = c

        if obj:
            packet = {"type":"allUsers", "data":new}
            send.send(packet, obj)
    
    def userUpdate(self, data):
        for x in self.users:
            if self.users[x]['sessionid'] == data['sessionid']:
                continue
            try:
                toSend = copy.copy(data)
                toSend.pop("sessionid")
                send.send({"type":"users", "data":toSend}, x)
            except:
                pass

    def removeUser(self, data, obj):
        for x in self.users: 
            send.send({"type":"removeUser", "data":data}, x)     

if __name__ == "__main__":
    MMOProtocolServer().main()
                
    
