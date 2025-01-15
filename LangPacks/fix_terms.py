import re
from pathlib import Path
import shutil

def determine_gender(text):
    """
    Визначає рід контексту на основі закінчень та слів
    """
    # Жіночі маркери
    female_markers = [
        r'\bвона\b', 
        r'\bїй\b',
        r'\bїї\b',
        r'[а-яіїє]ла\b',  # дієслова минулого часу
        r'[а-яіїє]лася\b',
        r'[а-яіїє]ачка\b',
        r'[а-яіїє]иця\b'
    ]
    
    # Чоловічі маркери
    male_markers = [
        r'\bвін\b',
        r'\bйому\b',
        r'\bйого\b',
        r'[а-яіїє]в\b',   # дієслова минулого часу
        r'[а-яіїє]вся\b'
    ]
    
    female_count = sum(1 for pattern in female_markers if re.search(pattern, text, re.IGNORECASE))
    male_count = sum(1 for pattern in male_markers if re.search(pattern, text, re.IGNORECASE))
    
    return 'female' if female_count > male_count else 'male'

def should_change_race_name(text, position, race_name):
    """
    Перевіряє, чи потрібно змінювати назву раси в даному контексті
    """
    # Перевіряємо, чи не є це частиною словосполучення "тіло [раси]"
    if re.search(r'тіло\s+' + race_name, text[max(0, position-10):position+len(race_name)+1]):
        return False
        
    # Перевіряємо, чи не є це присвійним прикметником
    if re.search(r'\b' + race_name + r'\s+(?:воїн|табір|поселення|зброя|армія|народ)\b', 
                text[position:position+30], re.IGNORECASE):
        return False
    
    # Додаткові перевірки контексту
    preceding_words = text[max(0, position-20):position].lower()
    if any(word in preceding_words for word in ['тіло', 'група', 'загін', 'армія']):
        return False
        
    return True

def fix_race_names(text):
    """
    Виправляє назви рас відповідно до роду та контексту
    """
    if not text:
        return text
    
    # Словник рас з формами чоловічого та жіночого роду
    races = {
        r'\bВалрат(?:а|у|ом|ові|і|е)?\b': {'male': 'Валрат', 'female': 'Валратка'},
        r'\bОрхід(?:а|у|ом|ові|і|е)?\b': {'male': 'Орхід', 'female': 'Орхідка'},
        r'\bКуатрил(?:а|у|ом|ові|і|е)?\b': {'male': 'Куатрил', 'female': 'Куатрилка'},
        r'\bЕстер(?:а|у|ом|ові|і|е)?\b': {'male': 'Естер', 'female': 'Естерка'},
        r'\bВермлінг(?:а|у|ом|ові|і|е)?\b': {'male': 'Вермлінг', 'female': 'Вермлінжка'},
        # Інокс потребує особливої обробки
        r'\bІнокс(?:а|у|ом|ові|і|е)?\b': {'male': 'Інокс', 'female': 'Інокска', 'keep_original': True}
    }
    
    # Визначаємо рід для всього тексту
    gender = determine_gender(text)
    
    # Замінюємо назви рас відповідно до роду
    for pattern, forms in races.items():
        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        for match in reversed(matches):  # Йдемо з кінця, щоб не зламати індекси
            start, end = match.span()
            original = match.group(0)
            
            # Перевіряємо контекст перед заміною
            if should_change_race_name(text, start, original):
                replacement = forms[gender]
                text = text[:start] + replacement + text[end:]
    
    return text

def process_csv(file_path):
    # Створюємо тимчасовий файл
    temp_path = file_path.with_suffix('.tmp')
    
    try:
        modified_lines = []
        changes_made = False
        
        # Читаємо оригінальний файл рядок за рядком
        with open(file_path, 'r', encoding='utf-8') as input_file:
            header = next(input_file)  # Читаємо заголовок
            modified_lines.append(header)  # Додаємо заголовок без змін
            
            for line in input_file:
                if ',' in line:  # Перевіряємо, що це валідний рядок з даними
                    # Знаходимо першу кому для розділення ключа та значення
                    split_index = line.find(',')
                    key = line[:split_index]
                    value = line[split_index + 1:]
                    
                    # Обробляємо текст
                    if value:
                        new_value = fix_race_names(value)
                        if new_value != value:
                            changes_made = True
                            print(f"\nЗміну застосовано в рядку {key}:")
                            print(f"Було: {value.strip()}")
                            print(f"Стало: {new_value.strip()}")
                        value = new_value
                    
                    # Зберігаємо модифікований рядок
                    modified_lines.append(f"{key},{value}")
                else:
                    modified_lines.append(line)  # Додаємо рядок без змін
        
        # Записуємо всі модифіковані рядки у тимчасовий файл
        with open(temp_path, 'w', encoding='utf-8', newline='') as output_file:
            output_file.writelines(modified_lines)
        
        # Замінюємо оригінальний файл
        if changes_made:
            shutil.move(str(temp_path), str(file_path))
            print("\nФайл успішно оновлено!")
            print(f"Оброблено {len(modified_lines) - 1} рядків")
        else:
            print("\nЗмін не було потрібно")
            Path(temp_path).unlink()
        
    except Exception as e:
        print(f"Помилка при обробці файлу: {str(e)}")
        if Path(temp_path).exists():
            Path(temp_path).unlink()
        raise

if __name__ == "__main__":
    file_path = Path("Main.csv")
    try:
        process_csv(file_path)
    except Exception as e:
        print(f"Критична помилка: {str(e)}")