# My favorite sorting algorithm! I like the way it operates in nlog(n) time.
# Given an arbitrary ordering instead of '<', this could be fairly easily rewritten to sort any data type with a natural linear order.
# This code allows the user to pick between ints, floats, and strings.

def merge_sort(data):
    # print(data)
    l = len(data)
    
    if l <= 1:
        return data
    
    sorted = True
    
    for i in range(0, l-1):
        if data[i] > data[i+1]:
            sorted = False
            # temp = data[i]
            # data[i] = data[i+1]
            # data[i+1] = temp

    if sorted == True:
        # print('sorted subarray:', data)
        return data
    else:
        first_half = merge_sort(data[:l//2])
        last_half = merge_sort(data[l//2:])
        top_idx = 0
        bot_idx = 0
        top_end_flag = False
        bot_end_flag = False
        temp = []
        
        while top_idx < len(first_half) and bot_idx < len(last_half):
            if first_half[top_idx] < last_half[bot_idx]:
                temp.append(first_half[top_idx])
                top_idx += 1
            else:
                temp.append(last_half[bot_idx])
                bot_idx += 1
            # print('top index:', top_idx, 'bottom index:', bot_idx)
            top_end_flag = (top_idx == len(first_half))
            bot_end_flag = (bot_idx == len(last_half))

        if top_end_flag:
            temp = temp + last_half[bot_idx:]
        if bot_end_flag:
            temp = temp + first_half[top_idx:] 
    return temp

if __name__ == '__main__':
    data = []
    n = int(input('Enter how many elements you want: '))
    type = input('Enter 0 for ints, 1 for floats, and anything else for arbitrary strings: ')
    if type == '0':
        for i in range(0, n):
            x = input('Enter an int to add to the array: ')
            data.append(int(x))
    elif type == '1':
        for i in range(0, n):
            x = input('Enter a float to add to the array: ')
            data.append(float(x))
    else:
        for i in range(0, n):
            x = input('Enter a string to add to the array: ')
            data.append(x)

    print(data)
    print(merge_sort(data))