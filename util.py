import networkx as nx


class Keys:
    
    ASYMPTOTIC_PROBABILITY = 'asymptoticProbability'
    AVAILABLE_BEDS = 'availableBeds'
    AVERAGE_DEGREE = 'averageDegree'
    AVERAGE_DURATION = 'averageDuration'
    AVERAGE_IMMUNITY = 'averageImmunity'
    AVERAGE_NUMBER_OF_PHYICAL_CONTACTS = 'averageNumberOfPhysicalContacts'
    AVERAGE_SAFETY_FACTOR = 'averageSafetyFactor'
    AVERAGE_SOCIAL_DISTANCE = 'averageSocialDistance'
    AVERAGE_TRAVEL_FACTOR = 'averageTravelFactor'
    CENTRAL_HUB_COUNT = 'centralHubCount'
    DAYS_REMAINING = 'daysRemaining'
    DEATH_PROBABILITY = 'deathProbability'
    DURATION_VARIATION = 'durationVariation'
    EPIDEMIC_DURATION = 'epidemicDuration'
    IMMUNITY = 'immunity'
    IMMUNITY_VARIATION = 'immunityVariation'
    INFECTION_PROBABILITY = 'infectionProbability'
    INFECTION_RADIUS = 'infectionRadius'
    NETWORK_TYPE = 'networkType'
    NEW_NODE_EDGE_COUNT = 'newNodeEdgeCount'
    NODE_COUNT = 'nodeCount'
    NUMBER_OF_PHYICAL_CONTACTS = 'noOfPhysicalContacts'
    NUMBER_OF_PHYICAL_CONTACTS_VARIATION = 'numberOfPhysicalContactsVariation'
    OUTPUT_IMAGE_URL = 'outputImageUrl'
    PEAK_CASES = 'peakCases'
    PHYSICAL_DISTANCE = 'physicalDistance'
    QUARANTINE_PROBABILITY = 'quarantineProbability'
    QUARANTINE_STRICTNESS = 'quarantineStrictness'
    SAFETY_FACTOR = 'safetyFactor'
    SAFETY_FACTOR_VARIATION = 'safetyFactorVariation'
    SECONDARY_INFECTIONS =  'secondaryInfections'
    SOCIAL_DISTANCE_VARIATION = 'socialDistanceVariation'
    STATUS = 'status'
    TOTAL_CASES = 'totalCases'
    TRAVEL_BAN_STRICTNESS = 'travelBanStrictness'
    TRAVEL_FACTOR_VARIATION = 'travelFactorVariation'
    TRAVEL_PROBABILITY = 'travelProb'


class GraphFactory:

    @staticmethod
    def get_graph(config):
        if config[Keys.NETWORK_TYPE] == 'BA':
            return nx.barabasi_albert_graph(config[Keys.NODE_COUNT], config[Keys.NEW_NODE_EDGE_COUNT])
        if config[Keys.NETWORK_TYPE] == 'ER':
            n = config[Keys.NODE_COUNT]
            p = config[Keys.AVERAGE_DEGREE] / config[Keys.NODE_COUNT]
            return nx.erdos_renyi_graph(n, p)


default_app_input = {
    'network_config.' + Keys.NODE_COUNT: 1000,
    'network_config.' + Keys.CENTRAL_HUB_COUNT: 25,
    'network_config.' + Keys.AVERAGE_DEGREE: 10,
    'network_config.' + Keys.QUARANTINE_STRICTNESS: 0.9,
    'network_config.' + Keys.QUARANTINE_PROBABILITY: 0.25,
    'network_config.' + Keys.AVAILABLE_BEDS: 100,
    'network_config.' + Keys.AVERAGE_IMMUNITY: 0.2,
    'network_config.' + Keys.IMMUNITY_VARIATION: 0.1,
    'network_config.' + Keys.AVERAGE_SOCIAL_DISTANCE: 1.25, # metres
    'network_config.' + Keys.SOCIAL_DISTANCE_VARIATION: 1.0, # metres
    'network_config.' + Keys.AVERAGE_SAFETY_FACTOR: 0.0,
    'network_config.' + Keys.SAFETY_FACTOR_VARIATION: 0.1,
    'network_config.' + Keys.AVERAGE_TRAVEL_FACTOR: 0.3,
    'network_config.' + Keys.TRAVEL_FACTOR_VARIATION: 0.2,
    'network_config.' + Keys.TRAVEL_BAN_STRICTNESS: 0,
    'network_config.' + Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS: 5,
    'network_config.' + Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION: 2,
    'virus_config.' + Keys.AVERAGE_DURATION: 9, # days
    'virus_config.' + Keys.DURATION_VARIATION: 2, # days
    'virus_config.' + Keys.DEATH_PROBABILITY: 0.05,
    'virus_config.' + Keys.INFECTION_PROBABILITY: 0.05,
    'virus_config.' + Keys.INFECTION_RADIUS: 2, # metres
    'virus_config.' + Keys.ASYMPTOTIC_PROBABILITY: 0.1,
}

field_metadata = {
    'network_config.' + Keys.NODE_COUNT: {
        'name': 'Population (number of nodes)',
        'minVal': 100,
        'maxVal': 5000,
        'step': 100,
    },
    'network_config.' + Keys.CENTRAL_HUB_COUNT: {
        'name': 'Community centres',
        'minVal': 0,
        'maxVal': 500,
        'step': 5,
    },
    'network_config.' + Keys.AVERAGE_DEGREE: {
        'name': 'Average friend count (node degree)',
        'minVal': 1,
        'maxVal': 250,
    },
    'network_config.' + Keys.QUARANTINE_STRICTNESS: {
        'name': 'Quarantine Strictness',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.QUARANTINE_PROBABILITY: {
        'name': 'Quarantine Probability',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.AVAILABLE_BEDS: {
        'name': 'Total Hospital Beds',
        'minVal': 0,
        'maxVal': 1000,
        'step': 5,
    },
    'network_config.' + Keys.AVERAGE_IMMUNITY: {
        'name': 'Average Immunity of Population',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.IMMUNITY_VARIATION: {
        'name': 'Immunity variation across Population',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.AVERAGE_SOCIAL_DISTANCE: {
        'name': 'Average social distance (m) among Population',
        'minVal': 0.1,
        'maxVal': 10,
        'step': 0.05
    },
    'network_config.' + Keys.SOCIAL_DISTANCE_VARIATION: {
        'name': 'Social distance variation across Population',
        'minVal': 0,
        'maxVal': 5,
        'step': 0.05
    },
    'network_config.' + Keys.AVERAGE_SAFETY_FACTOR: {
        'name': 'Average adherance to safety measures',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.SAFETY_FACTOR_VARIATION: {
        'name': 'Adherance to safety measures variation across Population',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.AVERAGE_TRAVEL_FACTOR: {
        'name': 'Average travel probability',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.TRAVEL_FACTOR_VARIATION: {
        'name': 'Travel probability variation across Population',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.TRAVEL_BAN_STRICTNESS: {
        'name': 'Travel ban strictness',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'network_config.' + Keys.AVERAGE_NUMBER_OF_PHYICAL_CONTACTS: {
        'name': 'Average physical contacts bet 2 people per day',
        'minVal': 0,
        'maxVal': 25
    },
    'network_config.' + Keys.NUMBER_OF_PHYICAL_CONTACTS_VARIATION: {
        'name': 'Physical contacts variation',
        'minVal': 0,
        'maxVal': 10
    },
    'virus_config.' + Keys.AVERAGE_DURATION: {
        'name': 'Average duration of Infection',
        'minVal': 0,
        'maxVal': 30
    },
    'virus_config.' + Keys.DURATION_VARIATION: {
        'name': 'Duration variation of Infection',
        'minVal': 0,
        'maxVal': 10
    },
    'virus_config.' + Keys.DEATH_PROBABILITY: {
        'name': 'Probability of infected person dying (per day)',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'virus_config.' + Keys.INFECTION_PROBABILITY: {
        'name': 'Infection probability of the Virus',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
    'virus_config.' + Keys.INFECTION_RADIUS: {
        'name': 'Infection radius of the Virus',
        'minVal': 0.1,
        'maxVal': 10,
        'step': 0.05
    },
    'virus_config.' + Keys.ASYMPTOTIC_PROBABILITY: {
        'name': 'Probability of infection to be asymptomatic',
        'minVal': 0,
        'maxVal': 1,
        'step': 0.05,
    },
}