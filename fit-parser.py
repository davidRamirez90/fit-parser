import fitdecode
import json
import numpy as np
import os

def saveJson(obj):
    with open('activities.json', 'w') as outfile:
        json.dump(obj, outfile)

def decodeFitFile(file, name):
    power = []
    obj = {}
    with fitdecode.FitReader(file) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage):
                if frame.name == 'file_id':
                    if frame.has_field('time_created'):
                        obj['date'] = frame.get_value('time_created').isoformat()
                if frame.name == 'record':
                    if frame.has_field('power'):
                        power.append(frame.get_value('power'))

    zones, _ = np.histogram(np.array(power), bins=[0, 176, 220, 2000])
    obj['zones'] = zones.tolist()
    obj['samples'] = len(power)
    obj['name'] = name.replace('.fit', '')

    print(zones)


    return obj

def main():
    path = './fit_files'
    files = [f for f in os.listdir(path) if f.endswith('.fit')]

    print(files)

    myJson = {
        'activities': []
    }

    for file in files:

        url = "./fit_files/{name}".format(name=file)
        obj = decodeFitFile(url, file)
        myJson['activities'].append(obj)
        print('Saved file {}'.format(obj['name']))

    saveJson(myJson)
    print('success')


if __name__ == '__main__':
    main()
