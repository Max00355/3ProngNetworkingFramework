import globalData
import send
import time
import utils

def whisper(data):
    users = globalData.users
    to = data['to']
    sessionid = data['sessionid']
    from_ = utils.checkUserLoggedIn(sessionid)
    
    if from_:
        for user in users:
            if users[user]['username'] == to:
                send.send({"type":"whisper", "data":{"from":from_, "message":data['message'], "timestamp":time.time()}}, user)
        

def message(data):
    users = globalData.users
    sessionid = data['sessionid']
    from_ = utils.checkUserLoggedIn(sessionid)
    if from_:
        for user in users:
            if users[user]['sessionid'] == sessionid:
                continue
            else:
                send.send({"type":"message", "data":{"from":from_, "message":data['message'], "timestamp":time.time()}}, user)
