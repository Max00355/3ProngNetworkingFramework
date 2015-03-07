import json

def send(data, obj):
    obj.send(json.dumps(data) + "\n")
    
