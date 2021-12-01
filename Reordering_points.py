# coding=utf-8
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


# Need to convert this to Grasshopper edges instead of Flipper edges.
deg1 = {(~7, ~6): 0, (~8, ~6): 1, (~7, 6): 1, (~1, 6): 0, (~1, 8): 1, (1, 8): 1, (1, 7): 0, (~8, 7): 0}
deg2 = {(~8, ~7): 1, (~7, ~1): 1, (6, 8): 0, (~1, 1): 1, (7, 8): 1, (~8, 1): 0, (~6, 7): 0, (~6, 6): 1}
deg3 = {(~8, 6): 1, (1, 6): 1, (~7, 8): 1, (~6, ~1): 1, (~1, 7): 1, (~6, 1): 0, (~7, 7): 0, (~8, 8): 0}
deg4 = {(~8, ~1): 0, (~6, 8): 0, (~7, 1): 0, (6, 7): 0}
# Orientation 0: start matching from the smaller end of the smaller edge.
# Orientation 1: start matching from the larger end of the smaller edge.

def reorder_a_pair(pair):
    if pair[1] < pair[0]:
        return (pair[1], pair[0])
    else:
        return pair


def getpair(connection):
    # A connection is in this form: ((edge1, index1),(edge2, index2))
    # Get the pair fo connection and also reorder it.
    return reorder_a_pair((connection[0][0], connection[1][0]))


def compare_index(connection1, connection2):
    # Return the one with the smaller index.
    if connection1[0][0] < connection1[1][0]:
        if connection2[0][0] < connection2[1][0]:
            if connection1[0][1] < connection2[0][1]:
                return connection1
            elif connection1[0][1] > connection2[0][1]:
                return connection2
        elif connection2[0][0] > connection2[1][0]:
            if connection1[0][1] < connection2[1][1]:
                return connection1
            elif connection1[0][1] > connection2[1][1]:
                return connection2
    elif connection1[0][0] > connection1[1][0]:
        if connection2[0][0] < connection2[1][0]:
            if connection1[1][1] < connection2[0][1]:
                return connection1
            elif connection1[1][1] > connection2[0][1]:
                return connection2
        elif connection2[0][0] > connection2[1][0]:
            if connection1[1][1] < connection2[1][1]:
                return connection1
            elif connection1[1][1] > connection2[1][1]:
                return connection2

#((1,0),(8,1)) ((1,2),(8,0))


def reorder_same_type(this_type, type0):
    # This function reorders a list of connections of the same type, i. e. connecting the same pair of edges.
    if (type0 in deg1) == True:
        orientation = deg1[type0]
    elif (type0 in deg2) == True:
        orientation = deg2[type0]
    elif (type0 in deg3) == True:
        orientation = deg3[type0]
    elif (type0 in deg4) == True:
        orientation = deg4[type0]
    this_type_new = [this_type[0]]
    for connection in this_type[1:]:
        for i in range(0, len(this_type_new)):
            if orientation == 0:
                if compare_index(connection, this_type_new[i]) == connection:
                    this_type_new.insert(i, connection)
                    break
                elif compare_index(connection, this_type_new[i]) == this_type_new[i]:
                    if i == len(this_type_new) - 1:
                        this_type_new.append(connection)
            elif orientation == 1:
                if compare_index(connection, this_type_new[i]) == this_type_new[i]:
                    this_type_new.insert(i, connection)
                    break
                elif compare_index(connection, this_type_new[i]) == connection:
                    if i == len(this_type_new) - 1:
                        this_type_new.append(connection)
    return this_type_new


def reorder_same_degree(conn_list):
    # This function reorders a list of connections of the same degree.
    original_list = conn_list
    reorder_list = []
    while len(original_list) > 0:
        type0 = getpair(original_list[0])
        this_type = []
        to_remove = []
        for connection in original_list:
            if getpair(connection) == type0:
                this_type.append(connection)
                to_remove.append(connection)
        for connection in to_remove:
            original_list.remove(connection)
        reorder_list = reorder_list + reorder_same_type(this_type, type0)
    return reorder_list


# It would be better if the input is the 'abstract point list,' i.e. [((point1),(point2)),...].

# Test
# abstractPointList = [((~8,0), (1,0)), ((~1,0), (7,0)), ((~7,0), (6,0)), ((~6,0), (1,1)), ((~1,1), (7,1)), ((~7,1), (8,0))]

def reorder_list(abstractPointList):
    conn_deg1 = []
    conn_deg2 = []
    conn_deg3 = []
    conn_deg4 = []
    for connection in abstractPointList:
        if (getpair(connection) in deg1) == True:
            conn_deg1.append(connection)
        elif (getpair(connection) in deg2) == True:
            conn_deg2.append(connection)
        elif (getpair(connection) in deg3) == True:
            conn_deg3.append(connection)
        elif (getpair(connection) in deg4) == True:
            conn_deg4.append(connection)
    sorted = reorder_same_degree(conn_deg1) + reorder_same_degree(conn_deg2) + reorder_same_degree(conn_deg3) + reorder_same_degree(conn_deg4)
    # print(sorted)
    return sorted

# print(reorder_list([((-7, 0), (7, 0)), ((-8, 0), (6, 1)), ((-7, 1), (6, 0))]))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
