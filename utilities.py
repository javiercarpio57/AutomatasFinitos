from pythomata import SimpleDFA

def GetTransitions(transitions):
    trans = ''
    for key, value in transitions.items():
        for s, n in value.items():
            s_real = s.replace(' ', '')
            trans += f'({key}, {s_real}, {n})' + ' - '
            # print(f'({key}, {s_real}, {n})')

    return trans

def getAlphabet(transicion):
    alphabet = []
    for v in transicion.values():
        for k in v.keys():
            alphabet.append(k)

    return { *alphabet }, { *[a.replace(' ', '') for a in alphabet] }

def graph_automata(states, alphabet, initial_state, accepting_states, transition_function, name, minimize = False):
    dfa = SimpleDFA(states, alphabet, initial_state, accepting_states, transition_function)

    if minimize:
        graph = dfa.minimize().trim().to_graphviz()
    else:
        graph = dfa.to_graphviz()
    graph.render(name)