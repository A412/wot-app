import requests
import time
import nm

class Clan:

    error_clan = 'error_clan'

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
        return '{0} ({1})'.format(self.name,self.abbreviation)

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
            self.time = 0
            self.started = ''
            self.province_id = ''

    def init_from_province_id(self,province_id):
        province_json = requests.get('https://api.worldoftanks.com/wot/globalwar/provinces/?application_id=f5904c98f5c04af24820d01cbddd8a86&map_id=globalmap&province_id={0}'.format(province_id)).json()
        self.name = province_json['data'][str(province_id)]['province_i18n']
        self.map = province_json['data'][str(province_id)]['arena_i18n']
        self.province_id = province_json['data'][str(province_id)]['province_id']

    @property
    def local_time(self):
        return time.strftime('%A %b %d, %H:%M',time.localtime(self.time))

    def __repr__(self):
        if self.time != 0:
            return '{0} ({1}) - {2} - {3}'.format(self.name,self.province_id,self.map,self.local_time)
        return '{0} ({1}) - {2}'.format(self.name,self.province_id,self.map)

class Tournament:
    def __init__(self, province_json):
        self.matches = []
        self.battle = Battle()
        if province_json['count'] > 0:
            province_id = province_json['data'][0]['province_id']
            self.battle.init_from_province_id(province_id)
            for match in province_json['data'][0]['tournament_tree']:
                self.matches.append({'clan1':match['battles'][0]['clan1'],'clan2':match['battles'][0]['clan2']})
        self.process()

    def process(self):
        newmatches = []
        for match in self.matches:
            newdic = {}
            for clan in match:
                if type(match[clan]) != Clan:
                    newclan = id_to_clan(match[clan])
                    if newclan is not Clan.error_clan:
                        newdic.update({clan:id_to_clan(match[clan])})
            if newdic:
                newmatches.append(newdic)
        self.matches = newmatches

    def enemies(self,id):
        matches = []
        for match in self.matches:
            if 'clan1' in match:
                if match['clan1'].id == id:
                    matches.append(match['clan2'])
            if 'clan2' in match:
                if match['clan2'].id == id:
                    matches.append(match['clan1'])
        return matches

    def __repr__(self):
        mystr = self.battle.__repr__() + '\n'
        for match in self.matches:
            mystr += ((str(match['clan1']) if 'clan1' in match else '----') + ' -- ' + (str(match['clan2']) if 'clan2' in match else '----') + '\n')
        return mystr

def analyze_matches(clan,tournament):
    matches = tournament.enemies(clan.id)
    return_str = '\n' + str(tournament) + '\nEnemies:\n'
    for clan in matches:
        return_str += '\n' + str(clan.name) + '\n' + str(nm.pull_data(clan))
    return return_str

def id_to_clan(clan_id):
    clan_json = requests.get('https://api.worldoftanks.com/wot/clan/info/?application_id=f5904c98f5c04af24820d01cbddd8a86&clan_id={0}'.format(clan_id)).json()
    if 'data' in clan_json:
        return Clan(clan_json['data'][str(clan_id)])
    return Clan.error_clan

def get_tournament(province_id):
    province_json = requests.get('https://api.worldoftanks.com/wot/globalwar/tournaments/?application_id=f5904c98f5c04af24820d01cbddd8a86&map_id=globalmap&province_id={0}'.format(province_id)).json()
    return Tournament(province_json)

def pick_clan(search_name, from_console = False):
    clan_list = requests.get('https://api.worldoftanks.com/wot/clan/list/?application_id=f5904c98f5c04af24820d01cbddd8a86&search={0}'.format(search_name)).json()['data']
    clans = []
    for i in range(len(clan_list)):
        clans.append(Clan(clan_list[i]))
        if clans[i].abbreviation == search_name:
            return clans[i]
    if not from_console:
        return Clan.error_clan
    for i in range(len(clans)):
        print('{0} | {1}'.format(i,clans[i]))
    clan = None
    if opt_num == None:
        while clan == None:
            clan_num = input('Select clan from search list by number: #')
            try:
                clan_num = int(clan_num)
                clan = clans[clan_num]
            except ValueError:
                print('Not a number.')
            except IndexError:
                print('Out of range.')
    else:
        clan = clans[int(clan_num)]
    return clan

def check_clan(clan_name = None):
    if clan_name == None:
        clan = pick_clan(input('Clan: '))
    else:
        clan = pick_clan(clan_name)
    return_str = str(nm.pull_data(clan))+'\n\nCurrent Tournaments: '
    for battle in clan.battles:
        return_str += analyze_matches(clan,get_tournament(battle.province_id))
    return return_str

def check_province():
    province_tourn = get_tournament(input('Province ID: '))
    print(province_tourn)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clan', help='Check clan data', action='store_true')
    parser.add_argument('-p', '--province', help='Check province data', action='store_true')
    args = parser.parse_args()
    if args.clan:
        print(check_clan())
    elif args.province:
        check_province()