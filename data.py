import os
import pprint
from Mongo_class import Mongo



mongo_uri = os.getenv('mongo_uri')

m = Mongo(mongo_uri, 'collatz')
query = { 'range': 10000000}
print(query)
result = m.find_doc(query)

for r in result:
    test = r['type']
    bound = r['range']
    t_time = r['total_time']

    print(f'type: {test} range: {bound} total_time: {t_time}')
