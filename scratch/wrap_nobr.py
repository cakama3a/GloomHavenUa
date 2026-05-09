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

# Define the pattern to find mechanic phrases
# Examples: 
# "+4 АТАКА <sprite name=Attack>"
# "-X РУХ <sprite name=Move>"
# "ЛІКУВАННЯ <sprite name=Heal>"
# "ЩИТ <sprite name=Shield> *BShield*" (Wait, maybe we don't need the *BShield* part unless it's in EN)
# Let's just focus on matching the number (optional), the word, and the sprite.
# Actually, the user pointed out +4 Attack <sprite name=Attack>.

pattern = re.compile(r'((?:[-+]\d+|[-+][Xx]\s*)?(?:АТАКА|РУХ|ЩИТ|ЛІКУВАННЯ|ДАЛЬНІСТЬ|ВІДПЛАТА|ОГЛУШЕННЯ|ПАРАЛІЧ|РОЗЗБРОЄННЯ|ОТРУЄННЯ|РАНА|СУМ\'ЯТТЯ|НЕВИДИМІСТЬ|ПОСИЛЕННЯ|ПРОКЛЯТТЯ|БЛАГОСЛОВЕННЯ)\s*<sprite name=[A-Za-z_]+>)')

for row in data:
    if len(row) < 2:
        new_data.append(row)
        continue
    
    text = row[1]
    orig_text = text
    
    # We want to wrap matches with <nobr>...</nobr> IF they are NOT already wrapped.
    # A simple way: remove all <nobr> around our exact pattern matches first, then add them back.
    # But wait, what if <nobr> wraps MORE than just our pattern?
    # e.g., <nobr>+1 АТАКА <sprite name=Attack> and +1 РУХ <sprite name=Move></nobr>
    # If we blindly wrap, we'd get <nobr><nobr>...</nobr> ...</nobr> which is bad.
    
    # Let's find matches that don't have <nobr> before them.
    # We can do this with a replacement function that checks the context.
    def repl(m):
        match_str = m.group(1)
        # Check if match_str is already surrounded by <nobr> in the orig text
        # Since we use re.sub, we can't easily check context without lookarounds.
        # But lookbehind for <nobr> is easy: (?<!<nobr>)
        return match_str
        
    # Better approach: 
    # Just remove <nobr> and </nobr> exactly around the pattern if present, then always wrap it.
    # e.g. <nobr>+1 АТАКА <sprite name=Attack></nobr> -> +1 АТАКА <sprite name=Attack> -> <nobr>+1 АТАКА <sprite name=Attack></nobr>
    # What if it's <nobr>+1 АТАКА <sprite name=Attack> something</nobr>? 
    # It's safer to just do a negative lookbehind and lookahead.
    
    # Let's replace:
    # (?<!<nobr>)((?:[-+]\d+|[-+][Xx])?\s*(?:АТАКА|РУХ|ЩИТ|ЛІКУВАННЯ|ДАЛЬНІСТЬ|ВІДПЛАТА|ОГЛУШЕННЯ|ПАРАЛІЧ|РОЗЗБРОЄННЯ|ОТРУЄННЯ|РАНА|СУМ\'ЯТТЯ|НЕВИДИМІСТЬ|ПОСИЛЕННЯ|ПРОКЛЯТТЯ|БЛАГОСЛОВЕННЯ)\s*<sprite name=[A-Za-z_]+>)(?!</nobr>)
    # Wait, the number part can be separated by a space.
    
    regex = r'(?<!<nobr>)((?:[-+]\d+|[-+][Xx])\s+(?:АТАКА|РУХ|ЩИТ|ЛІКУВАННЯ|ДАЛЬНІСТЬ|ВІДПЛАТА)\s*<sprite name=[A-Za-z_]+>)(?!</nobr>)'
    text = re.sub(regex, r'<nobr>\1</nobr>', text)
    
    # Also for cases without numbers, if they stand alone and should be wrapped.
    # Wait, in EN, does just "Attack <sprite name=Attack>" get wrapped?
    # e.g. "023_B,You may treat all <nobr>Move <sprite name=Move></nobr> abilities as <nobr>Attack <sprite name=Attack></nobr> abilities"
    # Yes, they do.
    regex2 = r'(?<!<nobr>)((?:АТАКА|РУХ|ЩИТ|ЛІКУВАННЯ|ДАЛЬНІСТЬ|ВІДПЛАТА|ОГЛУШЕННЯ|ПАРАЛІЧ|РОЗЗБРОЄННЯ|ОТРУЄННЯ|РАНА|СУМ\'ЯТТЯ|НЕВИДИМІСТЬ|ПОСИЛЕННЯ|ПРОКЛЯТТЯ|БЛАГОСЛОВЕННЯ)\s*<sprite name=[A-Za-z_]+>)(?!</nobr>)'
    # But wait, we shouldn't wrap if it's already inside a larger <nobr> block!
    # If the text has <nobr>... АТАКА <sprite name=Attack> ...</nobr>, the negative lookbehind (?<!<nobr>) will succeed because the immediately preceding chars aren't "<nobr>". This would nest <nobr> tags!
    
    # Let's fix this properly.
    # For every match, check if it's inside <nobr>...</nobr> anywhere in the string.
    
    def repl_safe(m):
        start = m.start()
        # Count <nobr> and </nobr> before start
        nobr_count = text[:start].count('<nobr>')
        end_nobr_count = text[:start].count('</nobr>')
        if nobr_count > end_nobr_count:
            # We are inside a <nobr> block
            return m.group(1)
        else:
            return f'<nobr>{m.group(1)}</nobr>'

    # Find all pattern occurrences and replace safely
    # Pattern: optional number, space, mechanic, space, sprite
    full_pattern = r'((?:[-+]\d+|[-+][Xx])?\s*(?:АТАКА|РУХ|ЩИТ|ЛІКУВАННЯ|ДАЛЬНІСТЬ|ВІДПЛАТА|ОГЛУШЕННЯ|ПАРАЛІЧ|РОЗЗБРОЄННЯ|ОТРУЄННЯ|РАНА|СУМ\'ЯТТЯ|НЕВИДИМІСТЬ|ПОСИЛЕННЯ|ПРОКЛЯТТЯ|БЛАГОСЛОВЕННЯ)\s*<sprite name=[A-Za-z_]+>)'
    
    # We must iterate since `text` changes and `m.start()` would shift if we do it manually.
    # re.sub can take a function. The function receives the match object on the ORIGINAL string.
    # This is safe because Python's re.sub evaluates matches sequentially.
    
    text = re.sub(full_pattern, repl_safe, text)
    
    if text != orig_text:
        changes += 1
        
    new_data.append([row[0], text])

with open(out_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
    writer.writerows(new_data)

print(f'Made <nobr> wrapping changes in {changes} rows.')
