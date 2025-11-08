def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.
    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""
    # PUT YOUR CODE HERE
    for letter in plaintext:
        if letter .islower():
            ciphertext = ciphertext + chr(((ord(letter)-97+shift)%26)+97)
        elif letter .isupper():
            ciphertext = ciphertext + chr(((ord(letter)-65+shift)%26)+65)
        else:
            ciphertext = ciphertext + letter
    return ciphertext


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.
    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""
    # PUT YOUR CODE HERE
    for letter in ciphertext:
        if letter.islower():
            plaintext = plaintext + chr(((ord(letter) - 97 - shift) % 26) + 97)
        elif letter.isupper():
            plaintext = plaintext + chr(((ord(letter) - 65 - shift) % 26) + 65)
        else:
            plaintext = plaintext + letter
    return plaintext