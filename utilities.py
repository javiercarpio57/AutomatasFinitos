from pythomata import SimpleDFA

def getStates(states):
    return {str(s.id) for s in states}

def getAlphabet(transicion):
    alphabet = []
    for v in transicion.values():
        for k in v.keys():
            alphabet.append(k)

    return { *alphabet }

def getTransitionFunction(transitions):
    f = {}
    for keys, values in transitions.items():
        cont = 1
        f[str(keys[0])] = {}

        for n in values:
            if str(keys[1]) in f[str(keys[0])].keys():
                f[str(keys[0])][str(keys[1]) + '_'*cont] = str(n)
                cont += 1
            else:
                f[str(keys[0])][str(keys[1])] = str(n)

    return f

def graph_automata(states, alphabet, initial_state, accepting_states, transition_function):
    dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)

    graph = dfa.to_graphviz()
    graph.render('prueba')