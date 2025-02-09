import passpy
import sys

sys.path.append('.')
import xxtea

passkey = None

def show(e, out):
    key = store.get_key(e).split('\n', 1)[0]
    print(e, file=sys.stderr)
    enc = xxtea.encryptToBase64(key, passkey)
    out.write(f"{e}\t{enc}\n")

def sub(d, out):
    (dirs, entries) = store.list_dir(d)
    for _d in dirs:
        sub(_d, out)
    for e in entries:
        show(e, out)


if __name__ == '__main__':
    passkey = input("Gib deinen Schlüssel ein: ")
    with open("settings.toml", "w") as settings:
        enc = xxtea.encryptToBase64(passkey, passkey)
        settings.write(f'PV_PASSWORD = "{enc}"\n')
    store = passpy.Store()
    with open('passwd.txt', 'w') as out:
        sub('.', out)
