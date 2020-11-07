import sqlite3

DB_PATH = '2_base_datos_objeto_currency.db'

class CurrencyDoesNotExists(Exception):
    pass

class CurrencyManager(object):

    def __init__(self, database = None):
        if not database:
            database = ':memory:'
        self.conn = sqlite3.connect(database)
        self.cursor = self.conn.cursor()

    def insert(self, obj):
        query = 'INSERT INTO currency VALUES ("{}", "{}", "{}")'.format(obj.code, obj.name, obj.symbol)
        self.cursor.execute(query)
        self.conn.commit()

    def get(self, code):
        query = 'SELECT * FROM currency WHERE code = "{}"'.format(code)
        self.cursor.execute(query)
        data = self.cursor.fetchone()
        if not data:
            raise CurrencyDoesNotExists("No existe la moneda de código {}".format(code))
        return Currency(code = data[0], name=data[1], symbol=data[2])

    def filter(self, **kwargs):
        code = kwargs.get('code')
        name = kwargs.get('name')
        symbol = kwargs.get('symbol')

        condition = ' WHERE '
        add_and = False
        add_condition = False

        if code:
            condition += 'code="{}" '.format(code)
            add_condition = True
            add_and = True
        if name:
            if add_and:
                condition += 'AND '
            condition += 'name="{}" '.format(name)
            add_condition = True
            add_and = True
        if symbol:
            if add_and:
                condition += 'AND '
            condition += 'symbol="{}" '.format(symbol)
            add_condition = True

        query = 'SELECT * FROM currency'
        if add_condition:
            query += condition
        
        self.cursor.execute(query)
        result = self.cursor.fetchall()

        currencies = []
        for data in result:
            currency = Currency(code=data[0], name =data[1], symbol = data[2])
            currencies.append(currency)

        return currencies

class Currency(object):
    "Currency Model"
    objects = CurrencyManager(DB_PATH)

    def __init__(self,code,name,symbol):
        self.code = code
        self.name = name
        self.symbol = symbol

    def __repr__(self):
        return u'{}'.format(self.name)

print(Currency.objects.get(code='ARS'))

print(Currency.objects.filter(code='EUR'))
print(Currency.objects.filter(name='Dolar'))
print(Currency.objects.filter(symbol='€'))

print(Currency.objects.filter())

#Currency.objects.get(code='ARS')
