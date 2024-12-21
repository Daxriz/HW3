import tomllib  # Встроенная библиотека для Python 3.11+
import sys

def parse_toml_to_custom_language(toml_data):
    """
    Преобразует TOML-данные в формат учебного конфигурационного языка.
    :param toml_data: Словарь, полученный из TOML.
    :return: Строка в формате учебного конфигурационного языка.
    """
    result = []

    # Рекурсивная функция для обработки структуры TOML
    def process_item(key, value, indent=0):
        prefix = " " * indent
        if isinstance(value, dict):
            # Обработка таблиц
            result.append(f"{prefix}def {key} := {{")
            for subkey, subvalue in value.items():
                process_item(subkey, subvalue, indent + 2)
            result.append(f"{prefix}}}")
        elif isinstance(value, list):
            # Обработка массивов
            items = ". ".join(map(str, value))
            result.append(f"{prefix}def {key} := {{ {items}. }}")
        elif isinstance(value, str):
            # Обработка строк
            result.append(f"{prefix}def {key} := '{value}'")
        else:
            # Обработка чисел
            result.append(f"{prefix}def {key} := {value}")

    for key, value in toml_data.items():
        process_item(key, value)

    return "\n".join(result)

def main():
    # Проверка наличия аргументов
    if len(sys.argv) != 3:
        print("Usage: Main.py input_file output_file")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        # Открытие TOML файла в бинарном режиме
        with open(input_file, 'rb') as f:
            toml_data = tomllib.load(f)

        # Преобразование TOML-данных в учебный конфигурационный язык
        custom_language_data = parse_toml_to_custom_language(toml_data)

        # Запись результата в выходной файл
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(custom_language_data)

        print(f"Файл успешно преобразован и сохранён в {output_file}")
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
