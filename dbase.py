'''
'''
import os

FNAME = "passwd.txt"
FRESHNAME = "fresh.txt"

class Database:
    def count(self, input):
        n = 0
        with open(FNAME) as f:
            while True:
                line = f.readline()
                if not line:
                    break
                name, passwd = line.split("\t", 1)
                if name.startswith(input):
                    n += 1
        return n

    def filter(self, input, offs, count):
        print("filter", input, offs, count)
        result = []
        batch_started = False
        with open(FNAME) as f:
            i = 0
            while True:
                line = f.readline()
                if not line:
                    break
                name = line.split("\t", 1)[0]
                if name.startswith(input):
                    batch_started = True
                else:
                    if batch_started:
                        break
                    else:
                        continue
                if i < offs:
                    i += 1
                    continue
                result.append(name)
                i += 1
                if i >= offs + count:
                    break
        return result

    def get(self, input):
        for fname in [FRESHNAME, FNAME]:
            with open(fname) as f:
                while True:
                    line = f.readline()
                    if not line:
                        break
                    name, passwd = line.split("\t", 1)
                    if name == input:
                        return passwd.rstrip()
        return None

    def put(self, new_name, new_password):
        new_line = f"{new_name}\t{new_password}\n"
        try:
            with open(FRESHNAME) as f:
                with open(FRESHNAME + "~", "w") as out:
                    written = False
                    while True:
                        line = f.readline()
                        if not line:
                            break
                        name, passwd = line.split("\t", 1)
                        if name < new_name:
                            out.write(line)
                        elif name >= new_name:
                            if not written:
                                out.write(new_line)
                                written = True
                            out.write(line)
                    if not written:
                        out.write(new_line)
            os.rename(FRESHNAME + "~", FRESHNAME)
        except OSError:
            with open(FRESHNAME, "w") as out:
                out.write(new_line)

    def favs(self, offs=0, count=-1):
        print("favs", offs, count)
        result = []
        try:
            with open("favs.txt") as f:
                i = 0
                while True:
                    line = f.readline()
                    if not line:
                        break
                    if i < offs:
                        i += 1
                        continue
                    result.append(line.rstrip())
                    i += 1
                    if count > 0 and i >= offs + count:
                        break
        except OSError:
            pass
        return result

    def add_fav(self, name):
        favs = set(self.favs())
        favs.add(name)
        with open("favs.txt", "w") as f:
            sorted_favs = sorted(favs)
            for name in sorted_favs:
                f.write(name + "\n")

