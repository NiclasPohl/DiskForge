def binary_search(arr, value): # TODO evt keyen fuer Array von dicts
    low, high = 0, len(arr) - 1
    if(len(arr)==0):
        return 0

    while low <= high:
        mid = (low + high) // 2

        if arr[mid] == value:
            return mid  # Value already exists, insert at this position
        elif arr[mid] < value:
            low = mid + 1
        else:
            high = mid - 1

    return low  # Position to insert the value

def binary_search_unixtime(arr,value):
    low, high = 0, len(arr) - 1
    if(len(arr)==0):
        return 0
    #print(value)

    while low <= high:
        mid = (low + high) // 2
        #print(arr[mid]["unixtime"])

        if int(arr[mid]["unixtime"]) == value:
            return mid  # Value already exists, insert at this position
        elif int(arr[mid]["unixtime"]) < value:
            low = mid + 1
        else:
            high = mid - 1

    return low  # Position to insert the value

def insert_into_sorted_array(sorted_array, value):
    index = binary_search(sorted_array, value)
    print(index)
    sorted_array.insert(index, value)

# Example usage:
#sorted_array = [1, 3,4, 5, 5,5, 5, 5, 7, 9]
#sorted_array = []
#value_to_insert = 4

#print(insert_into_sorted_array(sorted_array, value_to_insert))

#print(sorted_array)
