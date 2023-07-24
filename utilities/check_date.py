import re
from datetime import datetime


async def check_user_date(user_date):
    date_pattern = re.compile(
        '^(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])\/\d{4}-(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])\/\d{4}$')

    if not date_pattern.match(user_date):
        return False

    date_parts = user_date.split('-')
    start_date_str, end_date_str = date_parts[0], date_parts[1]

    start_date = datetime.strptime(start_date_str, '%d/%m/%Y').date()
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y').date()

    # Удаление времени из текущей даты
    current_date = datetime.now().date()

    # Проверка на будущую дату (начальная и конечная дата должны быть больше или равны текущей дате)
    if start_date < current_date or end_date < current_date:
        return False

    if start_date > end_date:
        return False

    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }

    # Проверка на високосный год (29 дней в феврале)
    if start_date.year % 4 == 0 and (start_date.year % 100 != 0 or start_date.year % 400 == 0):
        days_in_month[2] = 29

    if start_date.day > days_in_month[start_date.month] or end_date.day > days_in_month[end_date.month]:
        return False

    # Возвращаем даты в формате "00-00-0000"
    start_date_formatted = start_date.strftime('%Y-%m-%d')
    end_date_formatted = end_date.strftime('%Y-%m-%d')

    return [start_date_formatted, end_date_formatted]
