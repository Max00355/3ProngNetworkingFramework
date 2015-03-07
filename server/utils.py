import globalData
import send

"""

    These are a set of functions for making common tasks easier, such as checking if a session is valid.


"""

def checkUserLoggedIn(sessionid):
    verify = None
    for user in globalData.users: # Checks if user is valid and logged in.
        if globalData.users[user]['sessionid'] == sessionid:
            verify = globalData.users[user]['username']
            break

    return verify

def broadcastToAll(data):
    for user in globalData.users:
        send.send(data, user)

