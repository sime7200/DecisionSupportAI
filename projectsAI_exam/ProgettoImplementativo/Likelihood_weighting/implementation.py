import pysmile
import pysmile_license
import random


def topological_order(net):
    visited = set()
    order = []

    def dfs(node):
        nonlocal visited, order
        visited.add(node)
        children = net.get_children(node)
        for child in children:
            if child not in visited:
                dfs(child)
        if not isinstance(node, (int, float)):
            order.append(node)

    for node_id in net.get_all_node_ids():
        if node_id not in visited:
            dfs(node_id)

    return order

# per trovare l'indice della colonna giusta
def get_first_index(net, node, probabilities, single_sample):
    init = 0
    lenght = len(probabilities)

    parents = net.get_parent_ids(node)
    # scorro i genitori cioè Success/Failure e dopo Up/Flat/Down
    for parent in parents:
        lenght = lenght / net.get_outcome_count(parent) # prima divisione per 2, l'altra per 3 perchè 3 outcome
        outcome = net.get_outcome_ids(parent).index(single_sample[parent]) # prendo l'indice del nome della colonna in quel campione
        print(outcome, single_sample[parent])
        init = init + (lenght * outcome)

    return int(init)



def likelihood_weighting(network, evidence, varX, num_run):
    net = pysmile.Network()
    net.read_file(network)
    counts = {value: 0 for value in net.get_outcome_ids(varX)} # {'True': 0, 'False': 0} numero di volte che True e False compariranno nei campioni
    total_weight = 0
    for _ in range(num_run):
        single_sample = {} # assegnamento a ogni variabile della rete valori random per num_run volte
        weight = 1.0 
        # order = ['Cloudy', 'Rain', 'Sprinkler', 'Wet_grass']
        for var in topological_order(net):
            # se evidence assegno il valore osservato
            if var in evidence:
                single_sample[var] = evidence[var]
                probabilities = net.get_node_definition(var)
                # indice di probabilities corrispondente all'evidenza
                outcome_index = get_first_index(net, var, probabilities, single_sample) # nell'es di SMILE posso avere 0,3,6,9,12,15 (indice di ogni primo valore in ogni colonna)
                outcome_index += net.get_outcome_ids(var).index(single_sample[var]) # a quel numero poi aggiungo 0, 1 o 2 per ottenere ogni cella da 0 a 17
                weight *= probabilities[outcome_index] # ossia weight * 0.1 nel caso di Sprinkler
            else:
                valori = net.get_outcome_ids(var)
                probabilities = net.get_node_definition(var)
                outcome_index = get_first_index(net, var, probabilities, single_sample)
                conditional_prob = probabilities[outcome_index:outcome_index+net.get_outcome_count(var)]
                sample_val = random.choices(valori, weights=conditional_prob)[0] # [0] serve per prendere il primo valore
                single_sample[var] = sample_val
                weight *= probabilities[outcome_index+valori.index(sample_val)]
     
        counts[single_sample[varX]] += weight
        total_weight += weight

    # normalizzazione a 1 -> ogni count diviso la somma tot di count
    probabilities = {value: count / total_weight for value, count in counts.items()}

    return probabilities



network_file = "Likelihood_weighting/WetGrass.xdsl"
evidence = {'Sprinkler': 'On'}
var = "Rain"
num_run = 5

result = likelihood_weighting(network_file, evidence, var, num_run)
print(f"P({var} | 'Sprinkler': 'On'): {result}")