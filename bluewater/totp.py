from .hmac import SHA1HMAC

leftpad = lambda s, l, pad: ("".join([pad for i in range(0, l-len(s))])) + s
dec2hex = lambda s: ('0' if s < 16 else '') + Math.round(s).toString(16)
hex2dec = lambda s: parseInt(s, 16)
hex2buffer = lambda h: openpgp.util.hex_to_Uint8Array(h)
buffer2hex = lambda b: openpgp.util.Uint8Array_to_hex(b)

def base32tohex(base32):
    base32chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
    bits = ""
    ret = ""
    for i in range(0, base32.length):
        val = base32chars.indexOf(base32.charAt(i).toUpperCase())
        bits += leftpad(val.toString(2), 5, '0')
    for i in range(0, bits.length, 4):
        chunk = bits[i:i+4]
        ret += parseInt(chunk, 2).toString(16)
    return ret 

class TOTP:

    epoch = lambda: Math.round(__new__(Date()).getTime() / 1000.0) 

    def __init__(self, secret):
        self.secret = secret

    def __str__(self):
        key = base32tohex(self.secret)
        epoch = self.epoch() 
        time = leftpad(dec2hex(Math.floor(epoch / 30)), 16, '0')

        hmac = buffer2hex(SHA1HMAC(hex2buffer(key), hex2buffer(time)))

        offset = hex2dec(hmac[-1:])
        part1 = hmac[0:2*offset]
        part2 = hmac[2*offset:][:8] 
        part3 = hmac[offset * 2 + 8:][:hmac.length - offset]

        otp = str((hex2dec(hmac[offset * 2:][:8]) & hex2dec('7fffffff')))
        otp = otp[-6:]
        return otp

    def countdown(self):
        epoch = self.epoch()
        return 30 - (epoch % 30)
