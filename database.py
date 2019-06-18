from collections import defaultdict
class database:
    def __init__(self):
        self.database = [{}]
        self.cc = [{}]

    def begin(self):
        self.database.append(dict(self.database[-1]))
        self.cc.append(dict(self.cc[-1]))

    def rollback(self):
        if len(self.database) >= 2:
            self.database.pop()
            self.cc.pop()
            return 0
        else:
            return 1

    def set(self, key, value):
        self.database[-1][key] = value
        if value not in self.cc[-1]:
            self.cc[-1][value] = 0
        self.cc[-1][value] += 1

    def unset(self, key):
        if key in self.database[-1]:
            value = self.database[-1][key]
            del self.database[-1][key]
            del self.cc[-1][value]

    def get(self, key):
        if key in self.database[-1]:
            return self.database[-1][key]
        else:
            return None

    def count(self, value):
        if value in self.cc[-1]:
            return self.cc[-1][value]
        else:
            return 0

    def commit(self):
        t = {}
        while len(self.database) >=2:
            each = self.database.pop()
            c = self.cc.pop()
            for key in each:
                if key not in t:
                    self.database[0][key] = each[key]
                    t[key] = 1
                    if each[key] not in self.cc[0]:
                        self.cc[0][each[key]] = 0
                    self.cc[0][each[key]] += 1


db = database()
output = []
def process():
    string = input()
    while string != "END":
        strings = string.split()
        action, key, value = strings[0],strings[1] if len(strings) >= 2 else None,strings[2] if len(strings) == 3 else None
        #print (action, key, value)
        func = getattr(db, action.lower())
        if action == "SET":
            func(key, value)
        if action == "BEGIN":
            func()
        if action == "ROLLBACK":
            if func() == 1:
                output.append("INVALID ROLLBACK")
        if action == "UNSET":
            func(key)
        if action == "GET":
            output.append(str("NULL" if func(key) == None else func(key)))
        if action == "COMMIT":
            func()
        if action == "COUNT":
            #print (action, key, value, func)
            output.append(str(func(key)))
        string = input()

process()
#print ("".ljust(8, "="))
print ("\n".join(output))
