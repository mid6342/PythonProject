import sqlite3
import numpy as np
from operator import itemgetter

# connect to database
conn = sqlite3.connect("FindingFunctions.db")
cur = conn.cursor()

# function to get a whole column in form of a list
def get_list_of_column(column, table):
    # get all the cells of the column and write them to a list
    query= cur.execute("SELECT " + column + " FROM " + table)
    list_of_column = []
    for cell in query: 
        list_of_column.append(cell[0])  
    # remove column head
    list_of_column.pop(0)
    return list_of_column


# function for subtracting 2 lists
def sum_of_squared_deviations(list_1, list_2):
    #not_squared = np.array(list_1) - np.array(list_2)
    squared = np.square(np.array(list_1) - np.array(list_2))
    sum_of_squared = np.sum(squared)
    return sum_of_squared

# calculating the sum of squared deviation + print for all the 50 functions 
all_the_sums = []
for i in range(1, 51):
    for k in range(1, 5):
        ideal = get_list_of_column(("y" + str(i)), "ideal")
        train = get_list_of_column(("y" + str(k)), "train")
        all_the_sums.append([("y" + str(i)), ("y" + str(k)), 
        (sum_of_squared_deviations(ideal, train))])
        
sorted_list = sorted(all_the_sums, key=itemgetter(2))
four_ideal = sorted_list[:4]
print(four_ideal)

"""
Result of the equation (ideal, train, sum)
[['y31', 'y4', 31.128519434568638], 
['y46', 'y1', 32.660363984619835], 
['y6', 'y2', 33.74643722393511], 
['y25', 'y3', 35.39435460328838]]
"""

# one ideal function for demonstration purposes iy31ty4
ideal_y31 = get_list_of_column("y31", "ideal")
train_y4 = get_list_of_column("y4", "train")
train_y1 = get_list_of_column("y1", "train")
train_y2 = get_list_of_column("y2", "train")
train_y3 = get_list_of_column("y3", "train")
test_x = get_list_of_column("x", "test")
test_y = get_list_of_column("y", "test")
ideal_y31 = get_list_of_column("y31", "ideal")
ideal_y46 = get_list_of_column("y46", "ideal")
ideal_y6 = get_list_of_column("y6", "ideal")
ideal_y25 = get_list_of_column("y25", "ideal")

print("This is ideal 25")
print(ideal_y25)

def max_deviation(list_1, list_2):
    # list of squared deviations
    return np.max(np.square(np.array(list_1) - np.array(list_2)))

max_dev_y31 = max_deviation(ideal_y31, train_y4)
print(max_dev_y31)
max_dev_y46 = max_deviation(ideal_y46, train_y1)
print(max_dev_y46)
max_dev_y6 = max_deviation(ideal_y6, train_y2)
print(max_dev_y6)
max_dev_y25 = max_deviation(ideal_y25, train_y3)
print(max_dev_y25)
"""
Result for the demonstration function and its dedicated train function
0.24836179255280993
"""



#print(test_x)
#print(test_y)

all_deviations = []
deviation_2 = []
def get_y_in_ideal(column):
    y_test = []
    first_time = True
    for x_row in test_x:
        query = cur.execute("SELECT " + column + " FROM ideal WHERE x=" + str(x_row))
        for cell in query: 
            y_ideal = np.asarray(cell)
            #print("y wert of ideal function: " + str(y_ideal))
        # bis dahin passt alles, da es ja nur durch die ideal function geht
        query_2 = cur.execute("SELECT y FROM test WHERE " + "x" + "=" + str(x_row))
        for cell in query_2: 
            np.array(y_test.append(cell[0]))
        #print("y wert of test point: " + str(y_test))
        if(len(y_test) == 1):
            deviation = abs(y_test - y_ideal)
            #print("in between")
            #print(deviation)
        elif((len(y_test) == 2) & (first_time == True)):
            deviation = abs(y_test[0] - y_ideal)
            #print(first_time)
            #print(deviation)
            first_time = False
        else:
            deviation = abs(y_test[1] - y_ideal)
            #print(first_time)
            #print(deviation)
        y_test.clear()
        #deviation_squareroot = deviation * np.sqrt(2)
        all_deviations.append(deviation[0])
        #deviation_2.append(deviation[0])
        #print("----------------------------------------------------")
        #y_test = []
        #print("x wert of test point: " + str(x_row))
        #deviation = y_test - y_ideal
        #print(deviation)
        #print("----------------------------")


get_y_in_ideal("y31")
print("31")
#list of the deviation of all testpoints for the ideal function 31
print(all_deviations)
all_deviations.clear()

print("46")
get_y_in_ideal("y46")
print(all_deviations)
all_deviations.clear()

print("6")
get_y_in_ideal("y6")
print(all_deviations)
all_deviations.clear()

print("25")
get_y_in_ideal("y25")
print(all_deviations)
all_deviations.clear()

#print(deviation_2)
#print("y25")
#get_y_in_ideal("y25")



    
# commit and close connection to database    
conn. commit()
conn.close()