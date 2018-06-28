def Scrypt(password, salt):
    def scryptFactory(resolve, reject):
        scrypt(password, salt, {
            "N": 262144,
            "r": 8,
            "p": 1,
            "dkLen": 128,
            "encoding": "hex",
        }, resolve)
    return __new__(Promise(scryptFactory))
