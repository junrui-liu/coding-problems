import math as mt 
  
# Prints smaller elements on left  
# side of every element 
def printPrevSmaller(arr, n): 
  
    # Create an empty stack 
    S = list() 
  
    # Traverse all array elements 
    for i in range(n): 
        x = arr[i]
        # Keep removing top element from S  
        # while the top element is greater  
        # than or equal to arr[i] 
        while (len(S) > 0 and S[-1] < arr[i]): 
            S.pop() 
  
        # If all elements in S were greater 
        # than arr[i] 
        if (len(S) == 0): 
            print("_, ", end = "") 
        else: # Else print the nearest  
              # smaller element 
            print(S[-1], end = ", ") 
  
        # Push this element 
        S.append(arr[i]) 
l = [6,2,4,5,9,30,7,1,8]
printPrevSmaller(l,len(l))