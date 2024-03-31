from django.shortcuts import render
from django.http import JsonResponse
from .services import get_available_dates, get_data_by_date, check_rooms
from django.http import JsonResponse, HttpResponse
import json
import requests

# В вашем auth_token должен быть реальный токен аутентификации
auth_token = 'ppo_10_13903'


def parse_room_info(data):
    windows_data = data['windows']['data']  # Данные о свете в окнах по этажам
    windows_for_flat = data['windows_for_flat']['data']  # Количество окон в комнатах
    room_numbers = []  # Список для хранения номеров комнат с включенным светом

    current_room = 0  # Индекс текущей комнаты
    for floor, lights in windows_data.items():  # Итерируем по каждому этажу
        window_index = 0  # Счетчик индекса окна для текущей комнаты
        while window_index < len(lights):  # Пока не пройдем все окна на этаже
            if current_room < len(windows_for_flat):  # Проверяем, не вышли ли мы за пределы списка комнат
                windows_count = windows_for_flat[current_room]  # Количество окон в текущей комнате
                # Проверяем, горит ли свет хотя бы в одном окне текущей комнаты
                if any(lights[window_index:window_index + windows_count]):
                    room_numbers.append(current_room + 1)  # Добавляем номер комнаты (нумерация с 1)
                window_index += windows_count  # Переходим к следующему набору окон (следующей комнате)
                current_room += 1  # Увеличиваем счетчик комнат
            else:
                break  # Выходим из цикла, если все комнаты обработаны

    return room_numbers


def available_dates(request):
    dates = get_available_dates(auth_token)
    print(dates)
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
    if data:
        room_numbers = parse_room_info(data)  # Вызываем функцию анализа данных
        context = {
            'date': data['date']['description'],  # Описание даты
            'rooms_count': data['flats_count']['data'],  # Количество комнат на этаже
            'windows_for_room': data['windows_for_flat']['data'],  # Количество окон в комнатах
            'windows': data['windows']['data'],  # Данные о свете в окнах
            'room_numbers': room_numbers  # Номера комнат с репетициями
        }
        print(context)
        return render(request, 'rehearsals/rehearsal_info.html', context)  # Отправляем данные в шаблон
    else:
        return JsonResponse({'error': 'Не удалось получить данные за указанную дату'}, status=500)

