import csv
import re

ua_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'
out_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'

with open(ua_file, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    data = list(reader)

new_data = [header]
changes = 0

for row in data:
    if len(row) < 2:
        new_data.append(row)
        continue
    
    text = row[1]
    orig_text = text
    
    # Remove redundant trailing strings
    text = re.sub(r'(<sprite name=Attack>[^>]*?)\s*до атаки', r'\1', text)
    text = re.sub(r'(<sprite name=Move>[^>]*?)\s*до руху', r'\1', text)
    text = re.sub(r'(<sprite name=Range>[^>]*?)\s*до дальності', r'\1', text)
    text = re.sub(r'(<sprite name=Heal>[^>]*?)\s*до лікування', r'\1', text)
    
    # Remove leading
    text = re.sub(r'до атаки\s*(<nobr>.*?<sprite name=Attack>)', r'\1', text)
    text = re.sub(r'до руху\s*(<nobr>.*?<sprite name=Move>)', r'\1', text)
    
    if text != orig_text:
        changes += 1
        
    new_data.append([row[0], text])

with open(out_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerows(new_data)

print(f'Cleaned up {changes} rows.')
