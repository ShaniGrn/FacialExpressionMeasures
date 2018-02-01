from datetime import datetime
from LoadFilesGit import *
import pickle

# checking if the date of the experiment and expressions is in the range of experiment dates.
def get_time(t_str):
    try:
        return datetime.strptime(t_str, '%Y_%m_%d_%H_%M_%S')
    except:
        return datetime.strptime(t_str, '%Y_%m_%d_%H_%M_%S_%f')

# finding min and max timestamp per participant
def minmax(data):
    min_date = data[0]
    max_date = data[0]
    for x in data:
        if x < min_date:
            min_date = x
        if x > max_date:
            max_date = x
    return min_date, max_date

def extract_audio (filename):
    new_file_name = str(filename)
    temp = new_file_name.split('/')[1]
    temp2 = temp.split(".")[0]
    lastchar = temp2[-1]
    return temp2.replace(lastchar,'') , lastchar

def findActionFac(t_time,tab):
    for tab, data in new_game.iteritems():
        for subject in data.keys():
            tmin, tmax = new_game[tab][subject]['Min'],new_game[tab][subject]['Max']
            if t_time > tmin and t_time < tmax:
                for i, subjectx in enumerate(d['subject'] for d in game_data[tab]):
                    if subjectx == subject and get_time(game_data[tab][i]['time'])<t_time and t_time<get_time(game_data[tab][i+1]['time']):
                        return game_data[tab][i]['obj'],game_data[tab][i]['action'], game_data[tab][i]['comment']



with open('game_data.pickle', 'wb') as handle:
    pickle.dump(game_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('aff_data.pickle', 'wb') as handle:
    pickle.dump(aff_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Done - saved to pickle')
print('--- Done input ---')

new_game = {}
for tab, data in game_data.iteritems():
            subject_dict = {}
            for x in data: # x = dictionary
               if x['subject'] not in subject_dict:
                   subject_dict[x['subject']] = {'times': [get_time(x['time'])]}
               else:
                   subject_dict[x['subject']]['times'].append(get_time(x['time']))
            new_game[tab] = subject_dict

print('--- Done Create user MinMax ---')

for tab, data in new_game.iteritems():
    for subject in data.keys():  # x = dictionary
        tempmin, tempmax = minmax(data[subject]['times'])
        new_game[tab][subject]['Min'] , new_game[tab][subject]['Max'] = tempmin, tempmax
        for affdata in aff_data[tab]:
            temp_time = get_time(affdata['time'])
            if temp_time > tempmin and temp_time < tempmax:
                if 'aff' not in new_game[tab][subject]:
                    i = 0
                    new_game[tab][subject]['aff'] =[affdata]
                    new_game[tab][subject]['aff'][i]['Faculty'],new_game[tab][subject]['aff'][i]['action'], new_game[tab][subject]['aff'][i]['Track'] = findActionFac(temp_time, tab)
                    temp1, temp2 = extract_audio(new_game[tab][subject]['aff'][i]['Track'])
                    new_game[tab][subject]['aff'][i]['AudioFile'], new_game[tab][subject]['aff'][i]['FileNum'] = temp1, temp2
                    if float(new_game[tab][subject]['aff'][i]['joy']) > 50.0:
                        new_game[tab][subject]['aff'][i]['joy_cnt'] = 1
                    else:
                        new_game[tab][subject]['aff'][i]['joy_cnt'] = 0
                    if float(new_game[tab][subject]['aff'][i]['smile']) > 50.0:
                        new_game[tab][subject]['aff'][i]['smile_cnt'] = 1
                    else:
                        new_game[tab][subject]['aff'][i]['smile_cnt'] = 0
                else:
                    i = i + 1
                    new_game[tab][subject]['aff'].append(affdata)
                    new_game[tab][subject]['aff'][i]['Faculty'], new_game[tab][subject]['aff'][i]['action'], new_game[tab][subject]['aff'][i]['Track'] = findActionFac(temp_time, tab)
                    temp1, temp2 = extract_audio(new_game[tab][subject]['aff'][i]['Track'])
                    new_game[tab][subject]['aff'][i]['AudioFile'], new_game[tab][subject]['aff'][i]['FileNum'] = temp1, temp2
                    if float(new_game[tab][subject]['aff'][i]['joy']) > 50.0:
                        new_game[tab][subject]['aff'][i]['joy_cnt'] = 1
                    else:
                        new_game[tab][subject]['aff'][i]['joy_cnt'] = 0
                    if float(new_game[tab][subject]['aff'][i]['smile']) > 50.0:
                        new_game[tab][subject]['aff'][i]['smile_cnt'] = 1
                    else:
                        new_game[tab][subject]['aff'][i]['smile_cnt'] = 0

print('--- Done Create user and affdata ---')


with open('new_game.pickle', 'wb') as handle:
    pickle.dump(new_game, handle, protocol=pickle.HIGHEST_PROTOCOL)


new_game_aff = {}
for tab, data in new_game.iteritems():
            subject_dict = {}
            for x in data: # x = dictionary
                if 'aff' in data[x]:
                    if x not in subject_dict:
                        subject_dict[x] = data[x]
                    else:
                        subject_dict[x].append(data[x])
            new_game_aff[tab] = subject_dict

with open('new_game_aff.pickle', 'wb') as handle:
    pickle.dump(new_game_aff, handle, protocol=pickle.HIGHEST_PROTOCOL)

print('Done - saved to pickle - new_game_aff')



with open('new_game_aff.pickle', 'rb') as handle:
    new_game_aff_f = pickle.load(handle)

print new_game_aff == new_game_aff_f
