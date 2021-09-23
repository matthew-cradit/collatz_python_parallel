import time
import argparse
import os
import concurrent.futures
from Mongo_class import Mongo
from pymongo import MongoClient
from pprint import pprint

#argument information 
parser = argparse.ArgumentParser( description='collatz conjecture calculation')
parser.add_argument( '-b', type=int, action='store', required=True,  help='upper bound for collatz calculation')
parser.add_argument('-t', type=int, action='store', required = True, help='number of threads')
args = parser.parse_args()
#retrieve database connection information
mongo_uri = os.getenv('mongo_uri')

'''
method for running main collatz conjecture
'''
def collatz(bound: int, rank: int, threads: int) -> int:
    max_len = 0
    rank += 1

    for x in range(rank , bound, threads):
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
    max_len = 0  
    #start time 
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        thread_results = [ executor.submit(collatz, bound, x, threads) for x in range(threads) ]
        
    for f in concurrent.futures.as_completed(thread_results):
        max_len = max(max_len, f.result())

    stop = time.time()

    total_time = stop - start
    #create document to be created
    test_results = {
        'type' : 'multithread',
        'range' : bound,
        'number of threads' : threads,
        'max_length' : max_len,
        'total_time': total_time,
        'start_time': start,
        'end_time': stop 
    }
    
    m.insert_doc(test_results)
    
    print(f'The max length within range {bound} is {max_len}')



if __name__ == '__main__':
    main()


