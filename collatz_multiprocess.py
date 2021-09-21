import time
import argparse
import os
import multiprocessing
from Mongo_class import Mongo
from pymongo import MongoClient
from pprint import pprint

#argument information 
parser = argparse.ArgumentParser( description='collatz conjecture calculation')
parser.add_argument( '-b', type=int, action='store', required=True,  help='upper bound for collatz calculation')
parser.add_argument('-t', type=int, action='store', required = True, help='number of processes')
args = parser.parse_args()
#retrieve database connection information
mongo_uri = os.getenv('mongo_uri')

'''
method for running main collatz conjecture
'''
def collatz(bound):
    max_len = 0
    for x in range(1,bound):
        
        length = 0 
        val = x
        
        while val != 1:
            length += 1
            val = val // 2 if val % 2 == 0 else 3*val+1
        max_len = max(max_len, length)
    return max_len

def main():
    
    m = Mongo(mongo_uri, collatz)

    bound = args.b
    threads = args.t

    #start time 
    start = time.time()
    
    max_len = collatz(bound)
    stop = time.time()

    total_time = stop - start
    #create document to be created
    results = {
        'type' : 'serial',
        'range' : bound,
        'max_length' : max_len,
        'total_time': total_time,
        'start_time': start,
        'end_time': stop 
    }
    
    m.insert_doc(results)
    
    print(f'The max length within range {bound} is {max_len}')



if __name__ == '__main__':
    main()


