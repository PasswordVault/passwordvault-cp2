'''
Convert a CSV export from LastPass
'''
import csv
import re
from urllib.parse import urlparse
import sys

sys.path.append('.')
import xxtea

passkey = None

def convert(fname):
    with open(fname) as csvfile:
        reader = csv.DictReader(csvfile)
        with open('passwd.txt', 'w') as out:
            for row in reader:
                url = row['url']
                parsed_url = urlparse(url)
                host = parsed_url.hostname.replace('www.', '')
                name = re.sub(r'\.de$|\.com$', '', host)
                username = row['username'].strip()
                if username:
                    name += '/' + username
                password = row['password']

                enc = xxtea.encryptToBase64(password, passkey)
                out.write(f"{name}\t{enc}\n")
    print("Done.", file=sys.stderr)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f"Aufruf: {sys.argv[0]} <CSV-Datei>")
        sys.exit(-1)
    passkey = input("Gib deinen Schlüssel ein: ")
    convert(sys.argv[1])
