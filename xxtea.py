'''
https://github.com/fidcz/xxtea-python/blob/main/xxtea.py
'''
import re

if hasattr(re, 'findall'):
    re_findall = re.findall
else:
    def re_findall(pattern, string):
        matches = []
        regex = re.compile(pattern)
        pos = 0

        while True:
            match = regex.search(string, pos)
            if not match:
                break
            if match.groups():
                matches.append(match.groups() if len(match.groups()) > 1 else match.group(1))
            else:
                matches.append(match.group(0))
            pos = match.end()
        
        return matches

def int_overflow(val):
    maxint = 2147483647
    if not -maxint-1 <= val <= maxint:
        val = (val + (maxint + 1)) % (2 * (maxint + 1)) - maxint - 1
    return val

def unsigned_right_shift(n,i):
    if n<0:
        n &= 0xFFFFFFFF
    if i<0:
        return -int_overflow(n << abs(i))
    return int_overflow(n >> i)

def fromCharCode(a, *b):
    return chr(a%65536) + ''.join([chr(i%65536) for i in b])

def btoa(enStr):
    base64EncodeChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    i = j = 0
    length = len(enStr)
    r = length % 3
    length = length - r
    l = int_overflow(int(length / 3) << 2)
    if r > 0:
        l += 4
    buf = [''] * l
    while i < length:
        charAt1 = int_overflow(ord(enStr[i]) << 16)
        i += 1
        charAt2 = int_overflow(ord(enStr[i]) << 8)
        i += 1
        charAt3 = ord(enStr[i])
        i += 1
        c = charAt1 | charAt2 | charAt3
        
        buf[j] = base64EncodeChars[c >> 18] + base64EncodeChars[c >> 12 & 0x3f] + base64EncodeChars[c >> 6 & 0x3f] + base64EncodeChars[c & 0x3f]
        j += 1
    
    if r == 1:
        c = ord(enStr[i])
        i += 1
        buf[j] = base64EncodeChars[c>>2] + base64EncodeChars[int_overflow((c & 0x03) << 4)] + '=='
        j += 1
    elif r == 2:
        charAt1 = int_overflow(ord(enStr[i]) << 8)
        i += 1
        charAt2 = ord(enStr[i])
        i += 1
        c = charAt1 | charAt2
        buf[j] = base64EncodeChars[c >> 10] + base64EncodeChars[c >> 4 & 0x3f] + base64EncodeChars[int_overflow((c & 0x0f) << 2)] + '='
    return ''.join(buf)

def atob(deStr):
    base64DecodeChars = [
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 62, -1, -1, -1, 63,
        52, 53, 54, 55, 56, 57, 58, 59, 60, 61, -1, -1, -1, -1, -1, -1,
        -1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
        15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, -1, -1, -1, -1, -1,
        -1, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
        41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, -1, -1, -1, -1, -1
    ]

    length = len(deStr)
    if length % 4 != 0: return ''
    if re_findall(r'[^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\+\/\=]', deStr): return ''

    if deStr[-2] == '=':
        r = 1
    elif deStr[-1] == '=':
        r = 2
    else:
        r = 0
    
    l = length
    if r > 0: l -= 4
    l = (l >> 2) * 3 + r
    out = [''] * l

    i = j = 0
    while i < length:
        c1 = base64DecodeChars[ord(deStr[i])]
        i += 1
        if c1 == -1: break

        c2 = base64DecodeChars[ord(deStr[i])]
        i += 1
        if c2 == -1: break

        out[j] = fromCharCode(int_overflow(c1 << 2) | ((c2 & 0x30) >> 4))
        j += 1

        c3 = base64DecodeChars[ord(deStr[i])]
        i += 1
        if c3 == -1: break

        out[j] = fromCharCode(int_overflow((c2 & 0x0f) << 4) | ((c3 & 0x3c) >> 2))
        j += 1

        c4 = base64DecodeChars[ord(deStr[i])]
        i += 1
        if c4 == -1: break

        out[j] = fromCharCode(int_overflow((c3 & 0x03) << 6) | c4)
        j += 1
    
    return ''.join(out)

def toBinaryString(v, includeLength:bool):
    length = len(v)
    n = int_overflow(length << 2)
    # print(n)
    if includeLength:
        m = v[length - 1]
        n -= 4
        if m < n - 3 or m > n:
            return None
        n = m
    i = 0
    while i < length:
        v[i] = fromCharCode(
            v[i] & 0xFF, 
            unsigned_right_shift(v[i], 8) & 0xFF, 
            unsigned_right_shift(v[i], 16) & 0xFF, 
            unsigned_right_shift(v[i], 24) & 0xFF, 
        )
        i += 1
    result = ''.join(v)
    if includeLength:
        return result[0:n]
    return result

def mx(sum, y, z, p, e, k):
    return ((unsigned_right_shift(z, 5) ^ y << 2) + (unsigned_right_shift(y, 3) ^ z << 4)) ^ ((sum ^ y) + (k[p & 3 ^ e] ^ z))

def int32(i):
    return int_overflow(i & 0xFFFFFFFF)

def encryptUint32Array(v, k):
    length = len(v)
    n = length - 1
    z = v[n]
    sum = 0

    q = (int(6 + 52 / length) | 0)
    while q > 0:
        sum = int32(sum + 0x9E3779B9)
        e = unsigned_right_shift(sum, 2) & 3
        p = 0
        while p < n:
            y = v[p+1]
            z = v[p] = int32(v[p] +  mx(sum, y, z, p, e, k))
            p += 1
        y = v[0]
        z = v[n] = int32(v[n] + mx(sum, y, z, n, e, k))
        q -= 1
    return v

def decryptUint32Array(v, k):
    length = len(v)
    n = length - 1
    y = v[0]
    q = int(6 + 52 / length)

    sum = int32(q * 0x9E3779B9)
    while sum != 0:
        e = unsigned_right_shift(sum, 2) & 3
        
        p = n
        while p > 0:
            z = v[p - 1]
            y = v[p] = int32(v[p] - mx(sum, y, z, p, e, k))

            p -= 1
        
        z = v[n]
        y = v[0] = int32(v[0] - mx(sum, y, z, 0, e, k))

        sum = int32(sum - 0x9E3779B9)
    return v

def fixk(k):
    if len(k) < 4:
        k.extend([0]*(4-len(k)))
    return k

def toUint32Array(bs, includeLength:bool):
    length = len(bs)
    n = length >> 2
    if (length & 3) != 0:
        n += 1
    
    # v = None
    if includeLength:
        v = [0] * (n+1)
        v[n] = length
    else:
        v = [0] * n
    
    for i in range(length):
        # print('i:' + str(i))
        # print(v[i >> 2])
        # print(ord(bs[i]))
        # print(ord(bs[i]) << ((i & 3) << 3))
        v[i >> 2] = v[i >> 2] | int_overflow(ord(bs[i]) << int_overflow((i & 3) << 3))
    return v

def utf8Encode(enStr):
    if re_findall(r'^[\x00-\x7f]*$', enStr): return enStr
    buf = [None] * len(enStr)
    n = len(enStr)
    i = 0
    j = 0
    while i < n:
        # print(i,j)
        codeUnit = ord(enStr[i])
        if codeUnit < 0x80:
            buf[j] = enStr[i]
        elif codeUnit < 0x800:
            buf[j] = fromCharCode(0xC0 | (codeUnit >> 6), 0x80 | (codeUnit & 0x3F))
        elif codeUnit < 0xD800 or codeUnit > 0xDFFF:
            buf[j] = fromCharCode(0xE0 | (codeUnit >> 12), 0x80 | ((codeUnit >> 6) & 0x3F), 0x80 | (codeUnit & 0x3F))
        else:
            if i + 1 < n:
                nextCodeUnit = ord(enStr[i+1])
                if codeUnit < 0xDC00 and 0xDC00 <= nextCodeUnit and nextCodeUnit <= 0xDFFF:
                    rune = (((codeUnit & 0x03FF) << 10) | (nextCodeUnit & 0x03FF)) + 0x010000
                    buf[j] = fromCharCode(0xF0 | ((rune >> 18) & 0x3F), 0x80 | ((rune >> 12) & 0x3F), 0x80 | ((rune >> 6) & 0x3F), 0x80 | (rune & 0x3F))
                    i += 1

        i += 1
        j += 1
    return ''.join(buf)

def utf8DecodeShortString(bs, n):
    charCodes = [0] * n
    i = off = 0
    
    length = len(bs)
    while i < n and off < length:
        unit = ord(bs[off])
        off += 1

        switch = unit >> 4
        if switch in [0, 1, 2, 3 , 4, 5, 6, 7]:
            charCodes[i] = unit
        elif switch in [12, 13]:
            if off < length:
                charCodes[i] = int_overflow((unit & 0x1F) << 6) | (ord(bs[off]) & 0x3F)
                off += 1
            else:
                Exception('Unfinished UTF-8 octet sequence')
        elif switch in [14]:
            if off + 1 < length:
                charAt1 = int_overflow((ord(bs[off]) & 0x3F) << 6)
                off += 1
                charAt2 = ord(bs[off]) & 0x3F
                off += 1
                charCodes[i] = int_overflow((unit & 0x0F) << 12) | charAt1 | charAt2
            else:
                Exception('Unfinished UTF-8 octet sequence')
        elif switch in [15]:
            if off + 2 < length:
                charAt1 = int_overflow((ord(bs[off]) & 0x3F) << 12)
                off += 1
                charAt2 = int_overflow((ord(bs[off]) & 0x3F) << 6)
                off += 1
                charAt3 = (ord(bs[off]) & 0x3F)
                off += 1
                rune = (int_overflow((unit & 0x07) << 18) | charAt1 | charAt2 | charAt3) - 0x10000
                if  0 <= rune and rune <= 0xFFFFF:
                    charCodes[i] = (((rune >> 10) & 0x03FF) | 0xD800)
                    i += 1
                    charCodes[i] = (rune & 0x03FF) | 0xDC00
                else:
                    Exception('Character outside valid Unicode')
            else:
                Exception('Unfinished UTF-8 octet sequence')
        else:
            Exception('Bad UTF-8 encoding')


        i += 1
    
    if i < n:
        charCodes = charCodes[:i]
    return fromCharCode(*charCodes)

def utf8DecodeLongString(bs, n):
    buf = []
    charCodes = [0] * 0x8000
    i = off = 0
    length = len(bs)
    while i < n and off < length:
        unit = ord(bs[off])
        off += 1
        switch = unit >> 4
        if switch in [0, 1, 2, 3, 4, 5, 6, 7]:
            charCodes[i] = unit
        elif switch in [12, 13]:
            if off < length:
                charCodes[i] = int_overflow((unit & 0x1F) << 6) | (ord(bs[off]) & 0x3F)
                off += 1
            else:
                Exception('Unfinished UTF-8 octet sequence')
        elif switch in [14]:
            if off + 1 < length:
                charAt1 = int_overflow((ord(bs[off]) & 0x3F) << 6)
                off += 1
                charAt2 = ord(bs[off]) & 0x3F
                off += 1
                charCodes[i] = int_overflow((unit & 0x0F) << 12) | charAt1 | charAt2
            else:
                Exception('Unfinished UTF-8 octet sequence')
        elif switch in [15]:
            if off + 2 < length:
                charAt1 = int_overflow((ord(bs[off]) & 0x3F) << 12)
                off += 1
                charAt2 = int_overflow((ord(bs[off]) & 0x3F) << 6)
                off += 1
                charAt3 = ord(bs[off]) & 0x3F
                off += 1
                rune = (int_overflow((unit & 0x07) << 18) | charAt1 | charAt2 | charAt3) - 0x10000
                if 0 <= rune and rune <= 0xFFFFF:
                    charCodes[i] = (((rune >> 100) & 0x03FF) | 0xD800)
                    i += 1
                    charCodes[i] = ((rune & 0x03FF) | 0xDC00)
                else:
                    Exception('Character outside valid Unicode')
            else:
                Exception('Unfinished UTF-8 octet sequence')
        else:
            Exception('Bad UTF-8 encoding')
    
        if i >= 0x7FFF -1:
            size = i + 1
            if len(charCodes) > size:
                charCodes = charCodes[:size]
            else:
                charCodes.extend([0] * (size - len(charCodes)))
            buf.append(fromCharCode(*charCodes))
            n -= size
            i = -1

        i += 1
    
    if i > 0:
        charCodes = charCodes[:i]
        buf.append(fromCharCode(*charCodes))
    
    return ''.join(buf)

def utf8Decode(bs, n=None):
    if not n or n < 0: n = len(bs)
    if n == 0: return ''
    if re_findall(r'^[\x00-\x7f]*$', bs) or not re_findall(r'^[\x00-\xff]*$', bs):
        if n == len(bs): return bs
        return bs[0:n]
    
    return utf8DecodeShortString(bs, n) if n < 0x7FFF else utf8DecodeLongString(bs, n)

def encrypt(strData, key):
    if not strData or len(strData) == 0: return strData
    strData = utf8Encode(strData)
    key = utf8Encode(key)
    return toBinaryString(encryptUint32Array(toUint32Array(strData, True), fixk(toUint32Array(key, False))), False)

def decrypt(strData, key):
    if not strData or len(strData) == 0:
        return strData
    key = utf8Encode(key)
    return utf8Decode(toBinaryString(decryptUint32Array(toUint32Array(strData, False), fixk(toUint32Array(key, False))), True))

def decryptFromBase64(strData, key):
    if not strData or len(strData) == 0:
        return strData
    return decrypt(atob(strData), key)

def encryptToBase64(strData, key):
    return btoa(encrypt(strData, key))

#if __name__ == '__main__':
def run():
    enString = 'Hello World!!!'
    Key = 'password'
    a = encryptToBase64(enString, Key)
    print(a)
    b = decryptFromBase64(a, 'password')
    print(b)
    print(enString == b)