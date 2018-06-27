def SHA1(what):
    return openpgp.crypto.hash.sha1(what)

def concat(array1, array2):
    ret = __new__(Uint8Array(array1.length + array2.length))
    j = 0
    for i in range(0, array1.length):
        ret[j] = array1[i]
        j += 1
    for i in range(0, array2.length):
        ret[j] = array2[i]
        j += 1
    return ret

def SHA1HMAC(key, data):
    BLOCK_SIZE = 64

    if key.length > BLOCK_SIZE:
        key = SHA1(key)
    else:
        newKey = __new__(Uint8Array(BLOCK_SIZE))
        for i in range(0, newKey.length):
            newKey[i] = key[i] if i < key.length else 0
        key = newKey

    O_KEY_PAD = __new__(Uint8Array(BLOCK_SIZE))
    I_KEY_PAD = __new__(Uint8Array(BLOCK_SIZE))
    for i in range(0, BLOCK_SIZE):
        O_KEY_PAD[i] = 0x5c ^ key[i]
        I_KEY_PAD[i] = 0x36 ^ key[i]

    hashI = SHA1(concat(I_KEY_PAD, data))
    hashO = SHA1(concat(O_KEY_PAD, hashI))
    return hashO
