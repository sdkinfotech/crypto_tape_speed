# main.py

import asyncio
from trade_stream import trade_stream
from speed_indicator import speed_indicator
from graph_drawer import draw_trade_activity_from_file

async def main(symbol: str, interval: int):
    """
    Главный модуль, который интегрирует сбор информации о сделках и их анализ с отрисовкой графиков.

    :param symbol: Символ торговой пары на Binance Futures.
    :param interval: Интервал времени для анализа скорости сделок, в минутах.
    """
    queue = asyncio.Queue()

    # Запуск асинхронных потоков сбора информации о сделках и анализа скорости
    producer_task = asyncio.create_task(trade_stream(symbol, queue))
    indicator_task = asyncio.create_task(speed_indicator(queue, interval))

    # Ожидаем завершения обеих задач
    await asyncio.gather(producer_task, indicator_task)

    # После сбора данных отрисовываем графики из файла
    draw_trade_activity_from_file('trade_data.txt')

if __name__ == "__main__":
    # Запуск программы с заданными параметрами
    symbol = 'btcusdt'  # Пример с символом торговой пары BTC/USDT
    interval = 1  # Интервал анализа скорости сделок в минутах
    asyncio.run(main(symbol, interval))