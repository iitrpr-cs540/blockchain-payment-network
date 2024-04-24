from generate_graphs import make_list, write_graph

num_graph_nodes = [x*4 for x in range(1,201)]
num_graph_edges = [2*n - 2 for n in num_graph_nodes]  # sparse graph

# num_graph_edges = [int(n*(n-1)/2) for n in num_graph_nodes] # complete graph

for i in range(len(num_graph_nodes)):
    adj_list = make_list(num_graph_nodes[i], num_graph_edges[i], 10*num_graph_nodes[i])
    write_graph(num_graph_nodes[i], num_graph_edges[i], adj_list)