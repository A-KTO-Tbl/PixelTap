from requests import post, get
from threading import Thread, Lock
from os import system as sys
from platform import system as s_name
from time import sleep
from random import randint, choice
from colorama import Fore
from typing import Literal
from datetime import datetime, timedelta
from json import loads
from urllib.parse import unquote
from itertools import cycle

from Core.Tools.HPV_Getting_File_Paths import HPV_Get_Accounts
from Core.Tools.HPV_Proxy import HPV_Proxy_Checker
from Core.Tools.HPV_User_Agent import HPV_User_Agent

from Core.Config.HPV_Config import *







class HPV_PixelTap:
    '''
    AutoBot Ferma /// HPV
    ---------------------
    [1] - `Сбор монет`
    
    [2] - `Получение ежедневной награды`
    
    [3] - `Покупка нового робота`
    
    [4] - `Апгрейд всех роботов`
    
    [5] - `Получение кол-ва доступных спинов и запуск их прокрутки`
    
    [6] - `Активация буста, если таковые имеются`
    
    [7] - `Апгрейд уровня профиля, если доступно`
    
    [8] - `Получение ежедневного комбо (рандомные карточки)`
    
    [9] - `Ожидание от 5 до 6 часов`
    
    [10] - `Повторение действий через 5-6 часов`
    '''



    def __init__(self, Name: str, URL: str, Proxy: dict) -> None:
        INFO = self.URL_Clean(URL)
        self.Name = Name                   # Ник аккаунта
        self.TG_ID = INFO['ID']            # ID аккаунта
        self.Username = INFO['Username']   # Username аккаунта
        self.Token = INFO['Token']         # Токен аккаунта
        self.Proxy = Proxy                 # Прокси (при наличии)
        self.UA = HPV_User_Agent()         # Генерация уникального User Agent
        self.Secret = 'ad3ef94479d09aa8a7043762c487b80a8ce7a868b171a943d1a92e9b6a871837'



    def URL_Clean(self, URL: str) -> dict:
        '''Очистка ссылки'''

        try:
            ID = str(loads(unquote(unquote(unquote(URL.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))).split('&')[1].split('user=')[1])['id'])
        except:
            ID = ''

        try:
            Username = str(loads(unquote(unquote(unquote(URL.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))).split('&')[1].split('user=')[1])['username'])
        except:
            Username = ''

        try:
            Token = str(unquote(URL.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
        except:
            Token = ''
        
        return {'ID': ID, 'Username': Username, 'Token': Token}



    def Current_Time(self) -> str:
        '''Текущее время'''

        return Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'



    def Logging(self, Type: Literal['Success', 'Warning', 'Error'], Name: str, Smile: str, Text: str) -> None:
        '''Логирование'''

        with Console_Lock:
            COLOR = Fore.GREEN if Type == 'Success' else Fore.YELLOW if Type == 'Warning' else Fore.RED # Цвет текста
            DIVIDER = Fore.BLACK + ' | '   # Разделитель

            Time = self.Current_Time()     # Текущее время
            Name = Fore.MAGENTA + Name     # Ник аккаунта
            Smile = COLOR + str(Smile)     # Смайлик
            Text = COLOR + Text            # Текст лога

            print(Time + DIVIDER + Smile + DIVIDER + Text + DIVIDER + Name)



    def Get_Info(self) -> dict:
        '''Получение информации об игроке'''

        URL = 'https://api-clicker.pixelverse.xyz/api/users'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            Balance = f'{get(URL, headers=Headers, proxies=self.Proxy).json()["clicksCount"]:,.2f}' # Текущий баланс
            return {'Status': True, 'Balance': Balance}
        except:
            return {'Status': False}



    def Daily_Reward(self) -> dict:
        '''Получение ежедневной награды'''

        URL = 'https://api-clicker.pixelverse.xyz/api/daily-rewards/claim'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            Collected = post(URL, headers=Headers, proxies=self.Proxy).json()['amount']
            return {'Status': True, 'Collected': f'{Collected:,.2f}'}
        except:
            return {'Status': False}



    def Claim(self) -> None:
        '''Сбор монет'''

        URL = 'https://api-clicker.pixelverse.xyz/api/mining/claim'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()['claimedAmount']
            self.Logging('Success', self.Name, '🟢', f'Монеты собраны! +{HPV:,.2f}')
        except:
            self.Logging('Error', self.Name, '🔴', 'Монеты не собраны!')



    def Get_Pets(self) -> dict:
        '''Получение списка роботов'''

        URL = 'https://api-clicker.pixelverse.xyz/api/pets'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()['data']

            Pets = [] # Список хранящий информацию о всех роботах

            for Pet in HPV:
                Name = Pet['name'] # Имя робота
                ID = Pet['userPet']['id'] # ID робота
                LVL = Pet['userPet']['level'] # Уровень робота
                UP_Price = Pet['userPet']['levelUpPrice'] # Цена улучшения робота
                Pets.append({Name: {'ID': ID, 'LVL': LVL, 'Upgrade Price': UP_Price}})

            return {'Status': True, 'Pets': Pets}
        except:
            return {'Status': False}



    def Buy_Pet(self) -> bool:
        '''Покупка нового робота'''

        URL = 'https://api-clicker.pixelverse.xyz/api/pets/buy'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}
        Params = {'tg-id': self.TG_ID, 'secret': self.Secret}

        try:
            post(URL, params=Params, headers=Headers, json={}, proxies=self.Proxy).json()['level']
            return True
        except:
            return False



    def Upgrade_Pet(self, ID: str) -> dict:
        '''Улучшение робота'''

        URL = f'https://api-clicker.pixelverse.xyz/api/pets/user-pets/{ID}/level-up'
        Headers = {'authority': 'api-clicker.pixelverse.xyz', 'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"Windows"', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            HPV = post(URL, headers=Headers, proxies=self.Proxy).json()['level']
            return {'Status': True, 'NEW_LVL': HPV}
        except:
            return {'Status': False}



    def Get_Info_Spin(self) -> int:
        '''Получение информации о наличии спинов'''

        URL = 'https://api-clicker.pixelverse.xyz/api/roulette'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            return get(URL, headers=Headers, proxies=self.Proxy).json()['mySpinsAmount']
        except:
            return 0



    def Spin(self) -> dict:
        '''Прокрутка всех доступных спинов'''

        URL = 'https://api-clicker.pixelverse.xyz/api/roulette/spin'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            Prize = post(URL, headers=Headers, proxies=self.Proxy).json()['name'].split('.')[2]
            self.Logging('Success', self.Name, '🟢', f'Вращение произведено! Получено: {Prize}')
        except:
            self.Logging('Error', self.Name, '🔴', 'Вращение не произведено!')



    def Get_Boosts(self) -> dict:
        '''Получение списка доступных бустов'''

        URL = 'https://api-clicker.pixelverse.xyz/api/boost/my'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()[0] # Первый буст из списка доступных

            Boost_ID = HPV['id'] # ID буста
            Boost_Name = HPV['boost']['name'].split('.') # Имя буста

            return {'Status': True, 'Boost_ID': Boost_ID, 'Boost_Name': f'{Boost_Name[1]} {Boost_Name[2]}'}
        except:
            return {'Status': False}



    def Boost_Activation(self, ID: str) -> bool:
        '''Активация буста'''

        URL = f'https://api-clicker.pixelverse.xyz/api/boost/{ID}/activate'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            return False if post(URL, headers=Headers, proxies=self.Proxy).content else True
        except:
            return False



    def Check_Boost_Active(self) -> bool:
        '''Проверка на наличие активного буста'''

        URL = 'https://api-clicker.pixelverse.xyz/api/boost/my/active'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            get(URL, headers=Headers, proxies=self.Proxy).json()
            return True
        except:
            return False



    def Check_LVL_Upgrade(self) -> dict:
        '''Проверка на доступность обновить уровень'''

        URL = 'https://api-clicker.pixelverse.xyz/api/levels/my'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            HPV = get(URL, headers=Headers, proxies=self.Proxy).json()
            
            LVL = HPV['value'] # Текущий уровень
            TASK = all(TASK['completed'] for TASK in HPV['tasksToLevelup']) # Если все задания выполнены = True, иначе = False

            return {'Status': True, 'LVL': LVL, 'TASK': TASK}
        except:
            return {'Status': False}



    def LVL_Upgrade(self) -> bool:
        '''Обновление уровня'''

        URL_START = 'https://api-clicker.pixelverse.xyz/api/levels/levelup/start'
        URL_SKIP = 'https://api-clicker.pixelverse.xyz/api/levels/levelup/skip'
        URL_FINISH = 'https://api-clicker.pixelverse.xyz/api/levels/levelup/finish'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}

        try:
            post(URL_START, headers=Headers, proxies=self.Proxy)
            post(URL_SKIP, headers=Headers, proxies=self.Proxy)
            HPV = post(URL_FINISH, headers=Headers, proxies=self.Proxy).json()['message']

            return False if HPV == 'Levelup not available' else True
        except:
            return False



    def Daily_Combo(self) -> dict:
        '''Получение ежедневного комбо'''

        PETS = ['50e9e942-36d5-4f19-9bb7-c892cb956fff', '7ee9ed52-c808-4187-a942-b53d972cd399', '8074e9c5-f6c2-4012-bfa2-bcc98ceb5175', 'f097634a-c8e8-4de9-b707-575d20c5fd88', 'd364254e-f22f-4a43-9a1c-5a7c71ea9ecd', '7c3a95c6-75a3-4c62-a20e-896a21132060', '0a6306e5-cc33-401a-9664-a872e3eb2b71', '341195b4-f7d8-4b9c-a8f1-448318f32e8e', 'bc3f938f-8f4c-467b-a57d-2b40cd500f4b', 'ef0adeca-be18-4503-9e9a-d93c22bd7a6e', '90a07a32-431a-4299-be59-598180ee4a8c', 'f82a3b59-913d-4c57-8ffd-9ac954105e2d', 'e8c505ed-df93-47e0-bd2e-0e664d09ba86', '45f2e16e-fb64-4e15-a3fa-2fb99c8d4a04', '571523ae-872d-49f0-aa71-53d4a41cd810']
        URL = 'https://api-clicker.pixelverse.xyz/api/cypher-games/current'
        Headers = {'accept': 'application/json, text/plain, */*', 'accept-language': 'ru,en;q=0.9,uz;q=0.8', 'content-type': 'application/json', 'initdata': self.Token, 'origin': 'https://sexyzbot.pxlvrs.io', 'priority': 'u=1, i', 'referer': 'https://sexyzbot.pxlvrs.io/', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'cross-site', 'secret': self.Secret, 'tg-id': self.TG_ID, 'user-agent': self.UA, 'username': self.Username}
        Json = {choice(PETS): 0, choice(PETS): 1, choice(PETS): 2, choice(PETS): 3}

        try:
            GAME_ID = get(URL, headers=Headers, proxies=self.Proxy).json()['id']
            URL_GAME = f'https://api-clicker.pixelverse.xyz/api/cypher-games/{GAME_ID}/answer'
            Prize = post(URL_GAME, headers=Headers, json=Json, proxies=self.Proxy).json()['rewardAmount']

            return {'Status': True, 'Prize': f'{Prize:,}'}
        except:
            return {'Status': False}



    def Run(self):
        '''Активация бота'''

        while True:
            try:
                if self.Get_Info()['Status']:
                    self.Logging('Success', self.Name, '🟢', 'Инициализация успешна!')
                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')
                    Pets = self.Get_Pets()['Pets'] # Список роботов


                    self.Claim() # Сбор монет
                    sleep(randint(33, 103)) # Промежуточное ожидание


                    # Получение ежедневной награды
                    Daily_Reward = self.Daily_Reward()
                    if Daily_Reward['Status']:
                        self.Logging('Success', self.Name, '🎁', f'Ежедневная награда получена! +{Daily_Reward["Collected"]}')
                        sleep(randint(33, 103)) # Промежуточное ожидание


                    # Покупка нового робота, если нужное количество ещё не приобретено
                    if len(Pets) < MAX_PETS:
                        if self.Buy_Pet():
                            self.Logging('Success', self.Name, '👾', 'Приобретен новый робот')
                            sleep(randint(33, 103)) # Промежуточное ожидание


                    # Апгрейд всех роботов до максимально возможно уровня
                    Updates = {}
                    while True:
                        # Остановка цикла, если все роботы улучшены (или нет) до максимально возможно уровня
                        if all(Updates) and len(Updates) == len(Pets):
                            break

                        for Pet in Pets:
                            for Name, Conf in Pet.items():
                                # Проверка наличия достаточного баланса и уровня ниже необходимого для апгрейда
                                Balance = int(float(self.Get_Info()['Balance'].replace(',', ''))) # Баланс

                                if Conf['Upgrade Price'] <= Balance and Conf['LVL'] < MAX_LVL:
                                    Upgrade_Pet = self.Upgrade_Pet(Conf['ID'])
                                    if Upgrade_Pet['Status']:
                                        self.Logging('Success', self.Name, '🟢', f'Апгрейд {Name} успешен! Новый уровень: {Upgrade_Pet["NEW_LVL"]}')
                                        sleep(randint(33, 103)) # Промежуточное ожидание
                                    else:
                                        Updates[Name] = True
                                else:
                                    Updates[Name] = True


                    # Получение кол-ва доступных спинов и запуск их прокрутки
                    Get_Spins = self.Get_Info_Spin()
                    if Get_Spins > 0:
                        self.Logging('Success', self.Name, '🎮', f'Спинов доступно: {Get_Spins}!')
                        for _ in range(Get_Spins):
                            self.Spin()
                            sleep(randint(12, 23))

                        self.Logging('Success', self.Name, '💰', f'Баланс после спинов: {self.Get_Info()["Balance"]}')


                    # Активация буста, если таковые имеются
                    Get_Boosts = self.Get_Boosts()
                    if Get_Boosts['Status']:
                        if not self.Check_Boost_Active(): # Проверка на наличия отсутствия активных бустов
                            if self.Boost_Activation(Get_Boosts['Boost_ID']):
                                self.Logging('Success', self.Name, '⚡️', f'Буст `{Get_Boosts["Boost_Name"]}` активирован!')


                    # Апгрейд уровня профиля
                    C_LVL_U = self.Check_LVL_Upgrade()
                    if C_LVL_U['Status'] and C_LVL_U['TASK']: # Если запрос успешен и все задания выполнены
                        if self.LVL_Upgrade():
                            self.Logging('Success', self.Name, '🚀', f'Апгрейд уровня профиля успешен! Текущий уровень: {C_LVL_U["LVL"] + 1}')


                    # Получение ежедневного комбо
                    Daily_Combo = self.Daily_Combo()
                    if Daily_Combo['Status']:
                        self.Logging('Success', self.Name, '🎁', f'Ежедневное комбо выполнено! Получено: {Daily_Combo["Prize"]}')


                    Waiting = randint(18_000, 21_000) # Значение времени в секундах для ожидания
                    Waiting_STR = (datetime.now() + timedelta(seconds=Waiting)).strftime('%Y-%m-%d %H:%M:%S') # Значение времени в читаемом виде

                    self.Logging('Success', self.Name, '💰', f'Текущий баланс: {self.Get_Info()["Balance"]}')
                    self.Logging('Warning', self.Name, '⏳', f'Следующий сбор: {Waiting_STR}!')

                    sleep(Waiting) # Ожидание от 5 до 6 часов

                else: # Если аутентификация не успешна
                    self.Logging('Error', self.Name, '🔴', 'Ошибка инициализации!')
                    sleep(randint(33, 66)) # Ожидание от 33 до 66 секунд
            except:
                pass







if __name__ == '__main__':
    sys('cls') if s_name() == 'Windows' else sys('clear')

    Console_Lock = Lock()
    Proxy = HPV_Proxy_Checker()

    def Start_Thread(Account, URL, Proxy = None):
        PixelTap = HPV_PixelTap(Account, URL, Proxy)
        PixelTap.Run()

    if Proxy:
        DIVIDER = Fore.BLACK + ' | '
        Time = Fore.BLUE + f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        Text = Fore.GREEN + f'Проверка прокси окончена! Работоспособные: {len(Proxy)}'
        print(Time + DIVIDER + '🌐' + DIVIDER + Text)
        sleep(5)

    for Account, URL in HPV_Get_Accounts().items():
        if Proxy:
            Proxy = cycle(Proxy)
            Thread(target=Start_Thread, args=(Account, URL, next(Proxy),)).start()
        else:
            Thread(target=Start_Thread, args=(Account, URL,)).start()


