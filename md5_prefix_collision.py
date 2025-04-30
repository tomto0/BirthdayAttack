import hashlib
import os
from tqdm import tqdm

TARGET_BITS = 32  # 32-bit = 8 hex chars

seen = {}
i = 0

print("Suche nach MD5-Kollision im Präfix von %d Bit..." % TARGET_BITS)

while True:
    # zufällige semantikfreie Modifikation
    data = b"Vertrag Mietzins: 500 Euro\nKommentar: " + os.urandom(16)
    md5 = hashlib.md5(data).hexdigest()
    prefix = md5[:TARGET_BITS // 4]

    if prefix in seen:
        print(f"\nKollision gefunden bei Prefix: {prefix}")
        with open("doc1.bin", "wb") as f: f.write(seen[prefix])
        with open("doc2.bin", "wb") as f: f.write(data)
        print("Dateien gespeichert als doc1.bin und doc2.bin")
        break

    seen[prefix] = data
    i += 1
    if i % 1000 == 0:
        print(f"{i} Kandidaten getestet...", end="\r")
