import json

import requests


URL = 'https://tui.ru/api/office/cities'
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
'accept':'*/*' }
parsed_offices=[]
def get_data():
    offices_by_city_resp=requests.get(URL,headers=headers)
    offices_by_city = offices_by_city_resp.json()
    return offices_by_city
def parse_data ():
    for office_by_city in get_data():
        office_url = 'https://www.tui.ru/api/office/list/?cityId='+str(office_by_city.get('cityId'))+'&subwayId=&hoursFrom=&hoursTo=&serviceIds=all&toBeOpenOnHolidays=false'
        office_resp=requests.get(office_url,headers=headers)
        offices=office_resp.json()
        for office in offices:
            sat =''
            sun=''
            phones =[]
            if (str(office.get('hoursOfOperation').get('saturday').get('startStr'))!='None'):
                sat=str(office.get('hoursOfOperation').get('saturday').get('startStr'))+' - '+str(office.get('hoursOfOperation').get('saturday').get('endStr'))
            else: sat= 'dayoff'
            if (str(office.get('hoursOfOperation').get('sunday').get('startStr')) != 'None'):
                sun = str(office.get('hoursOfOperation').get('saturday').get('startStr'))+' - ' + str(office.get('hoursOfOperation').get('saturday').get('endStr'))
            else:
                sun = 'dayoff'
            for counter in range(0,len(office.get('phones'))):
                phones.append(office.get('phones')[counter].get('phone'))
            parsed_office={
            'address': office.get('address'),
            'latlon' : str(office_by_city.get('latitude'))+' ,'+str(office_by_city.get('longitude')),
            'name' : office.get('name'),
            'phones' : phones,
            'working_hours' : 'working_days: '+str(office.get('hoursOfOperation').get('workdays').get('startStr'))+' - '+
                                str(office.get('hoursOfOperation').get('workdays').get('endStr'))+
            ' saturday : '+sat+' sunday: '+sun
            }
            parsed_offices.append(parsed_office)
    with open('TUI_offices.json','w') as f:
       json.dump(parsed_offices, f, ensure_ascii=False)


parse_data()