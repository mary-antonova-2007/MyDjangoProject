from django.shortcuts import render
from django.http import JsonResponse
from .services import get_available_dates, get_data_by_date, check_rooms
from django.http import JsonResponse, HttpResponse
import json
import requests

# В вашем auth_token должен быть реальный токен аутентификации
auth_token = 'ppo_10_13903'


def parse_room_info(data):
    rooms_count = data['rooms_count']['data']
    windows_per_room = data['windows_for_room']['data']
    light_data = data['windows']['data']

    # Список для сбора номеров комнат с включенным светом
    room_numbers_with_light = []

    # Начальный номер комнаты для каждого этажа
    room_number = 1

    # Пройдемся по каждому этажу
    for floor in light_data:
        # Получим список окон с включенным светом на этаже
        windows_light_on = light_data[floor]

        # Счетчик окон для определения номера комнаты
        window_counter = 0

        # Пройдемся по каждому окну на этаже
        for window, is_light_on in enumerate(windows_light_on, start=1):
            # Если свет включен, добавим комнату в список
            if is_light_on:
                # Номер комнаты = текущий номер комнаты + номер окна // окна в комнате
                room_numbers_with_light.append(
                    room_number + window_counter // windows_per_room[window_counter % rooms_count])

            # Увеличиваем счетчик окон
            window_counter += 1

        # Пересчитываем номер комнаты для следующего этажа
        room_number += rooms_count

    # Убираем дубликаты номеров комнат и сортируем их
    room_numbers_with_light = sorted(set(room_numbers_with_light))
    return room_numbers_with_light


def available_dates(request):
    dates = get_available_dates(auth_token)
    if dates:
        return JsonResponse({'dates': dates})
    else:
        return JsonResponse({'error': 'Не удалось получить список дат'}, status=500)


def data_by_date(request, day, month, year):
    data = get_data_by_date(day, month, year, auth_token)
    if data and 'error' not in data:
        return JsonResponse(data)
    else:
        error_message = data.get('response', 'Неизвестная ошибка API')
        return JsonResponse({'error': f'Не удалось получить данные за указанную дату. {error_message}'}, status=500)



def rehearsal_rooms(request):
    if request.method == 'POST':
        # Получаем дату напрямую из данных формы
        date = request.POST.get('date')
        # Данные о комнатах получаем в виде строки JSON из данных формы
        rooms_data = request.POST.get('data')

        try:
            # Преобразуем строку JSON в объект Python
            data = json.loads(rooms_data)
        except json.JSONDecodeError as e:
            return JsonResponse({'error': f'Неверный формат JSON в поле data: {str(e)}'}, status=400)

        # Теперь `data` содержит словарь с данными о комнатах, который можно использовать для дальнейшей обработки
        # Здесь должен быть ваш код для обработки данных и отправки их во внешний API...

        # Пример возврата ответа
        return JsonResponse({'success': True, 'received_data': data, 'date': date})

    elif request.method == 'GET':
        return render(request, 'rehearsals/rehearsal_rooms_form.html')
    else:
        return HttpResponse('Метод запроса не поддерживается', status=405)


# View для отображения страницы с информацией
def rehearsal_info(request, day, month, year):
    data = get_data_by_date(day, month, year, auth_token)
    print('rehearsal_info data:', data)
    if data:
        # Допустим, что функция parse_room_info извлекает номера комнат из данных API
        room_numbers = parse_room_info(data)  # Вы должны написать эту функцию
        context = {
            'date': data['date'],
            'rooms_count': data['rooms_count'],
            'windows_for_room': data['windows_for_room'],
            'windows': data['windows'],
            'room_numbers': room_numbers
        }
        return render(request, 'rehearsals/rehearsal_info.html', context)
    else:
        return JsonResponse({'error': 'Не удалось получить данные за указанную дату'}, status=500)

