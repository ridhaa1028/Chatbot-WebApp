# This is to deal with the section tally time in a way i can run the algo
# Takes the entire string and converts to timeblocks
import re
import copy

# TR 1700 1815 -> T 1700 1815 R 1700 1815
def seperate_days(s):
    for day in ['M', 'T', 'W', 'R', 'F', 'S', 'U']:
        s = s.replace(day, f'{day} ')
    times = re.findall(r'\d{4} \d{4}', s)
    time_str = times[0]
    
    s = s.replace(time_str, '')
    result = ' '.join([f"{day} {time_str}" for day in s.split()])
    return result 

# Given a String, make array of every 3 words
# TR 1700 1815 TR 1830 1945" - > ['TR 1700 1815', 'TR 1830 1945']
def group_by_three(str):
    items = str.split()
    return [' '.join(items[i:i+3]) for i in range(0, len(items), 3)]

# In: Section Tally Mess
# Out: Array of all string time blocks ["Day Start End", ..]
def make_time_blocks(s):
    
    # Edge case if course has no time : "None"
    if not s:
        return ["None"]

    # TR 1700 1815 WESTBY 109 (Class) TR 1830 1945 WESTBY 109 (Class) - > TR 1700 1815 TR 1830 1945
    s = ' '.join(re.findall(r'([MTWRFSU]+ \d{4} \d{4})', s))

    # TR 1700 1815 TR 1830 1945" - > ['TR 1700 1815', 'TR 1830 1945']
    items = group_by_three(s)

    # ['TR 1700 1815', 'TR 1830 1945'] -> ['T 1700 1815 R 1700 1815', 'T 1830 1945 R 1830 1945']
    items = [seperate_days(i) for i in items]

    # ['T 1700 1815 R 1700 1815', 'T 1830 1945 R 1830 1945'] -> "T 1700 1815 R 1700 1815 T 1830 1945 R 1830 1945" 
    items = ' '.join(items)

    # "T 1700 1815 R 1700 1815 T 1830 1945 R 1830 1945" -> ['T 1700 1815', 'R 1700 1815', 'T 1830 1945', 'R 1830 1945']
    return group_by_three(items)

def ensure_trailing_zero(number):
    if number < 1000:
        string = str(number)
        if string[0] != 0:
            return "0" + string
    return str(number)
    
# In: Array of String Time Blocks
# Out: Array but with combined back to back blocks
def combine_time_blocks(Blocks):

    # Again edge case - connected to above
    if Blocks == ["None"]:
        return Blocks
    
    # Combine str to list for easier manipulation
    # ['M 0930 1045', 'W 0930 1045', 'M 1400 1515', 'M 1530 1645'] ->
    #           -> [['M', '0930', '1045'], ...]
    Blocks = [i.split() for i in Blocks]
    for i in range(len(Blocks)):
        block = Blocks[i] #['M', '0930', '1045']
        block[1] = int(block[1])
        block[2] = int(block[2])
    
    # Combine Step
    # Using high bound of 6 blocks just in case
    for _ in range(6):
        Blocks.sort(key=lambda x: (x[0], x[1]))
        myCopy = copy.deepcopy(Blocks)
        for b in range(len(myCopy)-1):
            day1, day2 = myCopy[b][0], myCopy[b+1][0]
            if day1 == day2:
                end_of_first = myCopy[b][2]
                start_of_second = myCopy[b+1][1]
                if start_of_second - end_of_first < 70:
                    new_start = myCopy[b][1]
                    new_end = myCopy[b+1][2]
                    new_block = [day1, new_start, new_end]
                    oldblock1 = [day1, new_start, end_of_first]
                    oldblock2 = [day2, start_of_second, new_end]
                    Blocks = [j for j in Blocks if j != oldblock1 and j != oldblock2]
                    Blocks.append(new_block)
                    break
    
    # Convert back from list to str
    for i in range(len(Blocks)):
        block = Blocks[i]
        day = block[0]
        start = ensure_trailing_zero(int(block[1]))
        end = ensure_trailing_zero(int(block[2]))
        Blocks[i] = f"{day} {start} {end}"
    
    return Blocks

def extract_times(str):
    return combine_time_blocks(make_time_blocks(str))