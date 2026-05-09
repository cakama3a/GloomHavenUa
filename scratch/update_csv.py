import csv
import re
import sys

en_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\English\Main_EN.csv'
ua_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'
out_file = r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Main.csv'

# Let's map from what's potentially wrong in UA to what's right.
replacements = {
    '<sprite name=Attack> до атаки': 'АТАКА <sprite name=Attack>',
    'до атаки <sprite name=Attack>': 'АТАКА <sprite name=Attack>',
    '+1 <sprite name=Attack>': '+1 АТАКА <sprite name=Attack>',
    '+2 <sprite name=Attack>': '+2 АТАКА <sprite name=Attack>',
    '+3 <sprite name=Attack>': '+3 АТАКА <sprite name=Attack>',
    '+4 <sprite name=Attack>': '+4 АТАКА <sprite name=Attack>',
    '+5 <sprite name=Attack>': '+5 АТАКА <sprite name=Attack>',
    '+X <sprite name=Attack>': '+X АТАКА <sprite name=Attack>',
    '-1 <sprite name=Attack>': '-1 АТАКА <sprite name=Attack>',
    '-2 <sprite name=Attack>': '-2 АТАКА <sprite name=Attack>',

    '<sprite name=Move> до руху': 'РУХ <sprite name=Move>',
    'до руху <sprite name=Move>': 'РУХ <sprite name=Move>',
    '+1 <sprite name=Move>': '+1 РУХ <sprite name=Move>',
    '+2 <sprite name=Move>': '+2 РУХ <sprite name=Move>',
    '+3 <sprite name=Move>': '+3 РУХ <sprite name=Move>',
    '+4 <sprite name=Move>': '+4 РУХ <sprite name=Move>',
    '-1 <sprite name=Move>': '-1 РУХ <sprite name=Move>',
    '-2 <sprite name=Move>': '-2 РУХ <sprite name=Move>',

    '<sprite name=Range> до дальності': 'ДАЛЬНІСТЬ <sprite name=Range>',
    'до дальності <sprite name=Range>': 'ДАЛЬНІСТЬ <sprite name=Range>',
    '+1 <sprite name=Range>': '+1 ДАЛЬНІСТЬ <sprite name=Range>',
    '+2 <sprite name=Range>': '+2 ДАЛЬНІСТЬ <sprite name=Range>',
    '-1 <sprite name=Range>': '-1 ДАЛЬНІСТЬ <sprite name=Range>',

    '+1 <sprite name=Heal>': '+1 ЛІКУВАННЯ <sprite name=Heal>',
    '+2 <sprite name=Heal>': '+2 ЛІКУВАННЯ <sprite name=Heal>',
    '+3 <sprite name=Heal>': '+3 ЛІКУВАННЯ <sprite name=Heal>',
    '+4 <sprite name=Heal>': '+4 ЛІКУВАННЯ <sprite name=Heal>',

    '+1 <sprite name=Shield>': '+1 ЩИТ <sprite name=Shield>',
    '+2 <sprite name=Shield>': '+2 ЩИТ <sprite name=Shield>',

    '""АТАКА <sprite name=Attack>""': '""АТАКА <sprite name=Attack>""',
    '""РУХ <sprite name=Move>""': '""РУХ <sprite name=Move>""',
    'Плутовка': 'Шахрайка',
    'Чарівниця': 'Чародійниця',
    'Плетуча чари': 'Чародійниця',
}

regex_replacements = [
    (r'<nobr>([-+]\d+|[-+]X)\s*<sprite name=Attack></nobr>\s*до атаки', r'<nobr>\1 АТАКА <sprite name=Attack></nobr>'),
    (r'<nobr>([-+]\d+|[-+]X)\s*<sprite name=Move></nobr>\s*до руху', r'<nobr>\1 РУХ <sprite name=Move></nobr>'),
    (r'<nobr>([-+]\d+|[-+]X)\s*<sprite name=Range></nobr>\s*до дальності', r'<nobr>\1 ДАЛЬНІСТЬ <sprite name=Range></nobr>'),
    (r'<nobr>([-+]\d+|[-+]X)\s*<sprite name=Heal></nobr>\s*до лікування', r'<nobr>\1 ЛІКУВАННЯ <sprite name=Heal></nobr>'),

    (r'до атаки\s*<nobr>([-+]\d+|[-+]X)\s*<sprite name=Attack></nobr>', r'<nobr>\1 АТАКА <sprite name=Attack></nobr>'),
    (r'до руху\s*<nobr>([-+]\d+|[-+]X)\s*<sprite name=Move></nobr>', r'<nobr>\1 РУХ <sprite name=Move></nobr>'),
    (r'до дальності\s*<nobr>([-+]\d+|[-+]X)\s*<sprite name=Range></nobr>', r'<nobr>\1 ДАЛЬНІСТЬ <sprite name=Range></nobr>'),

    (r'([-+]\d+|[-+]X) АТАКА <sprite name=Attack> до атаки', r'\1 АТАКА <sprite name=Attack>'),
    (r'([-+]\d+|[-+]X) РУХ <sprite name=Move> до руху', r'\1 РУХ <sprite name=Move>'),

    (r'(?i)\bОглушення\s*<sprite name=Stun>', r'ОГЛУШЕННЯ <sprite name=Stun>'),
    (r'(?i)\bПараліч\s*<sprite name=Immobilize>', r'ПАРАЛІЧ <sprite name=Immobilize>'),
    (r'(?i)\bРоззброєння\s*<sprite name=Disarm>', r'РОЗЗБРОЄННЯ <sprite name=Disarm>'),
    (r'(?i)\bОтруєння\s*<sprite name=Poison>', r'ОТРУЄННЯ <sprite name=Poison>'),
    (r'(?i)\bРана\s*<sprite name=Wound>', r'РАНА <sprite name=Wound>'),
    (r'(?i)\bСум\'яття\s*<sprite name=Muddle>', r'СУМ\'ЯТТЯ <sprite name=Muddle>'),
    (r'(?i)\bНевидимість\s*<sprite name=Invisible>', r'НЕВИДИМІСТЬ <sprite name=Invisible>'),
    (r'(?i)\bПосилення\s*<sprite name=Strengthen>', r'ПОСИЛЕННЯ <sprite name=Strengthen>'),
    (r'(?i)\bПрокляття\s*<sprite name=Curse>', r'ПРОКЛЯТТЯ <sprite name=Curse>'),
    (r'(?i)\bБлагословення\s*<sprite name=Bless>', r'БЛАГОСЛОВЕННЯ <sprite name=Bless>'),
    (r'(?i)\bВідновити\s*<sprite name=Recover>', r'ВІДНОВИТИ <sprite name=Recover>'),
    (r'(?i)\bОновити\s*<sprite name=Refresh>', r'ОНОВИТИ <sprite name=Refresh>'),
    (r'(?i)\bЗдобич\s*<sprite name=Loot>', r'ЗДОБИЧ <sprite name=Loot>'),
    (r'(?i)\bВідплата\s*<sprite name=Retaliate>', r'ВІДПЛАТА <sprite name=Retaliate>'),
    (r'(?i)\bЩит\s*<sprite name=Shield>', r'ЩИТ <sprite name=Shield>'),

    # Character names inside text
    (r'(?i)\bПлутовка\b', r'Шахрайка'),
    (r'(?i)\bЧарівниця\b', r'Чародійниця'),
    (r'(?i)\bПлетуча чари\b', r'Чародійниця'),
]

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
    
    for old, new in replacements.items():
        text = text.replace(old, new)
        
    for pat, rep in regex_replacements:
        text = re.sub(pat, rep, text)
        
    # Also strictly align tags if EN has exact "[mechanic] <sprite name=[mechanic]>" structure
    # However we did this mostly with regex above.
        
    if text != orig_text:
        changes += 1
        
    new_data.append([row[0], text])

with open(out_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerows(new_data)

print(f'Made changes in {changes} rows.')
