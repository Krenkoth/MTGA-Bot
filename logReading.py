from GameState import *
from gameActions import *
import requests

def follow(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if line is None or not line:
            yield None
            continue
        yield line



def analyzeLine(gameState, log, line):
    if not line is None:
        # check if it is a message with info
        if '"transactionId":' in line:
            if 'turnInfo' in line: 
                turnInfo = re.search('"turnInfo": { .+? }', line).group()
                phase = re.search('"phase": ".+?"', turnInfo)
                if not phase is None:
                    phase = phase.group()
                    step = re.search('"step": ".+?"', turnInfo)
                    if not step is None:
                        step = step.group()
                        step = step[9:len(step)-1]
                    turn = re.search('"activePlayer": [0-9]', turnInfo).group()[16]
                    gameState.goTo(phase[10:(len(phase)-1)], step, turn)
            if 'gameObjects' in line: 
                    # print(message)
                    results = re.findall('{ "instanceId": [0-9]+, "grpId": [0-9]+, .+?, "zoneId": [0-9][0-9]', line)
                    # print(results)
                    for card in results:
                        zone = int(re.search('"zoneId": [0-9][0-9]', card).group()[10:])
                        id = re.search("grpId.: [0-9]+", card).group()[8:]
                        # print(id)
                        response = getCard(id)

                        instance = re.search("instanceId.: [0-9]+", card)
                        if zone == 31: # if in hand
                            print('Drew ' + response["name"])
                            gameState.drawCard(Card(response, int(instance.group()[13:])))
                        if zone == 28: # if on battlefield
                            if response["object"] != "error":
                                print(response["name"] + ' on Battlefield')
                        
            if 'GREMessageType_ActionsAvailableReq' in line:
                print('Received priority')
                # find next play and play it i f nothing on stack
                search = re.search('"gameObjects": [.+?"zoneId": 27.+?]', line)
                if (gameState.step == 'Step_Upkeep'):
                    print(line)
                stackEmpty = search == None
                print(gameState.phase, stackEmpty, gameState.turn)
                if gameState.phase == 'Phase_Main1' and stackEmpty and gameState.turn == '1':
                    nextPlay = determineNextPlay(gameState)
                    playCardInHand(gameState, log, nextPlay)
                else:
                    if gameState.step == 'Step_Upkeep' and gameState.turn == '1':
                        gameState.upkeepSkipped = not gameState.upkeepSkipped
                    if gameState.upkeepSkipped:
                        print('space')
                        space()
            elif 'GREMessageType_PayCostsReq' in line:
                space()
            
            