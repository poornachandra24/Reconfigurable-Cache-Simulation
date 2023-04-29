import datetime
import time as tm

CACHE_SIZE = 4096
CACHE_SIZE_DM = 1024
BLOCK_SIZE = 32

dm_counter = 0
sa_counter = 0

cache = []

dec_cpu_addresses = [7833, 4987, 2529, 1369, 2627, 3481, 4540, 
                      1369, 2627, 3481, 4112, 5827, 7349, 4993, 
                      3311, 1402, 2529, 1369, 2627, 4062, 9126, 
                      8118, 2282, 3551, 8095, 4282, 3315, 7334, 
                      7431, 8146, 4935, 2847]# decimal addresses

def load_from_memory(index_val):

    return dec_cpu_addresses[index_val] #load an address from CPU into cache

def time():

    dt_object = datetime.datetime.now()
    t = dt_object.strftime(' %H:%M:%S.%f')
    return t

def direct_mapped_cache(address):

    global cache , dm_counter

    num_blocks = CACHE_SIZE_DM // BLOCK_SIZE
    if(not dm_counter):
        cache = [None] * num_blocks #first run only

    print("\nCounter Value : ",dm_counter)

    cache_display_dm(0) #print initial cache

    block_index = (address // BLOCK_SIZE) % num_blocks
    tag = address // num_blocks

    # print("Bit Data : Tag, Block Index , Number of Blocks : ",tag,block_index,num_blocks)

    if cache[block_index] is not None and cache[block_index]['tag'] == tag:
        # Block found, update access time and return data
        cache[block_index]['access_time'] = time()
        print("Cache Hit : ",cache[block_index]['data'])

    cache_display_dm(1) #show cache

    # Block not found, load data from memory and insert into cache
    data = address
    new_block = {'tag': tag, 'data': data, 'access_time': time()}
    cache[block_index] = new_block
    cache_display_dm(1) # with added new data

    dm_counter += 1

def set_associative_cache_v3(address, set_no):
    global cache, sa_counter
    
    num_blocks = CACHE_SIZE // BLOCK_SIZE
    num_sets = num_blocks // set_no
    set_index = (address // BLOCK_SIZE) % num_sets
    tag = address // (num_sets * BLOCK_SIZE)
    set_no = address % num_sets

    # cache_display_sa(0)
    
    # Initialize cache on first run

    if not sa_counter:
        cache = [None for _ in range(num_sets)]
    
    # Check if block is already in cache
    for i in range(num_sets):
        if cache[set_index] is not None and cache[set_index]['tag'] == tag:
            # Block found, update access time and return data
            cache[set_index]['access_time'] = time()
            print("Cache Hit : ",cache[set_index]['data'])
            return cache[set_index]['data']

    
    # Block not found, load data from memory and insert into cache
    data = address
    

    if cache[set_index] is None:
        # Insert if it's empty
        cache[set_index] = {'tag': tag, 'data': data, 'access_time': time()}
        print("Set No. : ",cache[set_index])
        cache_display_sa(1)

        
    else:
        # Both ways are occupied, evict LRU block and insert new block
        if cache[set_index] is not None and cache[set_index+1] is not None and cache[set_index]['access_time'] < cache[set_index+1]['access_time']:
            evicted_block = cache[set_index]['data']
            print("Evicted LRU Block : ", evicted_block)
            cache[set_index] = {'tag': tag, 'data': data, 'access_time': time()}
  
        # Fetch new block from memory and insert into cache
        new_block_data = address
        new_block = {'tag': tag, 'data': new_block_data, 'access_time': time()}
        cache[set_index] = new_block
        cache_display_sa(1)
    
    sa_counter += 1

def cache_display_sa(init_val):

    global cache

    if(init_val == 0):
        print("Cache Empty...\t Time Stamp : ",time())
    if(init_val != 0):
        print("Modified cache...\t Time Stamp : ",time())
         # Print the contents of the cache with timestamps

        print("\n\n ____SET ASSOCIATIVE____")
        print('Block Index\tTag\tData\tAccess Time')
        for i, block in enumerate(cache):
            # print(f'Element {i}: {block}, Type: {type(block)}')
            if block is not None:
                print(f'{i}\t\t{block["tag"]}\t{block["data"]}\t{block["access_time"]}')
                # print(f'{i}\t\t{block[0]}\t{block[1]}\t{block[2]}')
            else:
                print(f'{i}\t\t-\t-\t-')

def cache_display_dm(init_val):

    global cache

    
    if(init_val == 0):
        print("Cache Empty...\t Time Stamp : ",time(),"\n")

    if(init_val != 0):
        print("Modified cache...\t Time Stamp : ",time(),"\n")
         # Print the contents of the cache with timestamps

        print("\n\n ____DIRECT MAPPED____")
        print('Block Index\tTag\tData\tAccess Time')
        for i, block in enumerate(cache):
            # print(f'Element {i}: {block}, Type: {type(block)}')
            if block is not None:
                print(f'{i}\t\t{block["tag"]}\t{block["data"]}\t{block["access_time"]}')
            else:
                print(f'{i}\t\t-\t-\t-')

def main():

    cache_display_sa(0)

    print("1. Direct Mapped\t2. 2 Way SA\t3. 4 Way SA")
    selection = int(input("Enter your choice : "))
    
    for i in range (32):

        tm.sleep(1)
        cpu_val = load_from_memory(i)
        print("\nRetrieved from CPU : ",cpu_val)

        if (cpu_val not in cache):

            if (selection == 1):
                direct_mapped_cache(cpu_val)

            if (selection == 2):
                set_associative_cache_v3(cpu_val,2)
            
            if (selection == 3):
                set_associative_cache_v3(cpu_val,4) 
        
        else:
            print("Found in Cache")
        

main()