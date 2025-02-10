import os
import sys

sys.path.append('.')
import xxtea

passkey = None

def print_entries():
    with open('passwd.tsv') as inp:
        with open('passwd.txt', 'w') as out:
            print("Reading...", file=sys.stderr)
            while True:
                l = inp.readline()
                if not l:
                    break
                name, passwd = l.split('\t', 1)
                passwd = passwd.rstrip()
                enc = xxtea.encryptToBase64(passwd, passkey)
                out.write(f"{name}\t{enc}\n")
    print("Done.", file=sys.stderr)

if __name__ == '__main__':
    passkey = input("Gib deinen Schlüssel ein: ")
    print_entries()

