import pygame
import client
import sys
import random
import thread


def message(obj):
    while True:
        message = raw_input("> ")
        obj.message(message)


screen = pygame.display.set_mode((800, 600))
networkObj = client.MMOProtocolClient("173.63.75.82", 8080, {"moving":False, "direction":"right", "stats":{"speed":5}, "username":"tes", "class":"mage", "animationon":0, "lastanimation":100, "health":100, "energy":100, "attacking":False, "object":(random.randint(50, 500), random.randint(50, 500), 32, 32), "sessionid":__import__("uuid").uuid4().hex, "password":"test"})
thread.start_new_thread(message, (networkObj,))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_DOWN:
                networkObj.packet['direction'] = "down"
            elif event.key == pygame.K_UP:
                networkObj.packet['direction'] = "up"
            elif event.key == pygame.K_LEFT:
                networkObj.packet['direction'] = "left"
            elif event.key == pygame.K_RIGHT:
                networkObj.packet['direction'] = "right"
            
            networkObj.packet['moving'] = True
            networkObj.userUpdate()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                networkObj.packet['moving'] = False
                networkObj.userUpdate()
            elif event.key == pygame.K_DOWN:
                networkObj.packet['moving'] = False
                networkObj.userUpdate()
            elif event.key == pygame.K_LEFT:
                networkObj.packet['moving'] = False
                networkObj.userUpdate()
            elif event.key == pygame.K_RIGHT:
                networkObj.packet['moving'] = False
                networkObj.userUpdate()
        
    if networkObj.packet['moving']:
        if networkObj.packet['direction'] == "left":
            networkObj.packet['object'][0] -= 5
        elif networkObj.packet['direction'] == "right":
            networkObj.packet['object'][0] += 5
        elif networkObj.packet['direction'] == "up":
            networkObj.packet['object'][1] -= 5
        elif networkObj.packet['direction'] == "down":
            networkObj.packet['object'][1] += 5
    screen.fill((255,255,255)) 
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(networkObj.packet['object'][0], networkObj.packet['object'][1], networkObj.packet['object'][2], networkObj.packet['object'][3]))
    data = networkObj.returnedData['users']
    for user in data:
        data = networkObj.returnedData['users'][user]
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(data['object'][0], data['object'][1], 32, 32))
        if data['moving']:
            if data['direction'] == "right":
                data['object'][0] += data['stats']['speed']
            elif data['direction'] == "left":
                data['object'][0] -= data['stats']['speed']
            elif data['direction'] == "down":
                data['object'][1] += data['stats']['speed']
            elif data['direction'] == "up":
                data['object'][1] -= data['stats']['speed']
    pygame.display.update()
    pygame.time.wait(60)
