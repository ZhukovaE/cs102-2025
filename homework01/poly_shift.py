def encrypt_poly_shift(plaintext, odd_shift, even_shift):
    ciphertext = ""
    for i in range(len(plaintext)):
        symbol = plaintext[i]
        position = i + 1

        if position % 2 == 1:
            shift = odd_shift
        else:
            shift = even_shift

        if symbol.isalpha():
            if symbol.islower():
                ciphertext += chr((ord(symbol) - ord("а") + shift) % 32 + ord("а"))
            elif symbol.isupper():
                ciphertext += chr((ord(symbol) - ord("А") + shift) % 32 + ord("А"))
        else:
            ciphertext += symbol
    return ciphertext
