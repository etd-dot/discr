import sys
from math import log
from decimal import Decimal, getcontext


def define_segments(letters, probabilities):
    segments = {}
    current_left = Decimal('0')
    for letter, prob in zip(letters, probabilities):
        segments[letter] = {'left': current_left, 'right': current_left + prob}
        current_left += prob
    return segments


def arithmetic_coding(letters, probabilities, text):
    segments = define_segments(letters, probabilities)
    left = Decimal('0')
    right = Decimal('1')
    interval_history = []

    for idx, symbol in enumerate(text):
        if symbol not in segments:
            print(f"Ошибка: символ '{symbol}' не найден в сегментах.")
            sys.exit(1)

        seg = segments[symbol]
        range_width = right - left
        new_left = left + range_width * seg['left']
        new_right = left + range_width * seg['right']

        interval_history.append({
            'symbol': symbol,
            'left': new_left,
            'right': new_right
        })

        left, right = new_left, new_right

    code = (left + right) / 2
    return code, interval_history


def main():
    getcontext().prec = 150

    text = input("Введите слово для арифметического кодирования (кириллица): ").strip()

    if not text:
        print("Ошибка: введена пустая строка.")
        return

    frequency = {}
    first_occurrence = {}
    for idx, char in enumerate(text):
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
            first_occurrence[char] = idx

    letters = sorted(frequency.keys(), key=lambda x: (-frequency[x], first_occurrence[x]))
    total = Decimal(len(text))
    probabilities = [Decimal(frequency[letter]) / total for letter in letters]

    print("\nЧастоты и вероятности символов:")
    print("Символ\tЧастота\tВероятность")
    for letter, prob in zip(letters, probabilities):
        print(f"{letter}\t{frequency[letter]:d}\t{prob:.150f}")

    code, history = arithmetic_coding(letters, probabilities, text)

    print("\nПроцесс арифметического кодирования:")
    print("Символ\tЛевая граница\t\t\t\t\tПравая граница")
    for step in history:
        print(f"{step['symbol']}\t{step['left']:.150f}\t{step['right']:.150f}")

    print(f"\nКод: {code:.100f}")


if __name__ == "__main__":
    main()

