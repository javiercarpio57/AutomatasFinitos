import functools
import utilities
# import time
import datetime

epsilon = 'ε'

class DFA_Node():
    def __init__(self, name, nodos):
        self.name = name
        self.id = None
        self.conjunto_nodos = nodos
        self.transitions = []
        self.isMarked = False
        self.isFinal = False

        self.CreateID(nodos)

    def CreateID(self, nodos):
        a = [n.id for n in nodos]
        a.sort()
        a = [str(i) for i in a]
        self.id = ', '.join(a)

    def Mark(self):
        self.isMarked = True

    def isAcceptingState(self):
        self.isFinal = True

class DFA():
    def __init__(self, simbolos, estado_inicio, estado_fin):
        self.estados = []
        self.estado_inicial = None
        self.estados_aceptacion = []
        self.transiciones = []
        self.simbolos = simbolos

        self.count = 0
        self.rounds = 1

        self.CreateDFA(estado_inicio, estado_fin)

    def Simulate_DFA(self, exp):
        S = self.estado_inicial.name

        for e in exp:
            S = self.MoveSimulation(S, 'a')

            if S == None:
                return 'no'

        if S in self.estados_aceptacion:
            return 'yes'
            
        return 'no'

    def CreateTransitionFunction(self):
        f = {}
        for t in self.transiciones:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    def GetStates(self):
        return {s.name for s in self.estados}

    def GetAcceptingStates(self):
        return {s for s in self.estados_aceptacion}

    def CreateDFA(self, inicial, final):
        initial_state_DFA = self.e_closure([inicial])
        self.estado_inicial = DFA_Node(self.GetName(), initial_state_DFA)
        self.estados.append(self.estado_inicial)

        while not self.MarkedState():
            T = self.GetFirstUnmarkedState()
            T.Mark()

            for symbol in self.simbolos:
                if symbol != epsilon:
                    move = self.Move(T.conjunto_nodos, symbol)

                    if len(move) > 0:
                        cerradura = self.e_closure(move)
                        U = DFA_Node(self.GetName(), cerradura)
                        
                        if U.id not in [s.id for s in self.estados]:
                            if final.id in [c.id for c in cerradura]:
                                U.isAcceptingState()
                                self.estados_aceptacion.append(U.name)
                            self.estados.append(U)
                            self.transiciones.append((T.name, symbol, U.name))
                        else:
                            self.count -= 1
                            for s in self.estados:
                                if U.id == s.id:
                                    self.transiciones.append((T.name, symbol, s.name))
                            
                        # self.transiciones.append((T.name, symbol, U.name))
    
    def GetName(self):
        if self.count == 0:
            self.count += 1
            return 'S'

        possible_names = ' ABCDEFGHIJKLMNOPQRTUVWXYZ'
        name = possible_names[self.count]
        self.count += 1

        if self.count == len(possible_names):
            self.rounds += 1
            self.count = 0

        return name * self.rounds

    def GetFirstUnmarkedState(self):
        for n in self.estados:
            if not n.isMarked:
                return n
        
    def MarkedState(self):
        marks = [n.isMarked for n in self.estados]
        return functools.reduce(lambda a, b: a and b, marks)

    def CheckArrayStates(self, states, n):
        return str(n.id) in [str(s.id) for s in states]

    def e_closure(self, states):
        stack = [] + states
        closure = [] + states

        while len(stack) != 0:
            t = stack.pop()

            for transition in t.transitions:
                s, state = [*transition]
                if epsilon == s:
                    if not self.CheckArrayStates(closure, state):
                        stack.append(state)
                        closure.append(state)
        return closure

    def Move(self, T, symbol):
        moves = []
        for t in T:
            for transition in t.transitions:
                s, state = [*transition]
                if symbol == s:
                    moves.append(state)
        return moves

    def MoveSimulation(self, Nodo, symbol):
        move = None
        for i in self.transiciones:
            if i[0] == Nodo and i[1] == symbol:
                move = i[2]

        return move

class Node:
    def __init__(self, codigo, transitions = []):
        self.id = codigo
        self.transitions = transitions

    def toString(self):
        return (f'Nodo: {self.id} --- {self.VerTransisiones()}')

    def AddTransition(self, simbolo, estado):
        self.transitions.append((simbolo, estado))

    def VerTransisiones(self):
        sTransicion = ''
        for t in self.transitions:
            sTransicion += f'\n\t{self.id} --> "{t[0]}" --> {t[1].id}'

        return sTransicion

class AFN:
    def __init__(self, expresion_regular):
        self.estado_inicial = None
        self.estado_final = None
        self.estados = []
        self.simbolos = []
        self.ids = 0

        expresion_regular = self.CleanExpression(expresion_regular)
        print('EXPRESION REESCRITA:', expresion_regular)
        self.Evaluar(expresion_regular)

    def Simulate_NFA(self, exp):
        S = self.e_closure([self.estado_inicial])

        for e in exp:
            S = self.e_closure(self.Move(S, e))

        if str(self.estado_final.id) in [str(s.id) for s in S]:
            return 'yes'
        else:
            return 'no'

    def CheckArrayStates(self, states, n):
        return str(n.id) in [str(s.id) for s in states]

    def e_closure(self, states):
        stack = [] + states
        closure = [] + states

        while len(stack) != 0:
            t = stack.pop()

            for transition in t.transitions:
                s, state = [*transition]
                if epsilon == s:
                    if not self.CheckArrayStates(closure, state):
                        stack.append(state)
                        closure.append(state)

        return closure

    def Move(self, T, symbol):
        moves = []
        for t in T:
            for transition in t.transitions:
                s, state = [*transition]
                if symbol == s:
                    moves.append(state)

        return moves

    def GetStates(self):
        return {str(s.id) for s in self.estados}

    def CreateTransitionFunction(self):
        f = {}
        for e in self.estados:
            cont = 1
            f[str(e.id)] = {}

            for t in e.transitions:
                symbol, node = [*t]

                if str(symbol) in f[str(e.id)].keys():
                    f[str(e.id)][str(symbol) + ' '*cont] = str(node.id)
                    cont += 1
                else:
                    f[str(e.id)][str(symbol)] = str(node.id)
        return f

    def CleanExpression(self, regular):
        real = []
        exp = []
        hasExpression = False
        hasPlus = False
        initial = []
        final = 0
        i = 0

        if ')+' in regular:
            while i < len(regular):
                if regular[i] == '(':
                    initial.append(i)                        

                if regular[i] == ')':
                    real.append(regular[i])
                    if regular[i + 1] == '+':
                        final = i + 1
                        real.append('*')
                        real.append('.')
                        real.append(regular[initial.pop() : final])
                        i += 1
                    else:
                        initial.pop()

                else:
                    real.append(regular[i])
                i += 1

            regular = ''.join(real)

        if ')?' in regular:
            while i < len(regular):
                if regular[i] == '(':
                    initial.append(i)                        

                if regular[i] == ')':
                    real.append(regular[i])
                    if regular[i + 1] == '?':
                        final = i + 1
                        real.append('|')
                        real.append(epsilon)
                        real.append(')')
                        real.insert(initial[-1], '(')
                        print(initial[-1])
                        i += 1
                    else:
                        initial.pop()

                else:
                    real.append(regular[i])
                i += 1

            regular = ''.join(real)

        regular_copy = regular
        if '+' in regular:
            while '+' in regular_copy:
                i = regular_copy.find('+')
                symbol = regular_copy[i - 1]

                regular_copy = regular_copy.replace(symbol + '+', '(' + symbol + '*.' + symbol + ')')

        if '?' in regular_copy:
            while '?' in regular_copy:
                i = regular_copy.find('?')
                symbol = regular_copy[i - 1]

                regular_copy = regular_copy.replace(symbol + '?', '(' + symbol + '|' + epsilon + ')')

        return regular_copy

    def MergeNodes(self, nodeA, nodeB):
        print('MERGING:', nodeA.id, nodeB.id)
        # Quitar de estados
        nodeA.transitions += nodeB.transitions
        i = self.estados.index(nodeB)
        self.estados.pop(i)

    def CreateORNodes(self, a, b, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if a not in self.simbolos and a != None:
            self.simbolos.append(a)
        if b not in self.simbolos and b != None:
            self.simbolos.append(b)
        
        if not haGeneradoPrimerGrafo:
            # Nodo final de OR
            nodoF = Node(self.ids + 6, [])

            nodoFinalA = Node(self.ids + 5, [(epsilon, nodoF)])
            nodoFinalB = Node(self.ids + 4, [(epsilon, nodoF)])

            nodoInicialA = Node(self.ids + 3, [(a, nodoFinalA)])
            nodoInicialB = Node(self.ids + 2, [(b, nodoFinalB)])

            # Nodo inicial de OR
            nodoI = Node(self.ids + 1, [(epsilon, nodoInicialA), (epsilon, nodoInicialB)])

            self.ids += 6

            # Estados
            self.estados.append(nodoF)
            self.estados.append(nodoFinalA)
            self.estados.append(nodoFinalB)
            self.estados.append(nodoInicialA)
            self.estados.append(nodoInicialB)
            self.estados.append(nodoI)

            return nodoI, nodoF, nodoI, nodoF
        else:
            if a != None and b != None:
                # Nodo final de OR
                nodoF = Node(self.ids + 6, [])

                nodoFinalA = Node(self.ids + 5, [(epsilon, nodoF)])
                nodoFinalB = Node(self.ids + 4, [(epsilon, nodoF)])

                nodoInicialA = Node(self.ids + 3, [(a, nodoFinalA)])
                nodoInicialB = Node(self.ids + 2, [(b, nodoFinalB)])

                # Nodo inicial de OR
                nodoI = Node(self.ids + 1, [(epsilon, nodoInicialA), (epsilon, nodoInicialB)])

                self.ids += 6

                # Estados
                self.estados.append(nodoF)
                self.estados.append(nodoFinalA)
                self.estados.append(nodoFinalB)
                self.estados.append(nodoInicialA)
                self.estados.append(nodoInicialB)
                self.estados.append(nodoI)

                return nodoInicial, nodoFA, nodoI, nodoF
            elif a == None and b == None:
                # Nodo final de OR
                nodoF = Node(self.ids + 2, [])

                # Nodo inicial de OR
                nodoI = Node(self.ids + 1, [(epsilon, nodoInicial), (epsilon, nodoIB)])

                nodoFA.AddTransition(epsilon, nodoF)
                nodoFinal.AddTransition(epsilon, nodoF)

                self.ids += 2

                # Estados
                self.estados.append(nodoF)
                self.estados.append(nodoI)

                return nodoI, nodoF, nodoI, nodoF

            elif a == None and b != None:
                nodoF = Node(self.ids + 4, [])

                nodoFinalB = Node(self.ids + 3, [(epsilon, nodoF)])
                nodoInicialB = Node(self.ids + 2, [(b, nodoFinalB)])

                nodoI = Node(self.ids + 1, [(epsilon, nodoInicial), (epsilon, nodoInicialB)])
                nodoFinal.AddTransition(epsilon, nodoF)

                self.ids += 4

                # Estados
                self.estados.append(nodoF)
                self.estados.append(nodoFinalB)
                self.estados.append(nodoInicialB)
                self.estados.append(nodoI)

                if nodoFinal.id == nodoFA.id:
                    return nodoI, nodoF, nodoIB, nodoF
                else:
                    return nodoI, nodoFA, nodoIB, nodoF
                
            elif a != None and b == None:
                nodoF = Node(self.ids + 4, [])

                nodoFinalA = Node(self.ids + 3, [(epsilon, nodoF)])
                nodoInicialA = Node(self.ids + 2, [(a, nodoFinalA)])

                nodoI = Node(self.ids + 1, [(epsilon, nodoIB), (epsilon, nodoInicialA)])
                nodoFinal.AddTransition(epsilon, nodoF)

                self.ids += 4

                # Estados
                self.estados.append(nodoF)
                self.estados.append(nodoFinalA)
                self.estados.append(nodoInicialA)
                self.estados.append(nodoI)

                return nodoInicial, nodoFA, nodoI, nodoF

    def CreateCATNodes(self, a, b, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if a not in self.simbolos and a != None:
            self.simbolos.append(a)
        if b not in self.simbolos and b != None:
            self.simbolos.append(b)
        
        if not haGeneradoPrimerGrafo:
            # Nodo final de CAT
            node3 = Node(self.ids + 3, [])

            # Nodo en medio de CAT
            node2 = Node(self.ids + 2, [(b, node3)])

            # Nodo inicial de CAT
            node1 = Node(self.ids + 1, [(a, node2)])
            self.ids += 3

            self.estados.append(node1)
            self.estados.append(node2)
            self.estados.append(node3)

            return node1, node3, node1, node3
        else:
            if a != None and b != None:
                # Nodo final de CAT
                node3 = Node(self.ids + 3, [])

                # Nodo en medio de CAT
                node2 = Node(self.ids + 2, [(b, node3)])

                # Nodo inicial de CAT
                node1 = Node(self.ids + 1, [(a, node2)])
                self.ids += 3

                self.estados.append(node1)
                self.estados.append(node2)
                self.estados.append(node3)

                return nodoInicial, nodoFA, node1, node3
            elif a == None and b == None:
                self.MergeNodes(nodoFA, nodoIB)

                return nodoInicial, nodoFinal, nodoInicial, nodoFinal
                
            elif a != None and b == None:
                nodoI = Node(self.ids + 1, [(a, nodoIB)])
                self.estados.append(nodoI)
                self.ids += 1

                if nodoFinal.id == nodoFA.id:
                    return nodoI, nodoF, nodoI, nodoFinal
                else:
                    return nodoInicial, nodoFA, nodoI, nodoFinal

                # return nodoI, nodoFinal, nodoI, nodoFinal

            elif a == None and b != None:
                nodoF = Node(self.ids + 1, [])
                self.estados.append(nodoF)
                nodoFinal.AddTransition(b, nodoF)
                self.ids += 1

                if nodoFinal.id == nodoFA.id:
                    return nodoInicial, nodoF, nodoIB, nodoF
                else:
                    return nodoInicial, nodoFA, nodoIB, nodoF

    def CreateSTARNodes(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if not haGeneradoPrimerGrafo:
            # Nodo final de CAT
            node4 = Node(self.ids + 4, [])

            # Nodo en medio final de CAT
            node3 = Node(self.ids + 3, [(epsilon, node4)])

            # Nodo en medio inicial de CAT
            node2 = Node(self.ids + 2, [(a, node3)])

            # Nodo inicial de CAT
            node1 = Node(self.ids + 1, [(epsilon, node2), (epsilon, node4)])

            node3.AddTransition(epsilon, node2)
            self.ids += 4

            self.estados.append(node1)
            self.estados.append(node2)
            self.estados.append(node3)
            self.estados.append(node4)

            return node1, node4, node1, node4
        else:
            if a == None:
                # Nodo final de *
                node4 = Node(self.ids + 2, [])

                # Nodo inicial de *
                node1 = Node(self.ids + 1, [(epsilon, nodoIB), (epsilon, node4)])

                nodoFinal.AddTransition(epsilon, node4)
                nodoFinal.AddTransition(epsilon, nodoIB)
                self.ids += 2

                self.estados.append(node1)
                self.estados.append(node4)

                if nodoIB.id == nodoInicial.id:
                    return node1, node4, node1, node4
                else:
                    return nodoInicial, nodoFA, node1, node4

            elif a != None:
                # Nodo final de *
                node4 = Node(self.ids + 4, [])

                # Nodo en medio final de *
                node3 = Node(self.ids + 3, [(epsilon, node4)])

                # Nodo en medio inicial de *
                node2 = Node(self.ids + 2, [(a, node3)])

                # Nodo inicial de *
                node1 = Node(self.ids + 1, [(epsilon, node2), (epsilon, node4)])

                node3.AddTransition(epsilon, node2)
                self.ids += 4

                self.estados.append(node1)
                self.estados.append(node2)
                self.estados.append(node3)
                self.estados.append(node4)

                return nodoInicial, nodoFA, node1, node4

    def CreatePlusNodes(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        self.estado_inicial, node2, node3, self.estado_final = self.CreateSTARNodes(a, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        self.estado_inicial, node2, node3, self.estado_final = self.CreateCATNodes(None, a, True, self.estado_inicial, node2, node3, self.estado_final)
        return self.estado_inicial, node2, node3, self.estado_final

    def CreateOptionalNodes(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        node1, node2, node3, node4 = self.CreateORNodes(a, epsilon, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        return nodoInicial, nodoFA, node3, node4

    def ObtenerPrecedencia(self, operator):
        if operator == '|':
            return 1
        if operator == '.':
            return 2
        if operator == '*' or operator == '+' or operator == '?':
            return 3
        return 0

    def Operar(self, x, y, operator, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if operator == '|': return self.CreateORNodes(x, y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        if operator == '.': return self.CreateCATNodes(x, y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        if operator == '*': return self.CreateSTARNodes(y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        if operator == '+': return self.CreatePlusNodes(y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        if operator == '?': return self.CreateOptionalNodes(y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)

    def EsSimbolo(self, digit):
        digitos = 'abcdefghijklmnopqrstuvwxyz' + epsilon
        if digit in digitos:
            return True
        return False

    def Evaluar(self, expresion):
        simbolos = []
        operaciones = []
        intermedioA = None
        intermedioB = None
        i = 0

        haGeneradoPrimerGrafo = False
        
        while i < len(expresion):
            if expresion[i] == '(':
                operaciones.append(expresion[i])

            elif self.EsSimbolo(expresion[i]):
                val = ''

                while i < len(expresion) and self.EsSimbolo(expresion[i]):
                    val += expresion[i]
                    i += 1

                simbolos.append(val)
                i -= 1

            elif expresion[i] == ')':
                while len(operaciones) != 0 and operaciones[-1] != '(':
                    op = operaciones.pop()
                    val2 = simbolos.pop()
                    val1 = None

                    if op != '*' and op != '+' and op != '?':
                        val1 = simbolos.pop()
                    
                    self.estado_inicial, intermedioA, intermedioB, self.estado_final = self.Operar(val1, val2, op, haGeneradoPrimerGrafo, self.estado_inicial, intermedioA, intermedioB, self.estado_final)
                    
                    simbolos.append(None)

                    if not haGeneradoPrimerGrafo:
                        haGeneradoPrimerGrafo = True

                operaciones.pop()

            else:
                while (len(operaciones) != 0
                    and self.ObtenerPrecedencia(operaciones[-1]) >= self.ObtenerPrecedencia(expresion[i])):
                    op = operaciones.pop()
                    val2 = simbolos.pop()
                    val1 = None

                    if op != '*' and op != '+' and op != '?':
                        val1 = simbolos.pop()
                    
                    self.estado_inicial, intermedioA, intermedioB, self.estado_final = self.Operar(val1, val2, op, haGeneradoPrimerGrafo, self.estado_inicial, intermedioA, intermedioB, self.estado_final)

                    simbolos.append(None)

                    if not haGeneradoPrimerGrafo:
                        haGeneradoPrimerGrafo = True

                operaciones.append(expresion[i])

            i += 1

        while len(operaciones) != 0:
            op = operaciones.pop()
            val2 = simbolos.pop()
            val1 = None

            if op != '*' and op != '+' and op != '?':
                val1 = simbolos.pop()
            
            self.estado_inicial, intermedioA, intermedioB, self.estado_final = self.Operar(val1, val2, op, haGeneradoPrimerGrafo, self.estado_inicial, intermedioA, intermedioB, self.estado_final)

            simbolos.append(None)

            if not haGeneradoPrimerGrafo:
                haGeneradoPrimerGrafo = True


exp = input('Ingrese expresion regular: ')
w = input('Ingrese una cadena: ')



afn = AFN(exp)

states = afn.GetStates()
initial_state = str(afn.estado_inicial.id)
accepting_state = {str(afn.estado_final.id)}
transition_function = afn.CreateTransitionFunction()
alphabet, alphabet_print = utilities.getAlphabet(transition_function)

# ------------------------------------------------------

print('\n-------------------------------------------------------------')

print('ESTADOS =', states)
print('SIMBOLOS =', alphabet_print)
print('INICIO =', {initial_state})
print('ACEPTACION =', accepting_state)
print('TRANSICION =', utilities.GetTransitions(transition_function))
print('')

begin_time = datetime.datetime.now()
print(f'¿{w} cumple con {exp}?', afn.Simulate_NFA(w))
total_time = (datetime.datetime.now() - begin_time).total_seconds()
print(f' -- {total_time} seconds --')

print('-------------------------------------------------------------\n')
# ------------------------------------------------------

utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'NFA')

# ------------------------------------------------------




dfa = DFA([s for s in alphabet_print], afn.estado_inicial, afn.estado_final)

states = dfa.GetStates()
initial_state = dfa.estado_inicial.name
accepting_state = dfa.GetAcceptingStates()
transition_function = dfa.CreateTransitionFunction()
alphabet, alphabet_print = utilities.getAlphabet(transition_function)

# ------------------------------------------------------

print('\n-------------------------------------------------------------')

print('ESTADOS =', states)
print('SIMBOLOS =', alphabet_print)
print('INICIO =', {initial_state})
print('ACEPTACION =', accepting_state)
print('TRANSICION =', utilities.GetTransitions(transition_function))

print('')

begin_time = datetime.datetime.now()
print(f'¿{w} cumple con {exp}?', dfa.Simulate_DFA(w))
total_time = (datetime.datetime.now() - begin_time).total_seconds()
print(f' -- {total_time} seconds --')

print('-------------------------------------------------------------\n')

utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'DFA')
utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'DFA_minimize', True)


