# speed_indicator.py

import asyncio
from datetime import datetime, timedelta, timezone

async def speed_indicator(queue: asyncio.Queue, interval: int=1):
    """
    Анализ скорости сделок на фьючерсном рынке Binance.

    :param queue: Асинхронная очередь, из которой будут извлекаться данные о сделках.
    :param interval: Интервал времени в минутах, за который собираются и анализируются данные.
    """
    previous_data = {
        'long_count': 0,
        'short_count': 0,
        'long_volume': 0.0,
        'short_volume': 0.0
    }

    while True:
        current_data = {
            'long_count': 0,
            'short_count': 0,
            'long_volume': 0.0,
            'short_volume': 0.0
        }
        start_time = datetime.now(timezone.utc)
        
        while datetime.now(timezone.utc) - start_time < timedelta(minutes=interval):
            trade = await queue.get()
            update_trade_counters(current_data, trade)  # Обновление счетчиков на основе новых сделок
        
        print_trade_info(current_data, previous_data)  # Вывод информации о текущем интервале
        write_trade_data_to_file(current_data)  # Запись текущих значений в файл
        previous_data = current_data.copy()  # Сохранение текущих значений для следующего интервала
        start_time = datetime.now(timezone.utc)  # Сброс времени начала интервала

def update_trade_counters(current_data, trade):
    """
    Обновляет счетчики торговых операций в соответствии с текущей сделкой.

    :param current_data: Текущая статистика сделок.
    :param trade: Данные о сделке.
    """
    count = 1  # Количество сделок, для текущей сделки это всегда 1
    volume = float(trade['q'])  # Объем текущей сделки
    if trade['m']:  # Проверка, является ли сделка мейкерской (обычно шорты)
        current_data['short_count'] += count
        current_data['short_volume'] += volume
    else:  # Тейкерская сделка интерпретируется как лонг
        current_data['long_count'] += count
        current_data['long_volume'] += volume

def print_trade_info(current_data, previous_data):
    """
    Выводит статистику текущего интервала и сравнивает ее с предыдущим интервалом.

    :param current_data: Текущая статистика сделок.
    :param previous_data: Статистика сделок за предыдущий интервал.
    """
    # Вывод основной статистики сделок
    total_trades_count = current_data['long_count'] + current_data['short_count']
    total_volume = current_data['long_volume'] + current_data['short_volume']
    print(f"Total trades count: {total_trades_count}")
    print(f"Long trades count: {current_data['long_count']}, Volume: {current_data['long_volume']}")
    print(f"Short trades count: {current_data['short_count']}, Volume: {current_data['short_volume']}")
    print(f"Combined volume: {total_volume}")

    # Вывод изменений по сравнению с предыдущим интервалом
    long_volume_change = current_data['long_volume'] - previous_data['long_volume']
    short_volume_change = current_data['short_volume'] - previous_data['short_volume']
    total_volume_change = total_volume - (previous_data['long_volume'] + previous_data['short_volume'])
    print(f"Long volume change: {long_volume_change}")
    print(f"Short volume change: {short_volume_change}")
    print(f"Total volume change: {total_volume_change}")

    # Определение тенденции активности на рынке
    activity_trend = "accelerating" if total_trades_count > (previous_data['long_count'] + previous_data['short_count']) \
        else "slowing down" if total_trades_count < (previous_data['long_count'] + previous_data['short_count']) \
        else "stable"
    print(f"Market activity is {activity_trend}.")

def write_trade_data_to_file(current_data):
    """
    Записывает текущие торговые данные в файл для последующего анализа.

    :param current_data: Текущая статистика сделок.
    """
    with open('trade_data.txt', 'a') as f:  # Открываем файл для добавления данных
        f.write(f"{current_data['long_count']},{current_data['short_count']},"
                f"{current_data['long_volume']},{current_data['short_volume']}\n")