from GameState import *
from gameActions import *

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
        if '{ "transactionId":' in line:
            # split the line into the different game state messages
            list = line.split('{ "type": "GREMessageType_GameStateMessage"')
            # update game state and do stuff if bot has priority
            for message in list:

                if 'gameObjects' in message:
                    # print(message)
                    results = re.findall('{ "instanceId": [0-9]+, "grpId": [0-9]+, .+?, "zoneId": [0-9][0-9]', message)
                    print(results)
                    for card in results:

                        zone = int(re.search('"zoneId": [0-9][0-9]', card).group()[10:])
                        search = re.search("grpId.: [0-9]+", card)
                        link = "https://api.scryfall.com/cards/arena/" + search.group()[8:]
                        instance = re.search("instanceId.: [0-9]+", card)
                        response = requests.get(link).json()
                        
                        if zone == 31: # if in hand
                            print('Drew ' + response["name"])
                            gameState.drawCard(Card(response, int(instance.group()[13:])))
                        if zone == 28: # if on battlefield
                            print(response["name"] + ' on Battlefield')

                # check to see if the turn info has changed
                if 'turnInfo' in message:
                    turnInfo = re.search('"turnInfo": { .+? }', message).group()
                    print(turnInfo)
                    phase = re.search('"phase": ".+?"', turnInfo)
                    if not phase is None:
                        phase = phase.group()
                        step = re.search('"step": ".+?"', turnInfo)
                        if not step is None:
                            step = step.group()
                            step = step[9:len(step)-1]
                        turn = re.search('"activePlayer": [0-9]', turnInfo).group()[16]
                        gameState.goTo(phase[10:(len(phase)-1)], step, turn)

                        # check if bot can do stuff
                        if '"decisionPlayer": 1' in turnInfo and gameState.phase != "Phase_Beginning":
                            print('Recieved Priority')
                            if gameState.phase == 'Phase_Main1':
                                nextPlay = determineNextPlay(gameState)
                                if nextPlay is None:
                                    passPriority()
                                else:
                                    playCardInHand(gameState, log , nextPlay)
                                
                            elif gameState.phase == 'Phase_Combat' and gameState.step == 'Step_DeclareAttack' and gameState.turn == 'Self':
                                attack()
                            elif gameState.phase == 'Phase_Main2':
                                passPriority()
                            else:
                                passPriority()
                print("\n")