import requests


def get_available_dates(auth_token):
    url = 'https://olimp.miet.ru/ppo_it_final/date'
    print('get_available_dates - url:', url)
    headers = {'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        return None


def get_data_by_date(day, month, year, auth_token):
    url = f'https://olimp.miet.ru/ppo_it_final/?day={day}&month={month}&year={year}'

    print(f'get_data_by_date url: {url}')
    headers = {'X-Auth-Token': auth_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()['message']
    else:
        print(f'Error {response.status_code}: {response.text}')  # Для отладки
        return {'error': f'Ошибка API: {response.status_code}', 'response': response.text}



def check_rooms(data, auth_token):
    url = 'https://olimp.miet.ru/ppo_it_final'
    headers = {
        'X-Auth-Token': auth_token,
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f'Ошибка API: {response.status_code}', 'response': response.text}

