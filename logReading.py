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
        # print(line)
        # check if it is a message with info
        if '"transactionId":'  in line and 'greToClientEvent' in line:
            time.sleep(1)
            lineDict = json.loads(line)
            if 'turnInfo' in line:
                messages = lineDict['greToClientEvent']['greToClientMessages']
                for message in messages:
                    if 'gameStateMessage' in message:
                        if message['gameStateMessage']['update'] == 'GameStateUpdate_SendAndRecord':
                            turnInfo = message['gameStateMessage']['turnInfo']
                            if 'phase' in turnInfo:
                                phase = turnInfo['phase']
                                step = None
                                if 'step' in turnInfo:
                                    step = turnInfo['step']
                                turn = turnInfo['activePlayer']
                                gameState.goTo(phase, step, turn)
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
                time.sleep(0.5)
                print('Received priority')
                # find next play and play it i f nothing on stack
                search = re.search('"gameObjects": [.+?"zoneId": 27.+?]', line)
                # if (gameState.step == 'Step_Upkeep'):
                #     print(line)
                stackEmpty = search == None
                print(gameState.phase, stackEmpty, gameState.turn)
                if gameState.phase == 'Phase_Main1' and stackEmpty and gameState.turn == 'Self':
                    nextPlay = determineNextPlay(gameState)
                    if nextPlay is None:
                        space()
                    else:
                        playCardInHand(gameState, log, nextPlay)
                    time.sleep(0.5)
                else:
                    print('Not main phase space')
                    space()
           
            elif 'GREMessageType_PayCostsReq' in line:
                print('Cost space')
                space()
            elif 'GREMessageType_DeclareAttackersReq' in line:
                space()
                time.sleep(0.2)
                space()

            elif 'GREMessageType_DeclareBlockersReq' in line:
                space()

            elif 'GREMessageType_OrderCombatDamageReq' in line:
                space()

            print('Next line\n')
            
            