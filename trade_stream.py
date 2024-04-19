# trade_stream.py

import asyncio
import json
import websockets

async def trade_stream(symbol: str, queue: asyncio.Queue):
    """
    Сбор информации о фьючерсных сделках Binance через WebSocket и помещение ее в очередь.

    :param symbol: Строка, обозначающая символ торговой пары на Binance Futures (например, "btcusdt").
    :param queue: Асинхронная очередь для помещения информации о сделках.
    """
    uri = f"wss://fstream.binance.com/ws/{symbol}@aggTrade"  # URL потока Binance Futures
    async with websockets.connect(uri) as ws:
        while True:
            try:
                response = await ws.recv()  # Получаем новые данные о сделках
                trade_data = json.loads(response)  # Конвертируем из JSON в словарь Python
                await queue.put(trade_data)  # Помещаем данные о сделке в очередь
            except Exception as e:
                print(f"Ошибка в потоке данных сделок: {e}")
                # Прерывание цикла при возникновении исключения
                break
