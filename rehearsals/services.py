import requests


def get_available_dates(auth_token):
    url = 'https://olimp.miet.ru/ppo_it_final/date'
    headers = {'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return None


def get_data_by_date(day, month, year, auth_token):
    # Формируем URL с учетом требований к формату параметров
    url = f'https://olimp.miet.ru/ppo_it_final/?day={day}&month={month}&year={year}'
    headers = {'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        # Выводим информацию об ошибке для отладки
        print(f'Error {response.status_code}: {response.text}')
        return None



def check_rooms(data, date, auth_token):
    url = 'https://olimp.miet.ru/ppo_it_final'
    headers = {
        'X-Auth-Token': auth_token,
        'Content-Type': 'application/json'
    }
    payload = {
        "data": data,
        "date": date
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return None