import os
import csv
from copy import deepcopy
import json


def in_dates(info, the_dates):
    correct_date = False
    for d in the_dates:
        if info[0] == d[0] and info[1] == d[1] and info[2] == d[2]:
            correct_date = True
    return correct_date

def load_affectiva(the_path, the_dates):
    feelings = ['joy', 'anger', 'disgust', 'contempt', 'engagement', 'fear', 'sadness', 'surprise', 'valence', 'smile',
                'attention', 'smirk']

    the_data = {}
    datum = {'time': None}
    for f in feelings:
        datum[f] = 0.0
    print('Tablet, number of files')
    for t in range(1,6):
        the_tab = 'tab' + str(t)
        the_data[the_tab] = []
        p = the_path + 'faces//affectiva_' + str(t) + '//'
        the_files = os.listdir(p)
        print(the_tab, len(the_files))
        for f in the_files:
            info = f.split('_')
            if in_dates(info[1:], the_dates):
                with open(p + f, mode='r') as infile:
                    reader = csv.reader(infile)
                    first_line = True
                    for rows in reader:
                        if not first_line:
                            new_datum = deepcopy(datum)
                            new_datum['time'] = rows[0]
                            for ifeel, feel in enumerate(feelings):
                                new_datum[feel] = rows[ifeel+1]
                            the_data[the_tab].append(new_datum)
                        first_line = False
    return the_data

def load_game(the_path, the_dates):
    the_data = {}
    new_data = {}
    datum = {'time': None}
    print('Tablet, number of files')
    for t in range(1, 6):
        the_tab = 'tab' + str(t)
        the_data[the_tab] = {}
        p = the_path + 'TAB' + str(t) + '//'
        the_files = os.listdir(p)
        print(the_tab, len(the_files))
        for f in the_files:
            info = f.split('_')
            if in_dates(info, the_dates):
                with open(p + f, mode='r') as infile:
                    json_data = json.load(infile)
                    for k, v in json_data.items():
                        v_data = json.loads(v['data'])
                        if 'log' in v_data:     # correction for new format
                            v_data = v_data['log']
                        if v_data['action'] in ['play', 'stop']:
                            v_data['subject'] = f
                        #    v_data['ID'] = f.split('_')[6].split('.')[0]
                            the_data[the_tab][v_data['time']] = v_data
                    # break
            new_data[the_tab] = [the_data[the_tab][x] for x in sorted(the_data[the_tab])]

    return new_data



the_path = 'C://Goren//Keren_Data//'
the_dates = [['2016', '05', '25'], ['2016', '02', '05'], ['2017', '02', '03'],['2017','05','24']]

print('--- Affectiva ---')
aff_data = load_affectiva(the_path, the_dates)

#aff_data_file = open('C://Goren//Keren_Data//affectiva_raw_data.json', 'w+')
#json.dump(aff_data, aff_data_file)

print('Tablet, number of data points')
for t, data in aff_data.items():
    print(t, len(data))


print('--- game ---')
game_data = load_game(the_path, the_dates)
#game_data_file = open('C://Goren//Keren_Data//game_raw_data.json', 'w+')
#json.dump(game_data, game_data_file)

print('Tablet, number of data points')
for t, data in game_data.items():
    print(t, len(data))
