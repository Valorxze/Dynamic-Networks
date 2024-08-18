# VS Code command palette (ctrl+shift+p)
# Python: Create Environment
# Python: Create Terminal

import networkx as nx
from networkx.algorithms import bipartite
from matplotlib import pyplot as plt
from collections import Counter

# Assignment Grade - 4.8 / 5


# Bipartite Perfect Matching
def bipartite_graph():
    nodes = int(input("How many nodes in each set? "))
    probability = float(input("Probability (A float between 0 and 1)? "))

    # This segment creates a bipartite random graph, but if the nodes on the left lack any edges, recreate a graph until
    # every left node has at least one edge. This is mainly to avoid the AmbiguousSolution Exception where the input
    # graph created is not connected.
    g = bipartite.random_graph(nodes, nodes, probability)
    while True:
        if not nx.is_connected(g):
            g = bipartite.random_graph(nodes, nodes, probability)
        else:
            break

    # Separate the nodes into two groups, left and right nodes, and align them top to bottom.
    left_nodes, right_nodes = nx.bipartite.sets(g)
    for i, node in enumerate(sorted(list(left_nodes))):
        g.add_node(node, pos=(0, i))
    for i, node in enumerate(sorted(list(right_nodes))):
        g.add_node(node, pos=(1, i))

    # Use NetworkX function to check for perfect matching. If there is a perfect matching, color the edges green to
    # indicate which node connects for perfect matching. All remaining edges will become red.
    matching = nx.bipartite.maximum_matching(g).items()
    for edge in g.edges:
        if edge in matching:
            g.add_edge(edge[0], edge[1], color='green', weight=10)
        else:
            g.add_edge(edge[0], edge[1], color='red', weight=0.1)
    nx.draw(g, pos=nx.get_node_attributes(g, 'pos'), with_labels=True, edge_color=nx.get_edge_attributes(g, 'color')
            .values())

    print("Green represents a perfect match")
    plt.show()
    print("")


# Market Clearing Algorithm
def market():
    # Using Try and Except in case the user inputs an incorrect file.
    try:
        user_file = input("Enter text file: ")
        with open(user_file) as text:
            file_contents = [line.strip() for line in text]

        # Create the sellers, buyers, valuations, and prices.
        # This can only run using the sample file provided in the assignment.
        sellers = ['A', 'B', 'C']
        buyers = ['X', 'Y', 'Z']
        file_valuations = [[file_contents[4][0] + file_contents[4][1], (file_contents[4][3]), file_contents[4][5]],
                           [file_contents[5][0], file_contents[5][2], file_contents[5][4]],
                           [file_contents[6][0], file_contents[6][2], file_contents[6][4]]]
        file_price = [file_contents[3][0], file_contents[3][2], file_contents[3][4]]

        valuations = [list(map(int, sublist)) for sublist in file_valuations]
        price = [int(x) for x in file_price]

        # Separate the nodes into two groups, left and right nodes, and align them top to bottom.
        # Also create text to demonstrate the valuations and prices for the graph.
        g = nx.Graph()
        for i, node in enumerate(sellers):
            g.add_node(node, pos=(0, len(sellers) - i))
        for i, node in enumerate(buyers):
            g.add_node(node, pos=(1, len(buyers) - i))

        # Run a series of function calls until the market is cleared.
        number_of_sellers = 0
        while number_of_sellers != len(sellers):
            max_value = find_max_value(sellers, buyers, valuations, price)
            display_graph(sellers, buyers, valuations, price, max_value)
            count = constricted_edge(sellers, price, max_value)
            number_of_sellers = len(count)

        print("The market has been cleared\n")
    except FileNotFoundError:
        print("File does not exist in this directory, try again\n")


# Calculate the maximum payoff for each buyer.
# Sellers with more than one buyer will increase their price until buyers pursue another seller that gives them a better
# payoff.
def find_max_value(sellers, buyers, valuation, price):
    max_value_sellers = {}
    for buyer_index in range(len(buyers)):
        max_value = 0
        for seller_index in range(len(sellers)):
            if max_value < valuation[buyer_index][seller_index] - price[seller_index]:
                max_value = valuation[buyer_index][seller_index] - price[seller_index]
                max_value_sellers[buyers[buyer_index]] = [sellers[seller_index]]
            elif max_value == valuation[buyer_index][seller_index] - price[seller_index]:
                max_value_sellers[buyers[buyer_index]].append(sellers[seller_index])
    return max_value_sellers


# Plot the graph's current round revealing the best payoff for each buyer.
# Continues being called when sellers update their price and buyers pursue other sellers.
def display_graph(sellers, buyers, valuations, price, max_value):
    g = nx.Graph()

    for i, node in enumerate(sellers):
        g.add_node(node, pos=(0, len(sellers)-i))
    for i, node in enumerate(buyers):
        g.add_node(node, pos=(1, len(buyers)-i))

    for key, values in max_value.items():
        for value in values:
            g.add_edge(key, value)

    for i, buyer in enumerate(buyers):
        plt.text(1.1, len(buyers)-i, s=valuations[i])
    for i, buyer in enumerate(buyers):
        plt.text(-0.1, len(buyers)-i, s=price[i])

    nx.draw(g, pos=nx.get_node_attributes(g, 'pos'), with_labels=True)
    plt.show()


# Function that determines if the seller has more than one buyer.
# More than one buyer means it forms a constricted set, so we increment the sellers price.
def constricted_edge(sellers, price, max_value):
    count = dict(Counter(sum(max_value.values(), [])))
    constricted_list = []
    for key, value in count.items():
        if value > 1:
            constricted_list.append(key)
            price[sellers.index(key)] += 1
    print("Adding 1 to Node(s)", constricted_list)
    return count


print("Professor Notes:")
print("The Market Clearing Algorithm will only run using the sample file provided\n")

while True:
    choice = int(input("Press 1 for Bipartite Perfect Matching\nPress 2 for Market-Clearing Algorithm\n"
                       "Press 3 to exit program\n"))
    if choice == 1:
        bipartite_graph()
    elif choice == 2:
        market()
    elif choice == 3:
        break
