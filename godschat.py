from random import choice as pick
from simpleaichat import AIChat as ai
from godsdata import allgods


Heart = True


with open(".env") as key:
    openapi_key = key.readline().strip()

    
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


def chat(god, description):
    clr()
    chatz = ai(god, description, api_key=openapi_key, console=not logging)
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
            return bye


def character(chattype):
    clr()

    print(f"\nWho is your choice of {chattype}..\n")

    menu = {i: civ for i, civ in enumerate(all[chattype])}

    for i, civ in menu.items():
        print(i, civ)

    civnum = int(input("\nEnter number: "))
    civ = menu[civnum]

    print(f"\nWho is your choice of character..\n")
    civgods = {i: god for i, god in enumerate(all[chattype][civ])}
    for i, god in civgods.items():
        print(i, god)

    godnum = int(input("\nEnter number: "))
    god = civgods[godnum]
    description = all[chattype][civ][god]
    #print(f"\nOk, let's talk to {god}, {description}")

    return chat(god, description)


def menu():
    clr()
    print("Choose your character type..\n")
    categories = list(all.keys())
    choicemenu = {i: choice for i, choice in enumerate(categories)}
    for i, category in choicemenu.items():
        print(i, category)
    print('r', 'random choice')
    print('u', 'unique choice')
    print('x', 'exit')
    choose = input("\nEnter a choice: ")
    if choose == 'x':
        return bye
    
    if choose == 'r':
        chattype = pick(categories)
        print()
        civtype = pick(list(all[chattype].keys()))
        god = pick(list(all[chattype][civtype].keys()))
        description = all[chattype][civtype][god]
        return chat(god, description)

    if choose == 'u':
        god = input('Choose your character: ')
        description = input('Give a short description or extra notes: ')
        return chat(god, description)
    
    chattype = choicemenu[int(choose)]
    return character(chattype)


def setup():
    global logging
    clr()

    saving = input('Would you like to save your session text? (y/n) : ')
    logging = False if 'n' in saving.lower() else True

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