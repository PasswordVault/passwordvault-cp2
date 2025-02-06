import os
import sys
import xxtea
import datetime

key = '123'

inname = 'passwd.txt'
outname = 'passwd.py'

now = datetime.datetime.now().replace(microsecond=0).isoformat(' ')

header = f'''
# Passwords ({now})
entries = {{ 
'''

footer = '''
}
'''

def print_entries():
    with open('passwd.txt', 'rt') as f:
        print("Reading...", file=sys.stderr)
        while True:
            l = f.readline()
            if not l:
                break
            name, passwd = l.split('\t', 1)
            passwd = passwd.rstrip()

            enc = xxtea.encryptToBase64(passwd, key)
            print(f'  "{name}": "{enc}",')
        print("Done.", file=sys.stderr)

if __name__ == '__main__':
    print(header)
    print_entries()
    print(footer)
