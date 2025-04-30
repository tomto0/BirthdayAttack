import hashlib
import os

# === Konfiguration ===

# Anzahl der gewünschten übereinstimmenden Bits im MD5-Hash (z. B. 48 Bit = 12 hex Zeichen)
PREFIX_BITS = 48

# Dictionary zum Speichern von bereits generierten Hash-Präfixen
seen = {}

# Zähler für die Anzahl getesteter Varianten
i = 0

print(f"Suche nach Kollision direkt in .txt-Dateien (auf den ersten {PREFIX_BITS} Bit)...")

# === Schritt 1: Schleife zur Generierung von Eingaben und Hash-Kollisionen ===

while True:
    # Erzeuge 16 zufällige Bytes als semantikneutralen Kommentaranhang
    neutral_tail = os.urandom(16)

    # Basistext, der in beiden Dateien gleich bleibt
    base_text = b"Vertrag: Der Mieter zahlt monatlich 1000 Euro.\nKommentar: "

    # Kombiniere festen Text mit zufälligem Kommentarblock
    full_data = base_text + neutral_tail

    # Berechne den MD5-Hash der aktuellen Daten
    md5 = hashlib.md5(full_data).hexdigest()

    # Extrahiere den gewünschten Präfix (z. B. 48 Bit → 12 hex-Zeichen)
    prefix = md5[:PREFIX_BITS // 4]

    # Wenn der Präfix bereits im Dictionary existiert, wurde eine Kollision gefunden
    if prefix in seen:
        # Speichere beide kollidierenden Inhalte in Dateien
        with open("final1.txt", "wb") as f:
            f.write(seen[prefix])
        with open("final2.txt", "wb") as f:
            f.write(full_data)
        print(f"Kollision gefunden bei Präfix: {prefix}")
        print(f"Insgesamt getestete Varianten: {i}")
        break

    # Wenn der Präfix noch nicht gesehen wurde, speichere die Daten
    seen[prefix] = full_data
    i += 1

    # Alle 1000 Versuche Fortschritt ausgeben
    if i % 1000 == 0:
        print(f"{i} Varianten getestet...", end="\r")


# === Schritt 2: Vergleiche die Hashes der erzeugten Dateien ===

# Funktion zur Berechnung des MD5-Hashs einer Datei
def md5_of_file(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

# Berechne die Hashwerte beider Dateien
hash1 = md5_of_file("final1.txt")
hash2 = md5_of_file("final2.txt")

# Ausgabe der Hashwerte zur Kontrolle
print("\nMD5 der generierten .txt-Dateien:")
print(f"final1.txt: {hash1}")
print(f"final2.txt: {hash2}")

# Überprüfe, ob der gewünschte Präfix identisch ist
if hash1[:PREFIX_BITS // 4] == hash2[:PREFIX_BITS // 4]:
    print(f"Gleicher {PREFIX_BITS}-Bit-MD5-Präfix: {hash1[:PREFIX_BITS // 4]}")
else:
    print("Kein gemeinsamer Hash-Präfix!")
