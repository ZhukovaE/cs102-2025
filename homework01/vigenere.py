def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.
    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    keyword = keyword.upper()
    key_len = len(keyword)
    for i in range(len(plaintext)):
        letter = plaintext[i]
        if letter.isalpha():
            key_letter = keyword[i % key_len]
            shift = ord(key_letter) - ord("A")
        if letter.isupper():
            ciphertext = ciphertext + chr(((ord(letter) - 65 + shift) % 26) + 65)
        elif letter.islower():
            ciphertext = ciphertext + chr(((ord(letter) - 97 + shift) % 26) + 97)
        else:
            ciphertext = ciphertext + letter
    return ciphertext


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.
    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    >>> decrypt_vigenere("tfvzzvwkeaqv lq aqvpzf", "lsci")
    'introduction to python'
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    keyword = keyword.upper()
    key_len = len(keyword)
    for i in range(len(ciphertext)):
        letter = ciphertext[i]
        if letter.isalpha():
            key_letter = keyword[i % key_len]
            shift = ord(key_letter) - ord("A")
        if letter.isupper():
            plaintext = plaintext + chr(((ord(letter) - 65 - shift) % 26) + 65)
        elif letter.islower():
            plaintext = plaintext + chr(((ord(letter) - 97 - shift) % 26) + 97)
        else:
            plaintext = plaintext + letter
    return plaintext
