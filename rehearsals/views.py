from django.shortcuts import render
from django.http import JsonResponse
from .services import get_available_dates, get_data_by_date, check_rooms

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
    if data:
        return JsonResponse(data)
    else:
        return JsonResponse({'error': 'Не удалось получить данные за указанную дату'}, status=500)


def rehearsal_rooms(request):
    if request.method == 'POST':
        data = request.POST.get('data')
        date = request.POST.get('date')
        result = check_rooms(data, date, auth_token)
        if result:
            return JsonResponse({'result': result})
        else:
            return JsonResponse({'error': 'Не удалось проверить комнаты'}, status=500)
    else:
        return JsonResponse({'error': 'Неверный метод запроса'}, status=405)


# View для отображения страницы с информацией
def rehearsal_info(request, day, month, year):
    data = get_data_by_date(day, month, year, auth_token)
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

