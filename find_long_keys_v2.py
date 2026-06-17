import csv
import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

ENGLISH_DIR = r"c:\Users\cakam\Documents\GitHub\GloomHavenUa\English"
UA_DIR = r"c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks"

FILE_PAIRS = [
    ("Main_EN.csv", "Main.csv"),
    ("Lions_EN.csv", "Lions.csv"),
    ("Consoles_EN.csv", "Consoles.csv"),
    ("Solo_EN.csv", "Solo.csv"),
]

# Ability card key patterns: 
#   NNN_T, NNN_B, NNN_T_1, NNN_B_2, JOTL_NNN_T, JOTL_NNN_B, etc.
ABILITY_KEY_PATTERN = re.compile(
    r'^(?:[A-Za-z]+_)?\d+_[TB](?:_\d+)?$'
)

def strip_tags(text):
    """Remove XML/HTML tags and sprite references to measure actual visible text length."""
    cleaned = re.sub(r'<[^>]+>', '', text)
    return cleaned

def load_entries(filepath):
    entries = {}
    with open(filepath, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return entries
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip() if len(row) > 1 else ""
                if key:
                    entries[key] = value
    return entries

def is_ability_key(key):
    """Check if a key is an ability card key (NNN_T, NNN_B, JOTL_NNN_T, etc.)."""
    return bool(ABILITY_KEY_PATTERN.match(key))

def main():
    output_lines = []
    output_lines.append("=== СПИСОК КАРТОК ЗДІБНОСТЕЙ ДЛЯ ОПТИМІЗАЦІЇ ===")
    output_lines.append("Включено ЛИШЕ картки здібностей персонажів (ключі типу NNN_T, NNN_B, JOTL_NNN_T тощо)")
    output_lines.append("Критерії включення:")
    output_lines.append("  1. UA >10% довше за EN (при видимому тексті UA >30 символів)")
    output_lines.append("  2. Видимий текст UA >100 символів (довгий текст на картці потребує стислості)")
    output_lines.append("Format: File | Key | EN Len | UA Len | Excess % | Visible UA chars | Reason")
    output_lines.append("")
    
    total_keys = 0
    criteria1_only = 0
    criteria2_only = 0
    both_count = 0
    
    for en_file, ua_file in FILE_PAIRS:
        en_path = os.path.join(ENGLISH_DIR, en_file)
        ua_path = os.path.join(UA_DIR, ua_file)
        
        if not os.path.exists(en_path):
            output_lines.append(f"WARNING: English file not found: {en_path}")
            continue
        if not os.path.exists(ua_path):
            output_lines.append(f"WARNING: Ukrainian file not found: {ua_path}")
            continue
        
        en_entries = load_entries(en_path)
        ua_entries = load_entries(ua_path)
        
        file_keys = []
        
        for key in ua_entries:
            if key not in en_entries:
                continue
            
            # ONLY ability card keys
            if not is_ability_key(key):
                continue
            
            en_text = en_entries[key]
            ua_text = ua_entries[key]
            
            en_len = len(en_text)
            ua_len = len(ua_text)
            
            en_visible = strip_tags(en_text)
            ua_visible = strip_tags(ua_text)
            en_visible_len = len(en_visible)
            ua_visible_len = len(ua_visible)
            
            if en_len == 0:
                continue
            
            excess_pct = ((ua_len - en_len) / en_len) * 100
            
            # Criterion 1: UA >10% longer than EN, and visible text > 30 chars
            criterion1 = (excess_pct > 10 and ua_visible_len > 30)
            
            # Criterion 2: Long visible text on ability card (>100 chars)
            criterion2 = (ua_visible_len > 100)
            
            if criterion1 or criterion2:
                reasons = []
                if criterion1:
                    reasons.append(f">10% довше (+{excess_pct:.1f}%)")
                if criterion2:
                    reasons.append(f"довгий текст ({ua_visible_len} символів)")
                
                reason_str = " + ".join(reasons)
                
                file_keys.append({
                    'key': key,
                    'en_len': en_len,
                    'ua_len': ua_len,
                    'excess_pct': excess_pct,
                    'en_text': en_text,
                    'ua_text': ua_text,
                    'en_visible_len': en_visible_len,
                    'ua_visible_len': ua_visible_len,
                    'criterion1': criterion1,
                    'criterion2': criterion2,
                    'reason': reason_str,
                })
        
        if file_keys:
            output_lines.append("")
            output_lines.append(f"--- FILE: {ua_file} ---")
            
            for entry in file_keys:
                c1 = entry['criterion1']
                c2 = entry['criterion2']
                
                if c1 and c2:
                    both_count += 1
                elif c1:
                    criteria1_only += 1
                elif c2:
                    criteria2_only += 1
                
                total_keys += 1
                
                output_lines.append(
                    f"{ua_file} | {entry['key']} | "
                    f"EN: {entry['en_len']} | UA: {entry['ua_len']} | "
                    f"{'+' if entry['excess_pct'] >= 0 else ''}{entry['excess_pct']:.1f}% | "
                    f"Visible UA: {entry['ua_visible_len']} | "
                    f"[{entry['reason']}]"
                )
                output_lines.append(f"  EN: {entry['en_text']}")
                output_lines.append(f"  UA: {entry['ua_text']}")
                output_lines.append("")
    
    output_lines.append("")
    output_lines.append("=" * 60)
    output_lines.append(f"Загальна кількість карток здібностей для оптимізації: {total_keys}")
    output_lines.append(f"  - Лише за критерієм 1 (>10% довше, видимий текст >30): {criteria1_only}")
    output_lines.append(f"  - Лише за критерієм 2 (видимий текст >100 символів): {criteria2_only}")
    output_lines.append(f"  - За обома критеріями: {both_count}")
    
    output_path = r"c:\Users\cakam\Documents\GitHub\GloomHavenUa\long_keys_list.txt"
    with open(output_path, mode='w', encoding='utf-8') as f:
        f.write("\n".join(output_lines))
    
    print(f"Done! Written {total_keys} ability card keys to {output_path}")
    print(f"  - Criterion 1 only (>10% longer): {criteria1_only}")
    print(f"  - Criterion 2 only (long visible text >100): {criteria2_only}")  
    print(f"  - Both criteria: {both_count}")

if __name__ == "__main__":
    main()
