import requests
import time

class Clan:
    def __init__(self, clan_json = None):
        if clan_json:
            self.name = clan_json['name']
            self.abbreviation = clan_json['abbreviation']
            self.id = clan_json['clan_id']
            self.motto = clan_json['motto']
            self.emblem = clan_json['emblems']['large']
        else:
            self.name = ''
            self.abbreviation = ''
            self.id = ''
            self.motto = ''
            self.emblem = ''

    def __repr__(self):
        return '{0} ({1}) - {2}'.format(self.name,self.abbreviation,self.id)

    @property
    def battles(self):
        battles = []
        battles_json = requests.get('https://api.worldoftanks.com/wot/globalwar/battles/?application_id=f5904c98f5c04af24820d01cbddd8a86&map_id=globalmap&clan_id={0}'.format(self.id)).json()['data'][str(self.id)]
        for battle in battles_json:
            battles.append(Battle(battle))
        return battles

class Battle:
    def __init__(self, battle_json = None):
        if battle_json:
            self.name = battle_json['provinces_i18n'][0]['name_i18n']
            self.map = battle_json['arenas'][0]['name_i18n']
            self.time = battle_json['time']
            self.started = battle_json['started']
            self.province_id = battle_json['provinces_i18n'][0]['province_id']
        else:
            self.name = ''
            self.map = ''
            self.time = ''
            self.started = ''
            self.province_id = ''

    @property
    def local_time(self):
        return time.strftime('%A %b %d, %H:%M',time.localtime(self.time))

    def __repr__(self):
        return '{0} - {1} - {2}'.format(self.name,self.map,self.local_time)

def pick_clan(search_name):
    clan_list = requests.get('https://api.worldoftanks.com/wot/clan/list/?application_id=f5904c98f5c04af24820d01cbddd8a86&search={0}'.format(search_name)).json()['data']
    clans = []
    for i in range(len(clan_list)):
        clans.append(Clan(clan_list[i]))
        print('{0} | {1}'.format(i,clans[i]))
    clan = None
    while clan == None:
        clan_num = input('Select clan from search list by number: #')
        try:
            clan_num = int(clan_num)
            clan = clans[clan_num]
        except ValueError:
            print('Not a number.')
        except IndexError:
            print('Out of range.')
    return clan

clan = pick_clan(input('Clan: '))

for battle in clan.battles:
    print(battle)

#print(a.json())
#b = a.json()
#print(b['data'])
#r = requests.get('https://api.worldoftanks.com/wot/globalwar/battles/?application_id=f5904c98f5c04af24820d01cbddd8a86&map_id=globalmap&clan_id=1000009169')
#print(r.json())