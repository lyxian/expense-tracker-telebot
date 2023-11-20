# generate testing.json payload
from random import randint, random
import json
import os

def randTimestamp():
    return '2023-11-{:0>2}'.format(randint(1,30))
    # return '2023-11-{:0>2} {:0>2}:{:0>2}:00'.format(randint(1,30), randint(0,23), randint(0,59))

if os.path.exists('testing.json'):
    with open('testing.json', 'r') as file:
        d = json.load(file)
else:
    d = {
        'users': [
            {'username': 'abc', 'id': 123},
            {'username': 'def', 'id': 456}
        ],
        'records': []
    }

    ids = [123, 456]
    cat = ['dining', 'shopping', 'transport', 'entertainment', 'miscellaneous']
        
    for i in range(50):
        timestamp = randTimestamp()
        d['records'].append({
            'id': ids[randint(0,1)],
            'category': randint(1,len(cat)),
            'amount': '{:.2f}'.format(random()*100),   # '%.2f' % (x.random()*100),
            'timestamp': timestamp   # YYYY-MM-DD HH:MM:SS
        })

    with open('testing.json', 'w') as file:
        file.write(json.dumps(d, indent=2))