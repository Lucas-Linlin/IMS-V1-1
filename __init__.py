#!python3

TIPS_INFO = '''Item Management System V1.5.0
Made by zhilin.tang@qq.com'''

from pathlib import Path
import json
import os
import bcrypt

rootPath = Path(__file__).parent
things = {}
'''
def hash_password(password: str) -> bytes:
    # 将密码转换为字节类型
    password_bytes = password.encode('utf-8')
    # 生成盐并哈希密码
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password

def check_password(password: str, hashed_password: bytes) -> bool:
    # 将密码转换为字节类型
    password_bytes = password.encode('utf-8')
    # 验证密码
    return bcrypt.checkpw(password_bytes, hashed_password)
'''
def readInfo():
    global FILE, things, user
    with open(rootPath / f'users.json') as file:
        FILE = json.load(file)
        things = FILE[user]["things"]

def add(index, value):
    global FILE, things, user
    try:
        things[index][value] += 1
    except KeyError:
        try:
            things[index]|={value:1}
        except KeyError:
            things[index] = {value:1}
    FILE[user]["things"] = things
    with open(rootPath / f'users.json', 'w') as file:
        json.dump(FILE, file, indent=4, sort_keys=True)
    print(f'{value} added to {index}.')

def delete(index, value):
    global things, user
    if index not in things.keys():
        print(f'Index "{index}" does not exist.')
        return
    try:
        things[index][value] -= 1
        if things[index][value] == 0:
            del things[index][value]
        if len(things[index]) == 0:
            del things[index]
    except KeyError:
        print(f'{value} is not found in {index}.')
        return
    FILE[user]["things"] = things
    with open(rootPath / f'users.json', 'w') as file:
        json.dump(FILE, file, indent=4, sort_keys=True)
    print(f'{value} deleted from {index}.')

def search(value):
    global things
    found = {} # {address: count, ...}
    returnStr = ''
    for i in things.keys():
        for j in things[i].keys():
            if value.lower() in j.lower():
                found[i] = things[i][j]
                returnStr += f'At {i}: {things[i][j]}*{j}\n'
    if returnStr == '':
        print('No results.')
        return 0,''
    else:
        print(f'Found:')
        print(returnStr[:-1])
    return len(found), returnStr

def query(index):
    global things
    if index in things.keys():
        print('-'*20)
        for value in things[index].keys():
            print(f'{value}*{things[index][value]}')
        print('-'*20)
    else:
        print(f'Index "{index}" does not exist.')

def display():
    global things
    if len(things) == 0:
        print('No items.')
        return
    else:
        print('------------')
        for index in things.keys():
            print(index)
            for value in things[index].keys():
                print(f'    {value}*{things[index][value]}')
            print('------------')
        print(f'Total: {sum(sum(things[i].values()) for i in things.keys())} items in {len(things)} indexes.')

def login(usr:str, psw:str, num:int=3):
    with open(rootPath / 'users.json') as file:
        users:dict = json.loads(file.read())
    if usr in users.keys():
        if psw == users[usr]["password"]:
            global user
            user = usr
            print('Login successful.')
            return
        else:
            if num == 0:
                print('Sorry, login failed.')
                exit()
            print('Invalid username or password.')
            usr = input('Username: ')
            psw = input('Password: ')
            login(usr, psw, num-1)      
    else:
        if num == 0:
                print('Sorry, login failed.')
                exit()
        print('Invalid username or password.')
        usr = input('Username: ')
        psw = input('Password: ')
        login(usr, psw, num-1) 

def logister():
    global FILE, user
    print('Please choose [l]ogin or [r]egister or [e]xit.')
    choice = input('>>> ')
    match choice.lower():
        case 'l' | 'login':
            usr = input('Username: ')
            psw = input('Password: ')
            user = usr
            login(usr, psw)
            return
        case 'r' |'register':
            usr = input('Username: ')
            psw = input('Password: ')
            confirm_psw = input('Confirm Password: ')
            if psw!= confirm_psw:
                print('Passwords do not match.')
                logister()
            with open(rootPath / 'users.json') as file:
                FILE = json.load(file)
            if usr.lower() in (i.lower() for i in FILE.keys()):
                print('Username already exists.')
                logister()
            else:
                FILE[usr] = {"password": psw, "things": {}}
                with open(rootPath / f'users.json', 'w') as file:
                    json.dump(FILE, file, indent=4, sort_keys=True)
                print('Registration successful.')
                user = usr
                login(usr, psw)
                return
        case 'e' | 'exit':
            exit()
        case _:
            print('Invalid choice.')
            logister()

def main():
    print(TIPS_INFO)
    logister()
    readInfo()
    # Main loop
    keep_going = True
    while keep_going:
        command = input('>>> ')
        match command.lower():
            case 'add' | 'a':
                try:
                    index = input('Index: ')
                    value = input('Value: ')
                    count = int(input('Count: '))
                except:
                    print('Invalid input.')
                    continue
                else:
                    for _ in range(count):
                        add(index, value)

            case 'delete' | 'dl' | 'dlt':
                try:
                    index = input('Index: ')
                    value = input('Value: ')
                    count = int(input('Count: '))
                except:
                    print('Invalid input.')
                    continue
                else:
                    for _ in range(count):
                        delete(index, value)

            case'search' | 's'| 'sc' | 'find' | 'fd' | 'f':
                try:
                    value = input('Value: ')
                except:
                    print('Invalid input.')
                    continue
                else:
                    search(value)

            case 'query' | 'q':
                try:
                    index = input('Index: ')
                except:
                    print('Invalid input.')
                    continue
                else:
                    query(index)
            
            case 'clear' | 'cls':
                os.system('cls')

            case 'display' | 'd' | 'dis':
                display()

            case 'help' | 'h':
                print(f'''{TIPS_INFO}
==================== Commands Guide =======================
                    add, a - Add an item to an index.
           delete, dl, dlt - Delete an item from an index.
search, s, sc, find, fd, f - Search for an item.
                  query, q - Query an index.
                clear, cls - Clear the screen.
           display, d, dis - Display all items.
                   help, h - Display this help message.
                exit, quit - Exit the program.
===========================================================''')

            case 'exit' | 'quit':
                keep_going = False

            case _:
                print('Invalid command.')
                continue

if __name__ == '__main__':
    main()