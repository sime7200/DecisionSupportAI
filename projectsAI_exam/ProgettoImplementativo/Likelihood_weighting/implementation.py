import pysmile
import pysmile_license
import random


def likelihood_weighting(network, evidence, varX, num_run):
    net = pysmile.Network()
    net.read_file(network)
    counts = {value: 0 for value in net.get_outcome_ids(varX)} # {'True': 0, 'False': 0} numero di volte che True e False compariranno nei campioni
    for _ in range(num_run):
        single_sample = {} # assegnamento a ogni variabile della rete valori random per num_run volte
        weight = 1.0
        for var in net.get_all_node_ids():
            # se evidence assegno il valore osservato
            if var in evidence:
                single_sample[var] = evidence[var]
                probabilities = net.get_node_definition(var)
                # indice di probabilities corrispondente all'evidenza
                #outcome_index = net.get_outcome_ids(var).index(evidence[var]) 
                outcome_index = net.get_evidence(var)   # ------------------ provare
                print(outcome_index)
                weight *= probabilities[outcome_index]
            else:
                valori = net.get_outcome_ids(var)
                prob = net.get_node_definition(var)
                pesiValori = []
                # considero solo le prob nella prima colonna, non quelle condizionate
                for i in range(int(len(valori))):
                    pesiValori.append(prob[i])
                sample_val = random.choices(list(valori), weights=list(pesiValori))[0] # [0] serve per prendere il primo valore
                single_sample[var] = sample_val
                weight *= prob[valori.index(sample_val)]
     
        counts[single_sample[varX]] += weight

    # normalizzazione a 1 -> ogni count diviso la somma tot di count
    total_weight = sum(counts.values())
    probabilities = {value: count / total_weight for value, count in counts.items()}

    return probabilities




network_file = "Likelihood_weighting/WetGrass.xdsl"
evidence = {'Sprinkler': 'On'}
var = "Cloudy"
num_run = 1000

result = likelihood_weighting(network_file, evidence, var, num_run)
print(f"P({var} | 'Sprinkler': 'On'): {result}")