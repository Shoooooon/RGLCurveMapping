def graph_order(connection):
    graph = {0:0, 7:1, 1:2, 6:3, 5:4, 4:5, 2:6, 3:7}
    if (graph[connection[0][0]] < graph[connection[1][0]]) and (graph[connection[1][0]] < graph[connection[0][0]] + 4):
        return connection, False
    elif (graph[connection[0][0]] < graph[connection[1][0]] + 8) and (graph[connection[1][0]] + 8 < graph[connection[0][0]] + 4):
        return connection, False
    else:
        return (connection[1], connection[0]), True

## (edge1, edge2)  connection = [(edge1, index1), (edge2, index2)]
