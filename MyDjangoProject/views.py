from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt


def main(request):
    if request.method == 'POST':
        # Обработка POST запроса
        rooms_count = request.POST.get('rooms_count')
        windows_per_room = request.POST.get('windows_per_room')
        light_data = request.POST.get('light_data')

        # Здесь может быть логика по обработке данных, например, сохранение в базу данных или проверка

        # Передаем данные обратно для отображения или для дальнейшей обработки
        return JsonResponse({
            'rooms_count': rooms_count,
            'windows_per_room': windows_per_room,
            'light_data': light_data
        })

    elif request.method == 'GET':
        # Обработка GET запроса (если есть параметры)
        # ...

        # Показываем страницу, если это простой GET запрос
        return render(request, 'main.html')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])


