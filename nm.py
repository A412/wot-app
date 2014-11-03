import requests

class ClanData():

    def __init__(self,t10_tanks,avg_wn8,avg_wn8_60,wr,wr_60,battle_count):
        self.t10_tanks = t10_tanks
        self.avg_wn8 = avg_wn8
        self.avg_wn8_60 = avg_wn8_60
        self.wr = wr
        self.wr_60 = wr_60
        self.battle_count = battle_count

    def __repr__(self):
        return 'Tier 10 tanks: {0}\nAverage WN8: {1}\nAverage 60-day WN8: {2}\nAverage WR: {3}\nAverage 60-day WR: {4}\nAverage Battle Count: {5}'.format(self.t10_tanks,self.avg_wn8,self.avg_wn8_60,self.wr,self.wr_60,self.battle_count)

def pull_data(clan):
    nm_page = requests.get('http://www.noobmeter.com/clanTankList/na/{0}/{1}'.format(clan.abbreviation,clan.id)).text
    first_total = nm_page.find('Total (')
    total = search_forward(nm_page, first_total+7, first_total + 12)
    nm_page = requests.get('http://www.noobmeter.com/clan/na/{0}'.format(clan.abbreviation)).text
    first_weighted_average = nm_page.find('Weighted average:')
    average_text = nm_page[first_weighted_average:first_weighted_average + 250]
    average_text = average_text.replace('td','',9)
    fields = ['avg_wn8','avg_wn8_60','wr','wr_60','battle_count']
    field_dic = {}
    for item in fields:
        next_td = average_text.find('td')
        field_dic.update({item:search_forward(average_text, next_td + 3, next_td + 10)})
        average_text = average_text.replace('td','',2)
    return ClanData(total,field_dic['avg_wn8'],field_dic['avg_wn8_60'],field_dic['wr'],field_dic['wr_60'],field_dic['battle_count'])

def search_forward(search_str, first, last):
    new_str = search_str[first:last]
    i = 0
    while i < len(new_str) and is_int(new_str[i]):
        i += 1
    return new_str[:i]

def is_int(try_str):
    if try_str == '.' or try_str == ',':
        return True
    try:
        int(try_str)
        return True
    except:
        return False