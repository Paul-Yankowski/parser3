import json

import requests


URL = 'https://tui.ru/api/office/cities'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'accept':'*/*' }
office=[]
def get_data():
    resp=requests.get(URL,headers=headers)
    data = resp.json()
    for i in range(0,len(data)):
        offices = 'https://www.tui.ru/api/office/list/?cityId='+str(data[i].get('cityId'))+'&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
        resp1=requests.get(offices,headers=headers)
        city=resp1.json()
        for ct in city:
            sat =''
            sun=''
            phones =[]
            if (str(ct.get('hoursOfOperation').get('saturday').get('startStr'))!='None'):
                sat=str(ct.get('hoursOfOperation').get('saturday').get('startStr'))+' - '+str(ct.get('hoursOfOperation').get('saturday').get('endStr'))
            else: sat= 'dayoff'
            if (str(ct.get('hoursOfOperation').get('sunday').get('startStr')) != 'None'):
                sun = str(ct.get('hoursOfOperation').get('saturday').get('startStr'))+' - ' + str(ct.get('hoursOfOperation').get('saturday').get('endStr'))
            else:
                sun = 'dayoff'
            for l in range(0,len(ct.get('phones'))):
                phones.append(ct.get('phones')[l].get('phone'))
            cities={
            'address': ct.get('address'),
            'latlon' : str(data[i].get('latitude'))+' ,'+str(data[i].get('longitude')),
            'name' : ct.get('name'),
            'phones' : phones,
            'working_hours' : 'working_days: '+str(ct.get('hoursOfOperation').get('workdays').get('startStr'))+' - '+
                                str(ct.get('hoursOfOperation').get('workdays').get('endStr'))+
            ' saturday : '+sat+' sunday: '+sun
            }
            office.append(cities)
    with open('TUI_offices.json','w') as f:
       json.dump(office, f, ensure_ascii=False)


get_data()