import matplotlib.pyplot as plt
import random
from datetime import datetime
from scipy.ndimage.filters import gaussian_filter1d
from util import GraphFactory
from util import Keys


class EpidemicSimulation:

    def __init__(self, network_config, virus_config, seed=None):

        random.seed(seed)
        plt.switch_backend('Agg') # turns off GUI

        self.simulated = False
        self.network = GraphFactory.get_graph(network_config)
        self.virus_config = virus_config

        self.network.graph[Keys.QUARANTINE_PROBABILITY] = network_config[Keys.QUARANTINE_PROBABILITY]
        self.network.graph[Keys.QUARANTINE_STRICTNESS] = network_config[Keys.QUARANTINE_STRICTNESS]
        self.network.graph[Keys.TRAVEL_BAN_STRICTNESS] = network_config[Keys.TRAVEL_BAN_STRICTNESS]
        self.network.graph[Keys.AVAILABLE_BEDS] = network_config[Keys.AVAILABLE_BEDS]
        self.network.graph[Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS] = network_config[Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS]
        self.network.graph[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION] = network_config[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION]
        self.network.graph[Keys.AVERAGE_SOCIAL_DISTANCE] = network_config[Keys.AVERAGE_SOCIAL_DISTANCE]
        self.network.graph[Keys.SOCIAL_DISTANCE_VARIATION] = network_config[Keys.SOCIAL_DISTANCE_VARIATION]

        for node_id in self.network.nodes:

            immunityVariation = random.randint(-network_config[Keys.IMMUNITY_VARIATION] * 1000, network_config[Keys.IMMUNITY_VARIATION] * 1000) / 1000
            self.network.nodes[node_id][Keys.IMMUNITY] = network_config[Keys.AVERAGE_IMMUNITY] + immunityVariation

            safetyFactorVariation = random.randint(-network_config[Keys.SAFETY_FACTOR_VARIATION] * 1000, network_config[Keys.SAFETY_FACTOR_VARIATION] * 1000) / 1000
            self.network.nodes[node_id][Keys.SAFETY_FACTOR] = network_config[Keys.AVERAGE_SAFETY_FACTOR] + safetyFactorVariation

            travelVariation = random.randint(-network_config[Keys.TRAVEL_FACTOR_VARIATION] * 1000, network_config[Keys.TRAVEL_FACTOR_VARIATION] * 1000) / 1000
            self.network.nodes[node_id][Keys.TRAVEL_PROBABILITY] = network_config[Keys.AVERAGE_TRAVEL_FACTOR] + travelVariation
            
            self.network.nodes[node_id][Keys.STATUS] = 'S'
            self.network.nodes[node_id][Keys.SECONDARY_INFECTIONS] = 0

        for _ in range(network_config[Keys.CENTRAL_HUB_COUNT]):
            node_id = random.randint(0, self.network.number_of_nodes() - 1)
            while self.network.degree[node_id] < self.network.number_of_nodes() / 10:
                self.network.add_edge(node_id, random.randint(0, self.network.number_of_nodes() - 1))

        for edge in self.network.edges:
            socialDistanceVariation = random.randint(-network_config[Keys.SOCIAL_DISTANCE_VARIATION] * 1000, network_config[Keys.SOCIAL_DISTANCE_VARIATION] * 1000) / 1000
            self.network.edges[edge][Keys.PHYSICAL_DISTANCE] = network_config[Keys.AVERAGE_SOCIAL_DISTANCE] + socialDistanceVariation
            num_contacts_variation = random.randint(-network_config[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION], network_config[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION])
            self.network.edges[edge][Keys.NUMBER_OF_PHYICAL_CONTACTS] = network_config[Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS] + num_contacts_variation


    def is_infection_possible(self, infector_id, infectee_id):

        if self.network.nodes[infector_id][Keys.STATUS] not in ('I','Q'):
            return False

        if self.network.nodes[infectee_id][Keys.STATUS] != 'S':
            return False

        if self.network.edges[infector_id, infectee_id][Keys.PHYSICAL_DISTANCE] > self.virus_config[Keys.INFECTION_RADIUS]:
            return False

        for _ in range(self.network.edges[infector_id, infectee_id][Keys.NUMBER_OF_PHYICAL_CONTACTS]):

            if self.network.nodes[infector_id][Keys.STATUS] == 'Q':
                is_quarantine_followed = random.random() <= self.network.graph[Keys.QUARANTINE_STRICTNESS]
                if is_quarantine_followed:
                        continue

            isInfecteeImmune = random.random() <= self.network.nodes[infectee_id][Keys.IMMUNITY]
            if isInfecteeImmune:
                    continue

            doesInfecteeFollowSafety = random.random() <= self.network.nodes[infectee_id][Keys.SAFETY_FACTOR]
            if doesInfecteeFollowSafety:
                    continue

            does_infection_spread = random.random() <= self.virus_config[Keys.INFECTION_PROBABILITY]
            if does_infection_spread:
                return True

        return False


    def contaminate(self):

        if self.simulated:
            raise Exception('Simulation already completed for this instance!')
        self.simulated = True            

        random_node_id = random.randint(0, self.network.number_of_nodes() - 1)
        durationVariation = random.randint(-self.virus_config[Keys.DURATION_VARIATION], self.virus_config[Keys.DURATION_VARIATION])
        self.network.nodes[random_node_id][Keys.DAYS_REMAINING] = self.virus_config[Keys.AVERAGE_DURATION] + durationVariation
        self.network.nodes[random_node_id][Keys.STATUS] = 'I'
        bfs_queue = [random_node_id]
        susceptible, infected, removed, secondary_infections = self.network.number_of_nodes() - 1, 1, 0, 0
        statistics = [(susceptible, infected, removed, 0)]

        while bfs_queue:

            for i in range(len(bfs_queue)):

                node_id = bfs_queue[i]
                node = self.network.nodes[node_id]

                node[Keys.DAYS_REMAINING] -= 1
                is_dead = random.random() <= self.virus_config[Keys.DEATH_PROBABILITY]
                if node[Keys.DAYS_REMAINING] == 0 or is_dead:
                    if node[Keys.STATUS] == 'Q':
                        self.network.graph[Keys.AVAILABLE_BEDS] += 1
                    node[Keys.STATUS] = 'R'
                    infected -= 1
                    removed += 1
                    secondary_infections += node[Keys.SECONDARY_INFECTIONS]
                    continue

                if node[Keys.STATUS] != 'Q' and self.network.graph[Keys.AVAILABLE_BEDS] != 0:
                    is_quarantined = random.random() <= self.network.graph[Keys.QUARANTINE_PROBABILITY] * (1 - self.virus_config[Keys.ASYMPTOTIC_PROBABILITY])
                    if is_quarantined:
                        node[Keys.STATUS] = 'Q'
                        self.network.graph[Keys.AVAILABLE_BEDS] -= 1

                does_travel = (random.random() <= node[Keys.TRAVEL_PROBABILITY]) and (random.random() > self.network.graph[Keys.TRAVEL_BAN_STRICTNESS])
                if does_travel:
                    for neighbor_id in list(self.network.neighbors(node_id)):
                        self.network.remove_edge(node_id, neighbor_id)
                        new_neighbor_id = random.randint(0, self.network.number_of_nodes() - 1)
                        self.network.add_edge(node_id, new_neighbor_id)
                        social_distance_variation = random.randint(-self.network.graph[Keys.SOCIAL_DISTANCE_VARIATION] * 1000, self.network.graph[Keys.SOCIAL_DISTANCE_VARIATION] * 1000) / 1000
                        self.network.edges[node_id, new_neighbor_id][Keys.PHYSICAL_DISTANCE] = self.network.graph[Keys.AVERAGE_SOCIAL_DISTANCE] + social_distance_variation
                        num_contacts_variation = random.randint(-self.network.graph[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION], self.network.graph[Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION])
                        self.network.edges[node_id, new_neighbor_id][Keys.NUMBER_OF_PHYICAL_CONTACTS] = self.network.graph[Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS] + num_contacts_variation

                for neighbor_id in self.network.neighbors(node_id):
                    if self.is_infection_possible(bfs_queue[i], neighbor_id):
                        durationVariation = random.randint(-self.virus_config[Keys.DURATION_VARIATION], self.virus_config[Keys.DURATION_VARIATION])
                        self.network.nodes[neighbor_id][Keys.DAYS_REMAINING] = self.virus_config[Keys.AVERAGE_DURATION] + durationVariation
                        self.network.nodes[neighbor_id][Keys.STATUS] = 'I'
                        bfs_queue.append(neighbor_id)
                        susceptible -= 1
                        infected += 1
                        self.network.nodes[node_id][Keys.SECONDARY_INFECTIONS] += 1

            statistics.append((susceptible, infected, removed, secondary_infections))
            bfs_queue = [x for x in bfs_queue if self.network.nodes[x][Keys.STATUS] != 'R']
            random.shuffle(bfs_queue)

        return statistics


    def simulate(self):
        
        statistics = self.contaminate()
        x = list(range(len(statistics)))

        susceptible = [sum(statistic[:2]) for statistic in statistics]
        susceptible_smooth = gaussian_filter1d(susceptible, sigma=2)
        infected = [statistic[1] for statistic in statistics]
        infected_smooth = gaussian_filter1d(infected, sigma=2)
        removed = [sum(statistic[:3]) for statistic in statistics]

        effective_reproduction, new_cases = [1], [1]
        yesterday_statistic = statistics[0]
        for today_statistic in statistics[1:]:
            infected_delta = today_statistic[1] - yesterday_statistic[1]
            recovery_delta = today_statistic[2] - yesterday_statistic[2]
            new_cases.append(infected_delta + recovery_delta)
            if recovery_delta:
                secondary_delta = today_statistic[3] - yesterday_statistic[3]
                effective_reproduction.append(secondary_delta / recovery_delta)
            else:
                effective_reproduction.append(effective_reproduction[-1])
            yesterday_statistic = today_statistic
        shift_amount = round(self.virus_config[Keys.AVERAGE_DURATION] * (1 - self.virus_config[Keys.DEATH_PROBABILITY]) / 2)
        effective_reproduction_3_day_smooth = [sum(effective_reproduction[max(i - 3, 0) : i + 1]) / 3 for i in x]
        effective_reproduction_smooth_shift = effective_reproduction_3_day_smooth[shift_amount:] + [0] * shift_amount

        total_cases = [statistic[1] + statistic[2] for statistic in statistics]

        fig, axes = plt.subplots(2, 2, figsize=(10, 6))
        fig.tight_layout(h_pad=2, w_pad=2)
        axes[0][0].title.set_text('SIR Plot')
        axes[0][0].fill_between(x, removed, color='palegreen')
        axes[0][0].fill_between(x, susceptible_smooth, color='royalblue')
        axes[0][0].fill_between(x, infected_smooth, color='orangered')
        axes[0][0].plot(x, [self.network.graph[Keys.AVAILABLE_BEDS] for _ in x], color='black')
        axes[0][1].title.set_text('Total Cases')
        axes[0][1].plot(x, total_cases)
        axes[1][0].title.set_text('Effective Reproduction (R)')
        axes[1][0].bar(x, effective_reproduction_smooth_shift)
        axes[1][0].plot(x, [1 for _ in x], color='black')
        axes[1][1].title.set_text('New Cases')
        axes[1][1].bar(x, new_cases)
        filename = f'static/graphs/{datetime.now()}.png'
        plt.savefig(filename, bbox_inches='tight', dpi=256)

        return {
            Keys.EPIDEMIC_DURATION: len(statistics),
            Keys.PEAK_CASES: max(infected),
            Keys.TOTAL_CASES: total_cases[-1],
            Keys.OUTPUT_IMAGE_URL: filename,
        }
