import os
import sys
import xxtea

key = '123'

def print_entries():
    with open('passwd.raw') as inp:
        with open('passwd.txt', 'w') as out:
            print("Reading...", file=sys.stderr)
            while True:
                l = inp.readline()
                if not l:
                    break
                name, passwd = l.split('\t', 1)
                passwd = passwd.rstrip()
                enc = xxtea.encryptToBase64(passwd, key)
                out.write(f"{name}\t{enc}\n")
    print("Done.", file=sys.stderr)

if __name__ == '__main__':
    print_entries()

