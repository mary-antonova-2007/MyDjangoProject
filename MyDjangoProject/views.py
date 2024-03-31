from django.shortcuts import render
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from rehearsals.services import get_available_dates
from  rehearsals.views import auth_token


def main(request):
    dates = get_available_dates(auth_token)  # Получаем список доступных дат
    print(dates)
    if dates:
        # Преобразуем строки дат в словари с отдельными компонентами
        dates_context = []
        for date_str in dates:
            day, month, year = date_str.split('-')
            dates_context.append({
                'day': day,
                'month': month,
                'year': year,  # Преобразование в полный год, если в формате 'YY'
                'date_str': date_str  # Сохраняем исходную строку даты для отображения
            })
        context = {'dates': dates_context}
        return render(request, 'main.html', context)  # Отправляем данные в шаблон
    else:
        # В реальном приложении здесь может быть редирект на страницу ошибки или сообщение пользователю
        return JsonResponse({'error': 'Не удалось получить список дат'}, status=500)
