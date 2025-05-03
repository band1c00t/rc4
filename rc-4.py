def KSA(key):
    """
    Key Scheduling Algorithm (KSA)
    Initialisiert und permutiert das S-Array mit dem Schlüssel
    """
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    """
    Pseudo-Random Generation Algorithm (PRGA)
    Erzeugt einen unendlichen Strom von Keystream-Bytes aus dem S-Array
    """
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256] #Berechnng des Keystream-Bytes
        yield K #Keystream-Byte zurückgeben

def rc4(key, data):
    S = KSA(key)
    keystream = PRGA(S)
    return bytes([c ^ next(keystream) for c in data])

def main():
    print('RC-4 Algorithm')
    print('==============')
    print("1. Verschlüsseln")
    print("2. Entschlüsseln")
    print("3. Beenden")
    while True:
        wahl = input("Bitte Option wählen (1, 2 oder 3): ")
        if wahl == '1':
            text = input("Gib den Klartext ein: ").encode("utf-8")
            key = input("Schlüssel: ").encode("utf-8")
            ciphertext = rc4(key, text)
            decrypted = rc4(key,ciphertext)
            print("\nVerschlüsselter Text:", ciphertext.hex())
            print("Entschlüsselter Text:", decrypted)
            print("Verwendeter Schlüssel:", key)
        elif wahl == '2':
            ciphertext = bytes.fromhex(input("Gib den Geheimtext hexadezimal ein: "))
            key = input("Gib den Key ein: ").encode("utf-8")
            decrypted = rc4(key,ciphertext)
            print(f"Entschlüsselter Text: {decrypted}")
        elif wahl == '3':
            break
        else:
            print("Ungültige Auswahl. Bitte 1, 2 oder 3 eingeben.")

if __name__ == '__main__':
    main()