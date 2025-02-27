input_a = 10

def custom_max(*args):
    result = args[0]
    for i in range(len(args)-1):  
        if result < args[i+1]:
            result = args[i+1]
    return result

def custom_sort(_list, reverse = False):
    result = []

    while _list:
        if reverse:
            data = max(_list)
        else:
            data = min(_list) 
        result.append(data)
        _list.remove(data)
    return result