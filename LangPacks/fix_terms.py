import csv
import re
from pathlib import Path
import shutil

def fix_term_case(text, term, upper_case=True):
    if not text:
        return text
    
    upper_case_markers = [
        r'\"[^\"]*{}[^\"]*\"'.format(term),
        r'<nobr>[^<]*{}[^<]*</nobr>'.format(term),
        r'<b>[^<]*{}[^<]*</b>'.format(term),
        r'<link=[^>]*>[^<]*{}[^<]*</link>'.format(term),
        r'<color=[^>]*>[^<]*{}[^<]*</color>'.format(term)
    ]
    
    for marker in upper_case_markers:
        matches = re.finditer(marker, text, re.IGNORECASE)
        for match in matches:
            matched_text = match.group(0)
            if term.lower() in matched_text.lower():
                new_text = re.sub(
                    r'\b{}\b'.format(term), 
                    term.upper() if upper_case else term.lower(), 
                    matched_text, 
                    flags=re.IGNORECASE
                )
                text = text.replace(matched_text, new_text)
    
    return text

def process_csv(file_path):
    terms_to_fix = {
        'атака': 'АТАКА',
        'щит': 'ЩИТ',
        'отруєння': 'ОТРУЄННЯ',
        'лікування': 'ЛІКУВАННЯ',
        'прикликання': 'ПРИКЛИКАННЯ',
        'прокляття': 'ПРОКЛЯТТЯ',
        'рух': 'РУХ',
        'здобич': 'ЗДОБИЧ',
        'поштовх': 'ПОШТОВХ',
        'притягнути': 'ПРИТЯГНУТИ',
        'пробиття': 'ПРОБИТТЯ',
        'відплата': 'ВІДПЛАТА',
        'посилення': 'ПОСИЛЕННЯ',
        "сум'яття": "СУМ'ЯТТЯ",
        'роззброєння': 'РОЗЗБРОЄННЯ',
        'оглушення': 'ОГЛУШЕННЯ',
        'параліч': 'ПАРАЛІЧ',
        'рана': 'РАНА',
        'благословення': 'БЛАГОСЛОВЕННЯ',
        'стрибок': 'СТРИБОК',
        'політ': 'ПОЛІТ',
        'спожити': 'СПОЖИТИ',
        'наповнити': 'НАПОВНИТИ',
        'постійний ефект': 'ПОСТІЙНИЙ ЕФЕКТ',
        'дальність': 'ДАЛЬНІСТЬ',
        'ціль': 'ЦІЛЬ',
        'зона': 'ЗОНА',
        'елемент': 'ЕЛЕМЕНТ'
    }
    
    # Створюємо тимчасовий файл
    temp_path = file_path.with_suffix('.tmp')
    
    try:
        modified_lines = []
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
                        for term, upper_term in terms_to_fix.items():
                            value = fix_term_case(value, term)
                    
                    # Зберігаємо модифікований рядок
                    modified_lines.append(f"{key},{value}")
                else:
                    modified_lines.append(line)  # Додаємо рядок без змін
        
        # Записуємо всі модифіковані рядки у тимчасовий файл
        with open(temp_path, 'w', encoding='utf-8', newline='') as output_file:
            output_file.writelines(modified_lines)
        
        # Замінюємо оригінальний файл
        shutil.move(str(temp_path), str(file_path))
        print("Файл успішно оновлено!")
        print(f"Оброблено {len(modified_lines) - 1} рядків")
        
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