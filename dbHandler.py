import sqlite3


connection = sqlite3.connect('botDB.db', check_same_thread=False)

myCursor = connection.cursor()


'''
c.execute("""CREATE TABLE priceList(
        item text,
        price integer
    )""")

myCursor.execute("""CREATE TABLE priceListPL(
        item text,
        price integer
    )""")

connection.commit()

myCursor.execute("""CREATE TABLE priceListRU(
        item text,
        price integer
    )""")

connection.commit()


connection.commit()

myCursor.execute("INSERT INTO priceListPL VALUES ('database portfolioPL1', 228000)")
myCursor.execute("INSERT INTO priceListPL VALUES ('database portfolioPL2', 8000)")
myCursor.execute("INSERT INTO priceListRU VALUES ('database portfolioRU1', 12)")
myCursor.execute("INSERT INTO priceListRU VALUES ('database portfolioRU2', 4600)")
myCursor.execute("INSERT INTO clientsChatIDs VALUES (4600)")
'''

def get_pricesPL():
    myCursor.execute("SELECT * FROM priceListPL")
    outputString = ''
    for data in myCursor.fetchall():
        outputString += str(data[0]) + ' ' + str(data[1]) + 'zł\n'
    return outputString

def get_pricesRU():
    myCursor.execute("SELECT * FROM priceListRU")
    outputString = ''
    for data in myCursor.fetchall():
        outputString += str(data[0]) + ' ' + str(data[1]) + 'zł\n'
    return outputString

def write_order(order):
    myCursor.execute("INSERT INTO orders VALUES ('{}')".format(order))
    connection.commit()

