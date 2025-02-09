#!/bin/python

import xxtea

def validate(plain_password, enc_password):
    enc = xxtea.encryptToBase64(plain_password, plain_password)
    return enc == enc_password


if __name__ == '__main__':
    passwd = input("Please enter your password: ")
    enc = xxtea.encryptToBase64(passwd, passwd)

    print("Encrypted", enc)
    print("Validated", validate(passwd, enc))
