import csv
import re

en_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\English\Main_EN.csv'
ua_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'
out_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'

en_data = {}
with open(en_file, 'r', encoding='utf-8') as f:
    for row in csv.reader(f):
        if len(row) >= 2: en_data[row[0]] = row[1]

with open(ua_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

new_data = [header]
changes = 0

def clean_nested_nobr(text):
    # If text has <nobr>...<nobr>...</nobr>...</nobr>
    # We can just iterate through and keep only the first level of <nobr>
    result = []
    level = 0
    i = 0
    while i < len(text):
        if text[i:i+6] == '<nobr>':
            if level == 0:
                result.append('<nobr>')
            level += 1
            i += 6
        elif text[i:i+7] == '</nobr>':
            level = max(0, level - 1)
            if level == 0:
                result.append('</nobr>')
            i += 7
        else:
            result.append(text[i])
            i += 1
    return ''.join(result)

for row in data:
    if len(row) < 2:
        new_data.append(row)
        continue
    
    k = row[0]
    ua_text = row[1]
    orig_text = ua_text
    en_text = en_data.get(k, '')
    
    # 1. Clean nested <nobr>
    ua_text = clean_nested_nobr(ua_text)
    
    # 2. Capitalization check
    # Find first alphabetical char in EN
    en_first_char_match = re.search(r'[a-zA-Z]', en_text)
    if en_first_char_match:
        en_is_upper = en_first_char_match.group(0).isupper()
        
        # Find first alphabetical char in UA (Cyrillic)
        ua_first_char_match = re.search(r'[а-яА-ЯєЄіІїЇґҐ]', ua_text)
        if ua_first_char_match:
            ua_char_idx = ua_first_char_match.start()
            ua_char = ua_first_char_match.group(0)
            
            if en_is_upper and ua_char.islower():
                # Capitalize
                ua_text = ua_text[:ua_char_idx] + ua_char.upper() + ua_text[ua_char_idx+1:]
            elif not en_is_upper and ua_char.isupper():
                # Wait, if EN is lowercase, should UA be lowercase? 
                # Yes, to match exactly. e.g. "instead..." -> "замість..."
                ua_text = ua_text[:ua_char_idx] + ua_char.lower() + ua_text[ua_char_idx+1:]
                
    if ua_text != orig_text:
        changes += 1
        
    new_data.append([row[0], ua_text])

with open(out_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerows(new_data)

print(f'Made capitalization and nobr fixes in {changes} rows.')
