from pythomata import SimpleDFA

def Diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def Intersect(nums1, nums2):
      m = {}
      if len(nums1)<len(nums2):
         nums1,nums2 = nums2,nums1
      for i in nums1:
         if i not in m:
            m[i] = 1
         else:
            m[i]+=1
      result = []
      for i in nums2:
         if i in m and m[i]:
            m[i]-=1
            result.append(i)
      return result

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

def write_file(text, filename):
    f = open(filename, 'a', encoding='utf-8')
    f.write(text)
    f.close()