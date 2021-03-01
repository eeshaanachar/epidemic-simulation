import random
import networkx as nx
import matplotlib.pyplot as plt


def generate_network(network_config):
    '''
    def generate_network():
        Create new graph
        Add graph attributes
        1st loop:
            create node
            add node attributes
            2nd loop:
                create config[average_edges] + rand(-3, +3) edges based on config[network_type] ('BA' ie barabassi-albert or 'ER' erdos-renyi)
                Simulating prob: rand(0, 1) <= given_prob ? true : false
                add edge attributes
        return graph

    Graph Attributes
        quarantine_probability
        quarantine_strictness
        travel_ban_strictness
        available_beds
        network_type
        social_distancing_probability
    Node Attributes
        travel_prob: rand(0, 1)
        status: 'S', later changed to 'I' and 'R'
    Edge Attributes
        distance: rand(0.2, 4)
    '''

def contaminate(network, virus_config):
    '''
    Select a random node, infect it and start BFS
    When infecting a node (adding to BFS queue)
        change status to I
        add a countdown of virus_config[duration] +- virus_config[uncertainity]
    Each iteration of outer BFS loop represents one day
    Simulating prob: rand(0, 1) <= given_prob ? true : false

    while queue not empty:
        InnerLoop1:
            kill node based on virus_config[death_prob]
            if node survived countdown -= 1
            if countdown == 0 or node killed
                change status to R, remove from queue
                if quarantined, available_beds += 1
                skip iteration ie continue
            if node is not quarantined && available_beds != 0:
                chance of quarantine = quarantine_prob * (1 - virus_config[asymptotic prob])
                if quarantined:
                    change status to Q
                    available_beds -= 1
            if rand(0, 1) > travel_ban_strictness and rand(0, 1) < node_travel_prob
                remove all edges of node
                add new edges based on nw type (barabassi-albert or erdos renyi)
        InnerLoop2:
            infect other nodes and add to queue
        Find SIR values

    Condition to infect other nodes
        (infector must not be quarantined || rand(0, 1) > quarantine_strictness) && infectee must have status of S
        && rand(0, 1) > social_dist_prob && infector_infectee_distance < virus_config[radius]
    If condition true, infect based on virus_config[prob]
    
    Return dictionary of the form
    {
        1: {'S': x1, 'I': y1, 'R': z1},
        2: {'S': x2, 'I': y2, 'R': z2},
        .
        n: {'S': xn, 'I': yn, 'R': zn}
    }
    where n = min(100, last day of disease)
    '''

def analyse(sir_stats):
    '''
    Plot the SIR graph
    Plot R0 (rounded to 1 decimal) for each day
    Plot R0 histogram
    I think R0 on day i =  (yi - y[i-1] + zi - z[i-1]) / y[i-1]

    Return dictionary of the form
    {
        'peakCases': a,
        'modeR0': b,
        'totalEpidemicDuration': c,
        'noOfDaysBedsFull': d,
        'finalSPercentage': e,
        'finalIPercentage': f,
        'finalRPercentage': g,
        <anything else that might be of interest>
    }
    '''

def main(network_config, virus_config):
    network = generate_network(network_config)
    stats = contaminate(network, virus_config)
    analyse(stats)


if __name__ == "__main__":

    network_config = {
        'quarantine_strictness': 0.8,
        'quarantine_probability': 0.8,
        'travel_ban_strictness': 0.5,
        'social_distancing_probability': 0.3,
        'network_type': 'BA',
        'node_count': 10000,
        'average_edge_count': 5,
        'available_beds': 100,
    }

    virus_config = {
        'average_duration': 9, # days
        'duration_uncertainity': 2, # days
        'death_probability': 0.03,
        'infection_probability': 0.1,
        'spread_radius': 2, # metres
        'asymptotic_probability': 0.1
    }

    main(network_config, virus_config)
