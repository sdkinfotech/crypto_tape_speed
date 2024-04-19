# graph_drawer.py

import matplotlib.pyplot as plt
import numpy as np

def draw_trade_activity_from_file(filename):
    """
    Чтение данных из файла и отрисовка графиков активности торгов.
    
    :param filename: Имя файла с данными торговых операций.
    """
    total_counts, long_volumes, short_volumes, total_volumes = [], [], [], []
    with open(filename, 'r') as f:
        for line in f.readlines():
            long_count, short_count, long_volume, short_volume = line.strip().split(',')
            total_counts.append(int(long_count) + int(short_count))
            long_volumes.append(float(long_volume))
            short_volumes.append(float(short_volume))
            total_volumes.append(float(long_volume) + float(short_volume))

    intervals = np.arange(len(total_counts))

    # Создаем фигуру и массив подграфиков
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(14, 10), sharex=True)

    # График количества торгов гистограммой
    ax1.bar(intervals, total_counts, color='blue', alpha=0.7)
    ax1.set_ylabel('Number of Trades')
    ax1.set_title('Total Trades Count Over Intervals')

    # Линейные графики объемов лонгов и шортов
    ax2.plot(intervals, long_volumes, label="Long Volume", color='green')
    ax2.plot(intervals, short_volumes, label="Short Volume", color='red')
    ax2.set_ylabel('Trade Volume')
    ax2.set_title('Trade Volumes Over Intervals')
    ax2.legend()

    # График общего объема торгов гистограммой
    ax3.bar(intervals, total_volumes, color='grey', alpha=0.7)
    ax3.set_xlabel('Interval')
    ax3.set_ylabel('Total Trade Volume')
    ax3.set_title('Total Trade Volume Over Intervals')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_trade_activity_from_file('trade_data.txt')