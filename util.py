import networkx as nx


class Keys:
    ASYMPTOTIC_PROBABILITY = 'asymptoticProbability'
    AVAILABLE_BEDS = 'availableBeds'
    AVERAGE_DURATION = 'averageDuration'
    AVERAGE_IMMUNITY = 'averageImmunity'
    AVERAGE_SAFETY_FACTOR = 'averageSafetyFactor'
    AVERAGE_SOCIAL_DISTANCE = 'averageSocialDistance'
    AVERAGE_TRAVEL_FACTOR = 'averageTravelFactor'
    CENTRAL_HUB_COUNT = 'centralHubCount'
    DAYS_REMAINING = 'daysRemaining'
    DEATH_PROBABILITY = 'deathProbability'
    DURATION_VARIATION = 'durationVariation'
    EDGE_PROBABILITY = 'edgeProbability'
    IMMUNITY = 'immunity'
    IMMUNITY_VARIATION = 'immunityVariation'
    INFECTION_PROBABILITY = 'infectionProbability'
    INFECTION_RADIUS = 'infectionRadius'
    NETWORK_TYPE = 'networkType'
    NEW_NODE_EDGE_COUNT = 'newNodeEdgeCount'
    NODE_COUNT = 'nodeCount'
    PHYSICAL_DISTANCE = 'physicalDistance'
    QUARANTINE_PROBABILITY = 'quarantineProbability'
    QUARANTINE_STRICTNESS = 'quarantineStrictness'
    SAFETY_FACTOR = 'safetyFactor'
    SAFETY_FACTOR_VARIATION = 'safetyFactorVariation'
    SOCIAL_DISTANCE_VARIATION = 'socialDistanceVariation'
    STATUS = 'status'
    TRAVEL_BAN_STRICTNESS = 'travelBanStrictness'
    TRAVEL_FACTOR_VARIATION = 'travelFactorVariation'
    TRAVEL_PROBABILITY = 'travelProb'


class GraphFactory:

    @staticmethod
    def get_graph(config):
        if config[Keys.NETWORK_TYPE] == 'BA':
            return nx.barabasi_albert_graph(config[Keys.NODE_COUNT], config[Keys.NEW_NODE_EDGE_COUNT])
        if config[Keys.NETWORK_TYPE] == 'ER':
            return nx.erdos_renyi_graph(config[Keys.NODE_COUNT], config[Keys.EDGE_PROBABILITY])
