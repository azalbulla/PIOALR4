import os

def parse(value):
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value

def get_set(filename):
    if not os.path.exists(filename):
        print(f"Ошибка: файл {filename} не найден")
        return None

    result = set()
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Разделяем строку на элементы (по пробелам или запятым)
                elements = line.replace(',', ' ').split()

                if len(elements) == 1:
                    result.add(parse(elements[0]))
                else:
                    result.add(tuple(parse(elem) for elem in elements))
    except Exception as e:
        print(f"Ошибка чтения файла {filename}: {e}")
        return None

    return result

def input_set_manual():
    print("Введите элементы множества (по одному на строке).")
    print("Для завершения введите пустую строку:")

    result = set()
    while True:
        line = input("> ").strip()
        if not line:
            break

        elements = line.replace(',', ' ').split()
        if len(elements) == 1:
            result.add(parse(elements[0]))
        else:
            result.add(tuple(parse(elem) for elem in elements))

    return result

def format_item(item):
    if isinstance(item, tuple):
        return f"({', '.join(str(x) for x in item)})"
    return str(item)

def print_result(result, title):
    print(f"\n{title}:")
    if not result:
        print("  (пустое множество)")
    else:
        # Сортировка для удобства
        try:
            sorted_result = sorted(result, key=lambda x: str(x))
        except:
            sorted_result = list(result)
        for item in sorted_result:
            print(f"  {format_item(item)}")
    print("-" * 60)

def start_calc():
    print("\nВыберите способ ввода данных:")
    print("  1 - Загрузить из файлов")
    print("  2 - Ввести вручную")

    print("-" * 10)

    choice_input = input("Ваш выбор (1/2): ").strip()

    if choice_input == '1':
        file1 = input("Введите путь к первому файлу: ").strip()
        file2 = input("Введите путь ко второму файлу: ").strip()

        A = get_set(file1)
        B = get_set(file2)

        if A is None or B is None:
            print("Ошибка загрузки файлов. Завершение работы.")
            return
    else:
        print("\nВвод первого множества")
        A = input_set_manual()
        print("\nВвод второго множества")
        B = input_set_manual()

    print(f"Множество A ({len(A)} элементов):")
    for item in sorted(list(A), key=lambda x: str(x)):
        print(f"  {format_item(item)}")

    print(f"\nМножество B ({len(B)} элементов):")
    for item in sorted(list(B), key=lambda x: str(x)):
        print(f"  {format_item(item)}")

    print("-" * 10)

    # Флаг выхода
    running = True

    while running:
        print("Доступные операции:")
        print("  1 - Объединение (A ∪ B)")
        print("  2 - Пересечение (A ∩ B)")
        print("  3 - Вычитание (A - B)")
        print("  4 - Декартово произведение (A × B)")
        print("  5 - Выборка (фильтрация)")
        print("  6 - Проекция (выбор столбца)")
        print("  7 - Соединение")
        print("  8 - Деление")
        print("  0 - Выход")
        print("-" * 10)

        choice = input("Выберите операцию (0-8): ").strip()

        # Выход по флагу 0
        if choice == '0' or choice.lower() == 'exit':
            print("Выход из программы...")
            running = False
            continue

        if choice not in [str(i) for i in range(1, 9)]:
            print("Ошибка: неверный номер операции")
            continue

        # 1. Объединение
        if choice == '1':
            result = A | B
            print_result(result, "Объединение (A ∪ B)")

        # 2. Пересечение
        elif choice == '2':
            result = A & B
            print_result(result, "Пересечение (A ∩ B)")

        # 3. Вычитание
        elif choice == '3':
            result = A - B
            print_result(result, "Вычитание (A - B)")

        # 4. Декартово произведение
        elif choice == '4':
            result = {(a, b) for a in A for b in B}
            print_result(result, "Декартово произведение (A * B)")

        # 5. Выборка
        elif choice == '5':
            val = input("Введите значение для выборки: ").strip()
            val = parse(val)
            result = set()
            for row in A:
                if isinstance(row, tuple):
                    if val in row:
                        result.add(row)
                else:
                    if row == val:
                        result.add(row)
            print_result(result, f"Выборка по значению '{val}'")

        # 6. Проекция
        elif choice == '6':
            try:
                col = int(input("Введите номер столбца (0, 1, ...): ").strip())
                result = set()
                for row in A:
                    if isinstance(row, tuple) and col < len(row):
                        result.add(row[col])
                    elif not isinstance(row, tuple) and col == 0:
                        result.add(row)
                print_result(result, f"Проекция на столбец {col}")
            except ValueError:
                print("Ошибка: номер столбца должен быть целым числом")
            except Exception as e:
                print(f"Ошибка при выполнении проекции: {e}")

       # 7. Соединение
        elif choice == '7':
            if not A or not B:
                print_result(set(), "Соединение (пустые множества)")
                continue

            first_a = next(iter(A))
            first_b = next(iter(B))

            len_a = 1 if not isinstance(first_a, tuple) else len(first_a)
            len_b = 1 if not isinstance(first_b, tuple) else len(first_b)

            print(f"\nСтруктура: A (len={len_a}), B (len={len_b})")

            # Простые множества -> пересечение
            if len_a == 1 and len_b == 1:
                result = A & B
                print_result(result, "Соединение (пересечение)")

            # Кортежи: соединение по a[-1] == b[0]
            elif len_a >= 2 and len_b >= 2:
                result = {a + b[1:] for a in A for b in B
                          if isinstance(a, tuple) and isinstance(b, tuple) and a[-1] == b[0]}
                print_result(result, "Соединение (natural join)")

            # A - кортежи, B - простые элементы
            elif len_a >= 2 and len_b == 1:
                result = set()
                for a in A:
                    if isinstance(a, tuple):
                        for b in B:
                            if a[-1] == b:
                                result.add(a[:-1] + (b,))
                print_result(result, "Соединение (A - кортежи, B - значения)")

            # A - простые элементы, B - кортежи
            elif len_a == 1 and len_b >= 2:
                result = set()
                for a in A:
                    for b in B:
                        if isinstance(b, tuple) and a == b[0]:
                            result.add((a,) + b[1:])
                print_result(result, "Соединение (A - значения, B - кортежи)")

            else:
                print("Не удалось выполнить соединение")

        # 8. Деление
        elif choice == '8':
            if not B:
                print("Ошибка: деление на пустое множество невозможно")
                continue

            if not A:
                print_result(set(), "Деление")
                continue

            first_a = next(iter(A))
            first_b = next(iter(B))

            len_a = 1 if not isinstance(first_a, tuple) else len(first_a)
            len_b = 1 if not isinstance(first_b, tuple) else len(first_b)

            # Простые множества -> пересечение
            if len_a == 1 and len_b == 1:
                result = A & B
                print_result(result, "Деление (пересечение)")

            # Деление: поиск id, у которых есть все значения из B
            elif len_a >= 2 and len_b >= 1:
                # Требуемые значения из B
                if len_b == 1:
                    required_values = B
                else:
                    required_values = {b[0] for b in B}

                # Уникальные id из A
                ids = {a[0] for a in A}
                result = set()

                for i in ids:
                    # Значения, связанные с id i
                    related_values = {a[-1] for a in A if a[0] == i}
                    if required_values.issubset(related_values):
                        result.add(i)

                print_result(result, "Деление")

            else:
                print(f"Деление невозможно: A (len={len_a}), B (len={len_b})")

def main():
    print("КАЛЬКУЛЯТОР МНОЖЕСТВ")
    print("\nФормат ввода данных:")
    print("  - Одиночные элементы: просто число или текст")
    print("  - Кортежи: элементы разделяются пробелами или запятыми")
    print("    Пример: A 1  или  x,b")

    start_calc()

if __name__ == "__main__":
    main()
