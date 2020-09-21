import fitdecode
import json

def saveJson(obj, name):
    with open('{name}.json'.format(name=name), 'w') as outfile:
        json.dump(obj, outfile)

def decodeFitFile(file, field, keys):

    obj = {
        'distance': [],
        'cadence': [],
        'power': []
    }
    with fitdecode.FitReader(file) as fit:
        for frame in fit:
            if isinstance(frame, fitdecode.FitDataMessage):
                if (frame.name == field):
                    for k in keys:
                        obj[k].append(frame.get_value(k))

    return obj

def main():
    name = '2020-09-20-135543-ELEMNT BOLT EFFF-21-0'
    url = "./{name}.fit".format(name=name)
    field_name = 'record'
    keys = ['distance', 'cadence', 'power']
    obj = decodeFitFile(url, field_name, keys)

    saveJson(obj, name)
    print('success')


if __name__ == '__main__':
    main()
