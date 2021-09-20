import time
import argparse

#argument information 

parser = argparse.ArgumentParser( description='collatz conjecture calculation')
parser.add_argument( '-b', type=int, action='store', required=True,  help='upper bound for collatz calculation')

args = parser.parse_args()


def collatz(bound):
    max_len = 0
    for x in range(1,bound):
        
        
        length = 0 
        val = x
        
        while val != 1:
            
            length += 1
            if val % 2 == 0:
                val = val / 2
            else:
                val = 3 * val + 1
        print(f'x = {x} len = {length}\n\n') 
        max_len = max(max_len, length)
    return max_len


def main():
    
    bound = args.b

    max_len = collatz(bound)

    print(f'The max length within range {bound} is {max_len}')



if __name__ == '__main__':
    main()


