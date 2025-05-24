# -*- coding: utf-8 -*-
"""
Author: @marteszibelina
Created on: 24.05.2025
Project: Tile Calculator
File: main.py
Description: Калькулятор для расчёта количества плиток на площадь поверхности.
"""

import tkinter as tk


class TileCalculator:
    """Программа расчёта количества плиток на площадь поверхности."""

    # Типы плиток и размеры швов, используемых при расчёте
    # Программа считает по среднему значению
    TILE_GROUT = [
        ('Ректифицированная плитка', (0.5, 1, 2)),
        ('Неректифицированная плитка', (2.5, 5)),
        ('Стеновая плитка', (1, 4, 7)),
        ('Половая плитка', (2.5, 3)),
        ('Большие размеры плитки', (2.5, 3)),
        ('Плитка с компенсационными швами', (5, 10)),
    ]

    def __init__(self):
        super().__init__()
        # Диалоговое окно
        self.root = tk.Tk()
        self.root.title('Калькулятор для плиток')
        self.root.geometry('300x240')
        self.root.resizable(True, True)
        title = tk.Label(self.root,
                         text='Выберите параметры плитки'
                              'и тип плитки',
                         font=('Arial', 12))
        title.pack()
        footer = tk.Label(self.root,
                          text='@marteszibelina | '
                          'https://github.com/marteszibelina | © 2025',
                          font=('Arial', 8), bg='black', fg='white')
        footer.pack(side='bottom')

        # Ввод параметров стены
        self.length_label = tk.Label(self.root,
                                     text='Длина поверхности (м):')
        self.length_entry = tk.Entry(self.root)
        self.width_label = tk.Label(self.root,
                                    text='Высота/ширина поверхности (м):')
        self.width_entry = tk.Entry(self.root)

        # Ввод параметров плитки
        self.tile_size_label = tk.Label(self.root, text='Размер плитки (м):')
        self.tile_size_entry = tk.Entry(self.root)

        # Выбор типа плитки
        # Значение по умолчанию
        self.selected_tile = tk.StringVar(self.root)
        self.selected_tile.set(self.TILE_GROUT[0][0])

        self.tile_grout_label = tk.Label(self.root, text='Тип плитки:')
        self.tile_grout_label.pack()

        # Выбор типа плитки
        tile_names = [tile[0] for tile in self.TILE_GROUT]
        self.tile_grout_select = tk.OptionMenu(
            self.root,
            self.selected_tile,
            *tile_names,
        )
        self.tile_grout_select.pack()

        # Результат расчёта
        self.result_label = tk.Label(self.root, text='Результат:')

        self.calculate_button = tk.Button(
            self.root, text='Рассчитать', command=self.calculate
        )

    def calculate(self):
        """Расчёт количества плиток с учётом швов и обрезков."""
        try:
            # Функция для преобразования запятых в точки и валидации числа
            def parse_number(entry):
                value = entry.get().strip()
                value = value.replace(',', '.')  # Заменяем запятые на точки
                return float(value)
            # Получение параметров с автоматическим преобразованием формата
            length = parse_number(self.length_entry)
            height = parse_number(self.width_entry)
            tile_size = parse_number(self.tile_size_entry)

            # Проверка на положительные значения
            if length <= 0 or height <= 0 or tile_size <= 0:
                raise ValueError('Значения должны быть положительными')

            # Получаем выбранный тип плитки и размеры швов
            selected_tile_name = self.selected_tile.get()
            tile_data = (next(tile for tile in self.TILE_GROUT
                              if tile[0] == selected_tile_name))
            grout_sizes = tile_data[1]

            # Берем средний размер шва для выбранного типа плитки (в метрах)
            grout_size = sum(grout_sizes) / len(grout_sizes) / 1000

            # Рассчитываем количество плиток по длине и высоте с учетом швов
            tiles_length = (length + grout_size) / (tile_size + grout_size)
            tiles_height = (height + grout_size) / (tile_size + grout_size)

            # Округляем до целого в большую сторону
            tiles_length_whole = (int(tiles_length)
                                  if tiles_length.is_integer()
                                  else int(tiles_length) + 1)
            tiles_height_whole = (int(tiles_height)
                                  if tiles_height.is_integer()
                                  else int(tiles_height) + 1)

            # Общее количество плиток
            total_tiles = tiles_length_whole * tiles_height_whole

            # Рассчитываем обрезки
            cut_length = (tiles_length_whole
                          * (tile_size + grout_size) - grout_size - length)
            cut_height = (tiles_height_whole
                          * (tile_size + grout_size) - grout_size - height)

            # Формируем результат
            result_text = f'Всего плиток: {total_tiles}\n'

            if cut_length > 0:
                result_text += f'Нужно обрезать {tiles_height_whole}'
                result_text += f' плиток по длине на {cut_length*100:.1f} см\n'
            if cut_height > 0:
                result_text += f'Нужно обрезать {tiles_length_whole}'
                result_text += f' плиток по высоте на {cut_height*100:.1f} см'

            if cut_length <= 0 and cut_height <= 0:
                result_text += 'Обрезки не требуются'

            self.result_label.config(text=result_text)

        except ValueError as e:
            self.result_label.config(text=f'Ошибка: {str(e)}')
        except Exception as e:
            self.result_label.config(text=f'Неожиданная ошибка: {str(e)}')

    def run(self):
        """Запуск программы."""
        self.length_label.pack()
        self.length_entry.pack()
        self.width_label.pack()
        self.width_entry.pack()
        self.tile_size_label.pack()
        self.tile_size_entry.pack()
        self.tile_grout_select.pack()
        self.calculate_button.pack()
        self.result_label = tk.Label(self.root, text='',
                                     font=('Arial', 12, 'bold'))
        self.result_label.pack()
        self.root.mainloop()


if __name__ == '__main__':
    calculator = TileCalculator()
    calculator.run()
