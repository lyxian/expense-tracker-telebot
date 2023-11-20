from db import DB
from testing import d

tableName = ['categories', 'users', 'records']

testPayloadTable = [
    tableName[0], {
        'username': 'abc',
        'id': 123
    }
]

testPayloadRecord = [
    tableName[1], {
        'id': 123,
        'category': 'earn',
        'amount': 10.00,
        'timestamp': '2023-11-20 01:24:00'   # YYYY-MM-DD HH:MM:SS
    }
]

if __name__ == '__main__':
    db = DB(dbName='test', logFile='tmp.log')

    input('ok')
    db.runInsert('users', d['users'])
    input('ok')
    db.runInsert('records', d['records'])
    input('ok')
    db.runSelect(tableName[0])
    input('ok')
    db.runSelect(tableName[1])
    input('ok')
    db.runSelect(tableName[2])

    if 0:
        input('ok')
        db.runSelect(tableName[0])
        input('ok')
        db.runInsert(*testPayloadTable)
        input('ok')
        db.runSelect(tableName[1])
        input('ok')
        db.runInsert(*testPayloadRecord)