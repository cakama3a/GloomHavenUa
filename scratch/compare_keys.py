
import csv

def get_keys(filename):
    keys = []
    with open(filename, 'r', encoding='utf-8') as f:
        # We read manually because the files might have weird quoting or newlines
        for line in f:
            if ',' in line:
                key = line.split(',')[0].strip()
                if key and key != 'Keys':
                    keys.append(key)
    return keys

en_keys = get_keys(r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\English\Solo_EN.csv')
ua_keys = get_keys(r'c:\Users\cakam\Documents\GitHub\GloomHavenUa\LangPacks\Solo.csv')

missing_in_ua = set(en_keys) - set(ua_keys)
missing_in_en = set(ua_keys) - set(en_keys)

print(f"Total EN keys: {len(en_keys)}")
print(f"Total UA keys: {len(ua_keys)}")
print(f"Missing in UA: {sorted(list(missing_in_ua))}")
print(f"Missing in EN: {sorted(list(missing_in_en))}")
