import matplotlib
import pandas as pd
import matplotlib.pyplot as plt

import pickle

import csv
from datetime import datetime


def get_time(t_str):
    try:
        return datetime.strptime(t_str, '%Y_%m_%d_%H_%M_%S')
    except:
        return datetime.strptime(t_str, '%Y_%m_%d_%H_%M_%S_%f')


new_game_load = pd.read_pickle('C://Users//sgershtein//Documents//PycharmProjects//Goren//GitHub//new_game_aff.pickle')
new_game_load

print('Tablet, number of participants')
for t, data in new_game_load.items():
    print(t, len(data))



graph_subject ={}
for tab, data in new_game_load.iteritems():
    for subject, subjectdata in data.iteritems():
        if subject not in graph_subject:
            graph_subject[subject]={}
            for affdata in subjectdata['aff']:
                for feelings, value in  affdata.iteritems():
                    if feelings == 'attention':
                        if 'attention' not in graph_subject[subject]:
                            graph_subject[subject]['attention'] = [value]
                        else:
                            graph_subject[subject]['attention'].append(value)
                    if feelings == 'joy':
                        if 'joy' not in graph_subject[subject]:
                            graph_subject[subject]['joy'] = [value]
                            if value > 50.0:
                                graph_subject[subject]['joy_cnt'] = 1
                            else:
                                graph_subject[subject]['joy_cnt'] = 0
                        else:
                            graph_subject[subject]['joy'].append(value)
                            if value > 50.0:
                                graph_subject[subject]['joy_cnt'] = 1
                            else:
                                graph_subject[subject]['joy_cnt'] = 0
                    if feelings == 'surprise':
                        if 'surprise' not in graph_subject[subject]:
                            graph_subject[subject]['surprise'] = [value]
                        else:
                            graph_subject[subject]['surprise'].append(value)
                    if feelings == 'sadness':
                        if 'sadness' not in graph_subject[subject]:
                            graph_subject[subject]['sadness'] = [value]
                        else:
                            graph_subject[subject]['sadness'].append(value)
                    if feelings == 'smile':
                        if 'smile' not in graph_subject[subject]:
                            graph_subject[subject]['smile'] = [value]
                            if value >0.5:
                                graph_subject[subject]['smile_cnt'] = 1
                            else:
                                graph_subject[subject]['smile_cnt'] = 0
                        else:
                            graph_subject[subject]['smile'].append(value)
                            if value >0.5:
                                graph_subject[subject]['smile_cnt'] = 1
                            else:
                                graph_subject[subject]['smile_cnt'] = 0
                    if feelings == 'fear':
                        if 'fear' not in graph_subject[subject]:
                            graph_subject[subject]['fear'] = [value]
                        else:
                            graph_subject[subject]['fear'].append(value)
                    if feelings == 'valence':
                        if 'valence' not in graph_subject[subject]:
                            graph_subject[subject]['valence'] = [value]
                        else:
                            graph_subject[subject]['valence'].append(value)
                    if feelings == 'contempt':
                        if 'contempt' not in graph_subject[subject]:
                            graph_subject[subject]['contempt'] = [value]
                        else:
                            graph_subject[subject]['contempt'].append(value)
                    if feelings == 'engagement':
                        if 'engagement' not in graph_subject[subject]:
                            graph_subject[subject]['engagement'] = [value]
                        else:
                            graph_subject[subject]['engagement'].append(value)
                    if feelings == 'smirk':
                        if 'smirk' not in graph_subject[subject]:
                            graph_subject[subject]['smirk'] = [value]
                        else:
                            graph_subject[subject]['smirk'].append(value)
                    if feelings == 'anger':
                        if 'anger' not in graph_subject[subject]:
                            graph_subject[subject]['anger'] = [value]
                        else:
                            graph_subject[subject]['anger'].append(value)
                    if feelings == 'time':
                        if 'time' not in graph_subject[subject]:
                            graph_subject[subject]['time'] = [value]
                        else:
                            graph_subject[subject]['time'].append(value)
                    if feelings == 'action':
                        if 'action' not in graph_subject[subject]:
                            graph_subject[subject]['action'] = [value]
                        else:
                            graph_subject[subject]['action'].append(value)
                    if feelings == 'Faculty':
                        if 'Faculty' not in graph_subject[subject]:
                            graph_subject[subject]['Faculty'] = [value]
                        else:
                            graph_subject[subject]['Faculty'].append(value)



with open('graph_subject.pickle', 'wb') as handle:
    pickle.dump(graph_subject, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('graph_subject.pickle', 'rb') as handle:
    graph_subject_f = pickle.load(handle)


print graph_subject == graph_subject_f
print ('--- Done graph_subject ---')


with open('Data.csv', 'wb') as new_file:
        writer = csv.writer(new_file, dialect='excel' )
        writer.writerow(['subject','Min','Max','time','diff','action','Faculty','AudioFile','FileNum','joy','joy_cnt','smile','smile_cnt','surprise','sadness','valence','smirk','engagement','disgust','attention','fear','anger'])
        for tab, data in new_game_load.iteritems():
            for subject, subject_data in data.iteritems():
                for aff_data in subject_data['aff']:
                    writer.writerow([subject, subject_data['Min'], subject_data['Max'],
                                     get_time(aff_data['time']), get_time(aff_data['time'])-subject_data['Min'],
                                     aff_data['action'], aff_data['Faculty'],aff_data['AudioFile'], aff_data['FileNum'],
                                     aff_data['joy'], aff_data['joy_cnt'],aff_data['smile'], aff_data['smile_cnt'] ,aff_data['surprise'],aff_data['sadness'],aff_data['valence'],
                                     aff_data['smirk'],aff_data['engagement'],aff_data['disgust'],aff_data['attention'], aff_data['fear'], aff_data['anger']])
new_file.close()
print ('--- Done csv ---')














