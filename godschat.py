import json
from random import choice
from time import sleep

from simpleaichat import AIChat as ai

from godsdata import allgods


# in the .env file is OPENAI_API_KEY=jfdlblahblahblahyourkeyjndgf23 
with open(".env", 'r') as key:
    for line in key.readlines():
        if 'OPENAI_API_KEY' in line:
            openapi_key = line.split('OPENAI_API_KEY=').pop().strip()



Heart = True 



def clr(lines=99):
    print("\n" * lines)
    

def bye():
    global Heart
    print('''
    <q>uit
    <n>ew session
     ''')
    if 'q' in input('? ').lower():
        Heart = False


def logwork():
    try:
        with open('log.txt', 'r') as logger:
            loglist = logger.readlines()
    except:
        print('no saved log')
        return menu

    print('''
    <b>rowse for god
    <e>nter god
    ''')

    if 'e' in input('? ').lower():
        findgod = input("make god log of who? ")

    else:
        findgod, _ = search()
        
    sessions = {}

    temp = []
    seshes = []

    for line in loglist:
        if 'START SESSION' in line:
            if temp:
                seshes.append(temp)
                temp = []

        temp.append(line)

    if temp:
        seshes.append(temp)

    for sesh in seshes:
        session = sesh[0].rstrip()
        firstline = sesh[1]
        god = firstline.split(':')[0]

        if god not in sessions:
            sessions[god] = {}

        sessions[god][session] = sesh

    goddict = sessions[findgod]

    with open(findgod+'.txt', 'w') as godlog:
        for entry in goddict:
            for line in goddict[entry]:
                godlog.writelines(line)

    print(f'log for {findgod} saved as {findgod}.txt')
    sleep(2)

    return menu


def chat(god, description):
    clr()

    temperature = round(float(
        input('Enter creativity level from 0 to 10: ')))
    
    clr()
    
    if temperature:
        temperature /= 10
    
    if temperature > 1:
        temperature = 1

    temperature = float(temperature)

    params = {"temperature": temperature}

    chatz = ai(god, description, params=params, api_key=openapi_key, console=not logging)
    if not logging:
        return chatz
    
    print('Type "quitz" to exit chat..\n\n\n')
    
    response = chatz('hi')
    pretty = f"{god}: {response}\n"
    print(pretty)

    with open('session', 'r') as session:
        i = session.readline().strip()

    with open('log.txt', 'a') as logger:
        logger.write(f'START SESSION {i}\n')
        logger.write(pretty)

    while Heart is True:
        prompt = input('YOU: ')
        response = chatz(prompt)
        pretty = f"{god}: {response}\n"
        print(pretty)

        with open('log.txt', 'a') as logger:
            logger.write(f'YOU: {prompt}\n')
            logger.write(pretty)

        if 'quitz' in prompt.lower():
            with open('log.txt', 'a') as logger:
                logger.write('\n\n')
            return bye
        
        #todo add savesession option


def updategods():
    global allgods

    try:
        with open('usergods.json', 'r') as jar:
            usergods = json.load(jar)
    except:
        usergods = {}

    allgods['usergods'] = usergods


def search():
    updategods()
    clr()

    print("Choose your character type..\n")

    categories = list(allgods.keys())

    for i, godtype in enumerate(categories):
        print(i, godtype)

    choose = input('\nEnter number: ')

    godtype = categories[int(choose)]

    print(f"\nWho is your choice of {godtype}..\n")

    civs = {}
    for i, civ in enumerate(allgods[godtype]):
        civs[i] = civ
        print(i, civ)

    civnum = int(input("\nEnter number: "))
    civ = civs[civnum]

    print(f"\nWho is your choice of character..\n")

    civgods = {}
    for i, god in enumerate(allgods[godtype][civ]):
        civgods[i] = god
        print(i, god)

    godnum = int(input("\nEnter number: "))
    god = civgods[godnum]
    description = allgods[godtype][civ][god]

    return (god, description)


def usermade():
    global allgods

    god = input('Choose your character: ')
    description = input('Give a short description or extra notes: ')

    savegod = (input('Save your character for future? (y/n) '))

    if 'n' not in savegod.lower():
        usergods = allgods['usergods']

        category = input('Enter category for your character: ')

        if category not in usergods:
            usergods[category] = {}

        usergods[category][god] = description

        with open('usergods.json', 'w') as jar:
            json.dump(usergods, jar)

        allgods['usergods'] = usergods

    return chat(god, description)


def menu():
    updategods()
    clr()
    print('c', 'choose god')
    print('r', 'random choice')
    print('u', 'unique choice')
    print('m', 'make god log')
    print('x', 'exit')

    choose = input("\nEnter a choice: ")

    if choose == 'm':
        return logwork
    
    if choose == 'x':
        return bye
    
    if choose == 'u':
        return usermade
    
    if choose == 'r':
        godtype = choice(list(allgods.keys()))
        civtype = choice(list(allgods[godtype].keys()))
        god = choice(list(allgods[godtype][civtype].keys()))
        description = allgods[godtype][civtype][god]
        return chat(god, description)
    
    return chat(*search())
    

def setup():
    global logging
    clr()

    logging = not 'n' in input(
        "save your session text? (y/n) : ").lower()

    if logging:
        try:
            with open('session', 'r') as session:
                i = session.readline().strip()
                i = int(i) + 1
            with open('session', 'w') as session:
                session.write(str(i))
        except:
            with open('session', 'w') as first:
                first.write('1')

    return menu


def intro():
    clr()
    input("""
    High! Welcome to Godchat..
    Press enter to continue..""")
    return setup


def bounce(boing):
    while Heart is True:
        try:
            boing = boing()
        except:
            boing = intro
    

if __name__ == "__main__":
    bounce(intro)
