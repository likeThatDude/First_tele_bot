import re


async def check_user_date(user_date):
    date_pattern = re.compile(
        '^(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])\/\d{4}-(0[1-9]|[1-2]\d|3[0-1])\/(0[1-9]|1[0-2])\/\d{4}$')

    if not date_pattern.match(user_date):
        return False

    date_parts = user_date.split('-')
    start_date_str, end_date_str = date_parts[0], date_parts[1]

    from datetime import datetime
    start_date = datetime.strptime(start_date_str, '%d/%m/%Y')
    end_date = datetime.strptime(end_date_str, '%d/%m/%Y')

    if start_date > end_date:
        return False

    days_in_month = {
        1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
        7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
    }
    if start_date.day > days_in_month[start_date.month] or end_date.day > days_in_month[end_date.month]:
        return False

    return user_date
