import sqlite3
import datetime


class Storage:
    maximumСontent = 10000
    contents = 0

    def __init__(self, id, grain, weitght, data):
        self.id = id
        self.grain = grain
        self.weitght = weitght
        self.addContents(int(weitght))
        self.data = data

    @property
    def getMaximumСontent(self):
        return int(self.maximumСontent)

    @property
    def getId(self):
        return self.id

    @property
    def getGrain(self):
        return self.grain

    @property
    def getWeight(self):
        return self.weitght

    @property
    def getData(self):
        return self.data

    @getData.setter
    def setData(self, data):
        self.data = data

    @getGrain.setter
    def setGrain(self, grain):
        self.grain = grain

    @getWeight.setter
    def setWeitght(self, weitght):
        self.weitght = str(weitght)

    @classmethod
    def getContents(cls):
        return int(cls.contents)

    @classmethod
    def addContents(cls, con):
        temp = cls.contents + con
        if temp > cls.maximumСontent:
            print("Not enough space in stock")
        else:
            cls.contents += con

    def __add__(self, other):
        return self(self.id, self.grain, str(int(self.weitght) + int(other.weitght)), self.data)

    def __sub__(self, other):
        return self.weitght - other.weitght

    def __iadd__(self, other):
        self.weitght += int(other.weitght)
        return self

    def __eq__(self, other):
        return self.grain == other.grain and int(self.weitght) == int(other.weitght) and self.data == other.data

    def __ne__(self, other):
        return self.grain != other.grain and int(self.weitght) != int(other.weitgh) and self.data != other.dara

    def __lt__(self, other):
        return int(self.weitght) < int(other.weitght)

    def __gt__(self, other):
        return int(self.weitght) > int(other.weitght)


class DataBase:
    def __init__(self, nameDB, table):
        self.nameDB = nameDB
        self.table = table
        self.conn = sqlite3.connect(self.nameDB + '.bd')
        self.curs = self.conn.cursor()
        self.curs.execute("""SELECT * FROM {}""".format(self.table))
        self.temp = self.curs.fetchall()
        self.grainStorage = []
        for i in self.temp:
            self.grainStorage.append(Storage(i[0], i[1], int(i[2]), i[3]))

    def showFullData(self):
        print("id\t\tgrain\t\tweitght\t\tdata")
        for i in self.grainStorage:
            print("{}\t\t{}\t\t{}\t\t\t{}".format(i.getId, i.getGrain, i.getWeight, i.setData))
        print("In stock in total " + str(Storage.getContents()) + " grain!")

    def push(self, storage):
        self.grainStorage.append(storage)

    def remove(self, storage):
        try:
            self.grainStorage.remove(storage)
            print("delete item")
        except ValueError:
            print("Item not deleted!")

    def pop(self, index):
        try:
            self.grainStorage.pop(index)
        except IndexError:
            print("eroor id " + str(index) + " does not exist!")

    def find(self, storage):
        for i in self.grainStorage:
            if storage in self.grainStorage:
                return i.getId
        return None

    def add(self, id, data):
        temp = self.grainStorage[id].setWeitght + data
        if temp > self.grainStorage[id].getMaximumСontent:
            print("Not enough space in stock")
        else:
            self.grainStorage[id].setWeitght += data
            Storage.addContents(data)



    def subtract(self, id, data):
        self.grainStorage[id].setWeitght -= data

    def index(self, index):
        return self.grainStorage[index]

    @property
    def size(self):
        return len(self.grainStorage)

    def commit(self):
        self.conn.commit()

    def save(self):
        self.curs.execute("""SELECT * FROM {}""".format(self.table))
        self.curs.execute("DELETE FROM {}".format(self.table))
        for i in self.grainStorage:
            self.curs.execute("""INSERT INTO {}
                        VALUES({},'{}', '{}', '{}')""".format(str(self.table), int(i.getId), str(i.getGrain), str(i.getWeight),
                                                           str(i.getData)))
        self.conn.commit()

    def __del__(self):
        self.save()
        self.curs.close()
        self.conn.close()


if __name__ == "__main__":
    bd = DataBase("GrainStorage", "storage")
    choice = "start"

    while choice != "exit":
        print("""lead to
                display all data "all data"
                to make grain "add"
                withdraw the grain "subtract"
                add kind of grain "add kind"
                remove the kind of grain "subtract kind"
                save data "save"
                to exit "exit""")
        choice = input("-->")
        if choice == "all data":
            bd.showFullData()
        if choice == "add":
            id = input("ID - ")
            data = input("+ ")
            bd.add(int(id) - 1, int(data))
        if choice == "subtract":
            id = input("ID - ")
            data = input("+ ")
            bd.subtract(int(id) - 1, int(data))
        if choice == "add kind":
            grain = input("grain - ")
            weitght = input("weitght - ")
            new = Storage(bd.size + 1, grain, weitght, str(datetime.date.today()))
            bd.push(new)
        if choice == "subtract kind":
            id = input("ID -->")
            bd.pop(int(id) - 1)
        if choice == "save":
            bd.commit()
    bd.save()
