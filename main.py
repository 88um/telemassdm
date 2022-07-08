import os, random, time
from telethon.sync import TelegramClient
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from telethon.errors.rpcerrorlist import *




def check_files(phone : str) -> str:
    global groups #yea
    groups = []
    if not os.path.exists(phone):os.mkdir(phone)
    files = os.listdir(phone)

    if (phone+'.txt') not in files:
        with open(f'{phone}/{phone}.txt', 'w') as f:
            f.write('Enter your message here')


    if not os.path.exists('group_list.txt'):
        with open('group_list.txt', 'w') as f:
            f.write('@group_usename')


    with open(f'{phone}/{phone}.txt','r') as fr:
        message = fr.read()

    
    with open('group_list.txt', 'r',encoding='utf-8') as f:
        groupz = f.read().splitlines()
        for item in groupz:
            item =item.replace("@","").replace(" ","").replace("✔️","")
            groups.append(item)

    
    if os.path.exists(f"{phone}.session"):
            os.replace(f"{phone}.session", f"{phone}/{phone}.session")
    if os.path.exists(f"{phone}.session-journal"):
            os.replace(f"{phone}.session-journal", f"{phone}/{phone}.session-journal")
    
    return phone, message


def remove_group(group : str):
        try:groups.remove(group)
        except:pass
        with open("group_list.txt","r",encoding='utf-8') as f:lines=f.read().splitlines()
        with open("group_list.txt","w",encoding="utf-8") as f:
            for line in lines:
                if line!=group:
                    f.write(f"{line}\n")


def msg_groups(client : TelegramClient, message : str):
    phone = client.session.filename.split("/")[0]
    for group in groups:
        try:
            client.send_message(entity=group,message=message)
            print(f"\r[{phone}] Sent message -> {group}",end='')
        except (ChatWriteForbiddenError,ChatAdminRequiredError):
            client(LeaveChannelRequest(group))
            remove_group(group)
        except SlowModeWaitError:
            print(f"\r[{phone}] Slow mode for  -> {group}",end='')
            #groups.append(group)
    print(f"\r[{phone}] All markets have been messaged! Sleeping 1-2 hours...")
    time.sleep(random.randint(3600,7200))


def join_groups(client : TelegramClient):
    phone = client.session.filename.split("/")[0]
    current_groups = [str(dialog.id) for dialog in client.iter_dialogs()]
    for group in groups:
        try:
            chat_id= "-100"+str(client.get_entity(group).__getattribute__("id"))
            if chat_id in current_groups:continue
            client(JoinChannelRequest(group))
            print(f'\r[{phone}] Joined -> "{group} sleep 5 min"',end='')
            time.sleep(300)
        except ValueError as e:
            remove_group(group)
        except FloodWaitError:
            print(f"\r[{phone}] Blocked from joining groups...sleep 30 minutes")
            time.sleep(1800)
    print(f"\r[{phone}] All markets have been joined!")

        
def login(phone : str) -> TelegramClient:
    if os.path.exists(f"{phone}/{phone}.session"):
        session = f"{phone}/{phone}.session"
        client = TelegramClient(session, API_ID, API_HASH)
    else:
        client = TelegramClient(phone, API_ID, API_HASH)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        client.sign_in(phone, input('[+] Enter the code: '))
    return client

def main():
    os.system("cls")
    phone = input("[+] Enter Phone Number: ")
    login(phone).disconnect()
    phone, message = check_files(phone)
    input(f"\nCurrent message for {phone}: {message}\nYou can change the message in {phone}.txt. Press ENTER when ready...")
    print(f"[{phone}] Starting to join all groups...")
    client = login(phone) # login by session with moved files
    phone, message = check_files(phone)
    join_groups(client)
    while True:
        phone, message = check_files(phone)
        msg_groups(client,message)


if __name__ == "__main__":
    API_ID = 1370903  
    API_HASH = '23c73e7bb6075cd2c909ca51decd7460' 
    main()

