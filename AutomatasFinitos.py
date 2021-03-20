import functools
import utilities
from time import perf_counter
# import datetime

epsilon = 'ε'

class Minimization():
    def __init__(self, funcion_transicion, estados, estados_aceptacion, simbolos, estado_inicial):
        self.last_particion = []
        self.new_particion = []
        self.transiciones = funcion_transicion
        self.estado_inicial = estado_inicial
        self.estados_aceptacion = estados_aceptacion
        self.estados = []

        self.last_particion = self.CreatePartition(estados, estados_aceptacion)
        self.Minimize(simbolos)

    # Crea las transiciones a partir de las calculadas en los nodos.
    def CreateTransitionFunction(self):
        f = {}
        for t in self.transiciones:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    # Obtiene los estados de la minimizacion.
    def GetStates(self):
        return {s for s in self.estados}

    # Crea las particiones para el algoritmo.
    def CreatePartition(self, estados, estados_aceptacion):
        set1 = []
        set2 = []
        for e in estados:
            if e in estados_aceptacion:
                set1.append(e)
            else:
                set2.append(e)

        return [set1, set2]

    # Implementacion del algoritmo de minimizacion.
    def Minimize(self, simbolos):
        new = []
        moreParition = [[]]
        primeraVez = True
        
        while len(functools.reduce(lambda x, y: x + y, moreParition)) != 0 or primeraVez:
            moreParition = []
            if primeraVez:
                primeraVez = False

            for s in self.last_particion:
                for symbol in simbolos:
                    for estado_index_1 in range(0, len(s) - 1):
                        if s[estado_index_1] in new:
                            continue
                        for estado_index_2 in range(estado_index_1 + 1, len(s)):
                            if s[estado_index_2] in new:
                                continue
                            q_1 = s[estado_index_1]
                            quien_q1 = self.GetMove(q_1, symbol)
                            q_2 = s[estado_index_2]
                            quien_q2 = self.GetMove(q_2, symbol)

                            if quien_q1 == None or quien_q2 == None:
                                continue

                            grupo_q1 = self.GetGroup(self.last_particion, quien_q1)
                            grupo_q2 = self.GetGroup(self.last_particion, quien_q2)

                            if grupo_q1 != grupo_q2:
                                new.append(q_2)
                
                moreParition.append(new)
                new = []
            self.last_particion = self.CreateMorePartitions(self.last_particion, moreParition)
        self.estados = [i[0] for i in self.last_particion if len(i) > 0]

        self.MergeNodes()
            
    # Union entre dos nodos que son iguales, para reducir redundancias.
    def MergeNodes(self):
        newEstadosFinal = []
        for l in self.last_particion:
            if self.estado_inicial in l:
                self.estado_inicial = l[0]

            for a in self.estados_aceptacion:
                if a in l:
                    newEstadosFinal.append(l[0])
                    break
        self.estados_aceptacion = newEstadosFinal

        nuevasTransiciones = []
        for transicion in self.transiciones:
            for i in self.last_particion:
                A, s, B = [*transicion]
                nuevoA = ''
                if A not in i:
                    continue

                if A in i:
                    nuevoA = i[0]
                else:
                    nuevoA = A

                nuevasTransiciones.append((nuevoA, s, B))
                break

        self.transiciones = nuevasTransiciones
        nuevasTransiciones = []

        for transicion in self.transiciones:
            for i in self.last_particion:
                A, s, B = [*transicion]
                nuevoB = ''
                if B not in i:
                    continue

                if B in i:
                    nuevoB = i[0]
                else:
                    nuevoB = B

                nuevasTransiciones.append((A, s, nuevoB))
                break
        self.transiciones = nuevasTransiciones
        resultado = {t for t in self.transiciones}
        self.transiciones = [r for r in resultado]

    # Creacion de las particiones generadas en el algoritmo.
    def CreateMorePartitions(self, partitions, more):
        newPartition = []

        for i in range(len(partitions)):
            original = utilities.Diff(partitions[i], more[i])
            if len(more[i]) > 0:
                newPartition.append(more[i])
            newPartition.append(original)
        return newPartition

    # Obtener el numero de grupo al que pertenece un estado.
    def GetGroup(self, particion, state):
        pos = 0
        for p in particion:
            if state in p:
                return pos
            pos +=1

    # Obtiene el movimiento dado un estado y el simbolo.
    def GetMove(self, estado, simbolo):
        for t in self.transiciones:
            if estado == t[0] and simbolo == t[1]:
                return t[2]

        return None

class DFA_Node():
    def __init__(self, name, nodos, isDirect = False):
        self.name = name
        self.id = None
        self.conjunto_nodos = nodos
        self.transitions = []
        self.isMarked = False
        self.isFinal = False

        if not isDirect:
            self.CreateID(nodos)
        else:
            self.CreateID2(nodos)

    # Metodo para crear un ID unico para el nodo.
    def CreateID(self, nodos):
        a = [n.id for n in nodos]
        a.sort()
        a = [str(i) for i in a]
        self.id = ', '.join(a)

    # Metodo para crear ID unico para hoja de arbol sintactico.
    def CreateID2(self, nodos):
        a = [n for n in nodos]
        a.sort()
        a = [str(i) for i in a]
        self.id = ', '.join(a)

    # Metodo para marcar un estado que ya ha sido visitado.
    def Mark(self):
        self.isMarked = True

    # Metodo para definir un estado como de aceptacion.
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

    # Simulacion de una cadena en la expresion regular.
    def Simulate_DFA(self, exp):
        S = self.estado_inicial.name

        for e in exp:
            S = self.MoveSimulation(S, e)

            if S == None:
                return 'no'

        if S in self.estados_aceptacion:
            return 'yes'
            
        return 'no'

    # Obtene la funcion de transicion del grafo generado.
    def CreateTransitionFunction(self):
        f = {}
        for t in self.transiciones:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    # Obtiene el listado de nodos del grafo.
    def GetStates(self):
        return {s.name for s in self.estados}

    # Obtiene el listado de nodos de aceptacion.
    def GetAcceptingStates(self):
        return {s for s in self.estados_aceptacion}

    # Implementacion de algoritmo para generar AFD.
    def CreateDFA(self, inicial, final):
        initial_state_DFA = self.e_closure([inicial])

        self.estado_inicial = DFA_Node(self.GetName(), initial_state_DFA)
        self.estados.append(self.estado_inicial)

        if final.id in [c.id for c in initial_state_DFA]:
            self.estado_inicial.isAcceptingState()
            self.estados_aceptacion.append(self.estado_inicial.name)

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
                            
    # Obtiene un nombre unico para el nodo.
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

    # Obtiene, si existe, un nodo que no esta marcado todavia.
    def GetFirstUnmarkedState(self):
        for n in self.estados:
            if not n.isMarked:
                return n
        
    # Metodo para verificar si existe algun nodo desmarcado.
    def MarkedState(self):
        marks = [n.isMarked for n in self.estados]
        return functools.reduce(lambda a, b: a and b, marks)

    # Verifica si un estado esta dentro de un conjunto de estados.
    def CheckArrayStates(self, states, n):
        return str(n.id) in [str(s.id) for s in states]

    # Implementacion de cerradura epsilon.
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

    # Implementacion de funcion Move dado un conjunto de estados y un simbolo.
    def Move(self, T, symbol):
        moves = []
        for t in T:
            for transition in t.transitions:
                s, state = [*transition]
                if symbol == s:
                    moves.append(state)
        return moves

    # Implementacion de funcion Move para usarlo en simulacion.
    def MoveSimulation(self, Nodo, symbol):
        move = None
        for i in self.transiciones:
            if i[0] == Nodo and i[1] == symbol:
                move = i[2]

        return move

class Node():
    def __init__(self, codigo, transitions = []):
        self.id = codigo
        self.transitions = transitions

    # Obtiene la informacion del nodo.
    def toString(self):
        return (f'Nodo: {self.id} --- {self.VerTransisiones()}')

    # Agrega una transicion al nodo.
    def AddTransition(self, simbolo, estado):
        self.transitions.append((simbolo, estado))

    # Obtiene todas las transiciones del nodo.
    def VerTransisiones(self):
        sTransicion = ''
        for t in self.transitions:
            sTransicion += f'\n\t{self.id} --> "{t[0]}" --> {t[1].id}'

        return sTransicion

class AFN():
    def __init__(self, expresion_regular):
        self.estado_inicial = None
        self.estado_final = None
        self.estados = []
        self.simbolos = []
        self.ids = 0

        expresion_regular = self.CleanExpression(expresion_regular)
        expresion_regular = self.CreateConcat(expresion_regular)
        print('EXPRESION FIXED:', expresion_regular)
        self.Evaluar(expresion_regular)

    # Simulacion de grafo AFN.
    def Simulate_NFA(self, exp):
        S = self.e_closure([self.estado_inicial])

        for e in exp:
            S = self.e_closure(self.Move(S, e))

        if str(self.estado_final.id) in [str(s.id) for s in S]:
            return 'yes'
        else:
            return 'no'

    # Verifica que un nodo se encuentre en un conjunto de estados.
    def CheckArrayStates(self, states, n):
        return str(n.id) in [str(s.id) for s in states]

    # Implementacion de cerradura epsilon
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

    # Implementacion de Move dado un conjunto de estados y simbolo
    def Move(self, T, symbol):
        moves = []
        for t in T:
            for transition in t.transitions:
                s, state = [*transition]
                if symbol == s:
                    moves.append(state)

        return moves

    # Obtiene todo los estados del AFN
    def GetStates(self):
        return {str(s.id) for s in self.estados}

    # Creacion de la funcion de transicion
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

    # Agrega las operaciones concatenacion.
    def CreateConcat(self, expresion):
        new = ''
        operators = ['*','|','(','?','+']
        cont = 0
        while cont < len(expresion):
            if cont+1 >= len(expresion):
                new += expresion[-1]
                break

            if expresion[cont] == '*' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
                new += expresion[cont]+'.'
            elif expresion[cont] == '*' and expresion[cont+1] == '(':
                new += expresion[cont]+'.'
            elif expresion[cont] == '?' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
                new += expresion[cont]+'.'
            elif expresion[cont] == '?' and expresion[cont+1] == '(':
                new += expresion[cont]+'.'
            elif not (expresion[cont] in operators) and expresion[cont+1] == ')':
                new += expresion[cont]
            elif (not (expresion[cont] in operators) and not (expresion[cont+1] in operators)) or (not (expresion[cont] in operators) and (expresion[cont+1] == '(')):
                new += expresion[cont]+'.'
            else:
                new += expresion[cont]
        
            cont += 1
        return new

    # Transformacion de la expresion regular a una que entienda el programa
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

                if regular[i] == ')' and i < len(regular) - 1:
                    real.append(regular[i])
                    if regular[i + 1] == '+':
                        final = i + 1
                        real.append('*')
                        # real.append('.')
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

                regular_copy = regular_copy.replace(symbol + '+', '(' + symbol + '*' + symbol + ')')

        if '?' in regular_copy:
            while '?' in regular_copy:
                i = regular_copy.find('?')
                symbol = regular_copy[i - 1]

                regular_copy = regular_copy.replace(symbol + '?', '(' + symbol + '|' + epsilon + ')')

        if regular_copy.count('(') > regular_copy.count(')'):
            for i in range(regular_copy.count('(') - regular_copy.count(')')):
                regular_copy += ')'
                print(regular_copy)

        elif regular_copy.count('(') < regular_copy.count(')'):
            for i in range(regular_copy.count(')') - regular_copy.count('(')):
                regular_copy = '(' + regular_copy

        return regular_copy

    # Metodo para unir dos nodos que son iguales.
    def MergeNodes(self, nodeA, nodeB):
        # Quitar de estados
        nodeA.transitions += nodeB.transitions
        i = self.estados.index(nodeB)
        self.estados.pop(i)

    # Creacion de nodos de operacion |
    def CreateORNodes(self, a, b):
        if type(a) == tuple and type(b) == tuple:
            a_inicial, a_final = [*a]
            b_inicial, b_final = [*b]

            # Nodo final de OR
            nodoF = Node(self.ids + 2, [])

            # Nodo inicial de OR
            nodoI = Node(self.ids + 1, [(epsilon, a_inicial), (epsilon, b_inicial)])

            a_final.AddTransition(epsilon, nodoF)
            b_final.AddTransition(epsilon, nodoF)

            self.ids += 2

            # Estados
            self.estados.append(nodoF)
            self.estados.append(nodoI)

            return nodoI, nodoF
            
        elif type(a) != tuple and type(b) != tuple:
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

            return nodoI, nodoF
        elif type(a) != tuple and type(b) == tuple:
            b_inicial, b_final = [*b]

            nodoF = Node(self.ids + 4, [])

            nodoFinalA = Node(self.ids + 3, [(epsilon, nodoF)])
            nodoInicialA = Node(self.ids + 2, [(a, nodoFinalA)])

            nodoI = Node(self.ids + 1, [(epsilon, b_inicial), (epsilon, nodoInicialA)])
            b_final.AddTransition(epsilon, nodoF)

            self.ids += 4

            # Estados
            self.estados.append(nodoF)
            self.estados.append(nodoFinalA)
            self.estados.append(nodoInicialA)
            self.estados.append(nodoI)

            return nodoI, nodoF
        elif type(a) == tuple and type(b) != tuple:
            a_inicial, a_final = [*a]
            nodoF = Node(self.ids + 4, [])

            nodoFinalB = Node(self.ids + 3, [(epsilon, nodoF)])
            nodoInicialB = Node(self.ids + 2, [(b, nodoFinalB)])

            nodoI = Node(self.ids + 1, [(epsilon, a_inicial), (epsilon, nodoInicialB)])
            a_final.AddTransition(epsilon, nodoF)

            self.ids += 4

            # Estados
            self.estados.append(nodoF)
            self.estados.append(nodoFinalB)
            self.estados.append(nodoInicialB)
            self.estados.append(nodoI)
            return nodoI, nodoF  

    # Creacion de nodos por operacion de concatenacion
    def CreateCATNodes(self, a, b):
        if type(a) == tuple and type(b) == tuple:
            a_inicial, a_final = [*a]
            b_inicial, b_final = [*b]

            self.MergeNodes(a_final, b_inicial)
            return a_inicial, b_final
        elif type(a) != tuple and type(b) != tuple:
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

            return node1, node3
        elif type(a) != tuple and type(b) == tuple:
            b_inicial, b_final = [*b]

            nodoI = Node(self.ids + 1, [(a, b_inicial)])
            self.estados.append(nodoI)
            self.ids += 1

            return nodoI, b_final
        elif type(a) == tuple and type(b) != tuple:
            a_inicial, a_final = [*a]

            nodoF = Node(self.ids + 1, [])
            self.estados.append(nodoF)
            a_final.AddTransition(b, nodoF)
            self.ids += 1
            
            return a_inicial, nodoF

    # Creacion de nodos por operacion de cerradura kleene
    def CreateSTARNodes(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if type(a) == tuple:
            a_inicial, a_final = [*a]
            
            # Nodo final de *
            node4 = Node(self.ids + 2, [])

            # Nodo inicial de *
            node1 = Node(self.ids + 1, [(epsilon, a_inicial), (epsilon, node4)])

            a_final.AddTransition(epsilon, node4)
            a_final.AddTransition(epsilon, a_inicial)
            self.ids += 2

            self.estados.append(node1)
            self.estados.append(node4)
            return node1, node4
        else:
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
            return node1, node4

    # Obtiene la precedencia de operadores
    def ObtenerPrecedencia(self, operator):
        if operator == '|':
            return 1
        if operator == '.':
            return 2
        if operator == '*' or operator == '+' or operator == '?':
            return 3
        return 0

    # Realiza la operacion entre los operandos dado un operador
    def Operar(self, x, y, operator):
        if operator == '|': return self.CreateORNodes(x, y)
        if operator == '.': return self.CreateCATNodes(x, y)
        if operator == '*': return self.CreateSTARNodes(y)

    # Determina si el token es un simbolo
    def EsSimbolo(self, digit):
        digitos = 'abcdefghijklmnopqrstuvwxyz0123456789' + epsilon
        if digit in digitos:
            return True
        return False

    # Evaluacion de la expresion regular.
    def Evaluar(self, expresion):
        simbolos = []
        operaciones = []
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
                    
                    inicio, fin = self.Operar(val1, val2, op)
                    simbolos.append((inicio, fin))

                operaciones.pop()

            else:
                while (len(operaciones) != 0
                    and self.ObtenerPrecedencia(operaciones[-1]) >= self.ObtenerPrecedencia(expresion[i])):
                    op = operaciones.pop()
                    val2 = simbolos.pop()
                    val1 = None

                    if op != '*' and op != '+' and op != '?':
                        val1 = simbolos.pop()
                    
                    inicio, fin = self.Operar(val1, val2, op)
                    simbolos.append((inicio, fin))
                operaciones.append(expresion[i])

            i += 1

        while len(operaciones) != 0:
            op = operaciones.pop()
            val2 = simbolos.pop()
            val1 = None

            if op != '*' and op != '+' and op != '?':
                val1 = simbolos.pop()
            
            inicio, fin = self.Operar(val1, val2, op)
            simbolos.append((inicio, fin))
        
        self.estado_inicial, self.estado_final = simbolos.pop()

class SyntaxTree():
    def __init__(self, regular_expression):
        self.count = 0
        self.rounds = 1
        self.estados = []

        self.simbolos = []
        self.transiciones = []
        self.estados_aceptacion = []
        self.estado_inicial = None
        
        self.nodos = []
        self.root = None
        self.id = 0
        self.primera_vez = True
        self.estado_final = None

        self.follow_pos = {}
        regular_expression = self.CleanExpression(regular_expression)
        regular_expression = self.CreateConcat(regular_expression)
        print('EXPRESION FIXED:', regular_expression)
        self.evaluate(regular_expression)

        for n in self.nodos:
            if n.name == '#':
                self.estado_final = n.position
                break

        self.calculate_followpow()
        print(self.follow_pos)
        self.create_dfa()

    # Simulacion de AFD
    def Simulate_DFA(self, exp):
        S = self.estado_inicial

        for e in exp:
            S = self.MoveSimulation(S, e)

            if S == None:
                return 'no'

        if S in self.estados_aceptacion:
            return 'yes'
            
        return 'no'
        
    # Implementacion de Move para la simulacion
    def MoveSimulation(self, Nodo, symbol):
        move = None
        for i in self.transiciones:
            if i[0] == Nodo and i[1] == symbol:
                move = i[2]

        return move
    
    # Agrega los operadores concatenacion
    def CreateConcat(self, expresion):
        new = ''
        operators = ['*','|','(','?','+']
        cont = 0
        while cont < len(expresion):
            if cont+1 >= len(expresion):
                new += expresion[-1]
                break

            if expresion[cont] == '*' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
                new += expresion[cont]+'.'
            elif expresion[cont] == '*' and expresion[cont+1] == '(':
                new += expresion[cont]+'.'
            elif expresion[cont] == '?' and not (expresion[cont+1] in operators) and expresion[cont+1] != ')':
                new += expresion[cont]+'.'
            elif expresion[cont] == '?' and expresion[cont+1] == '(':
                new += expresion[cont]+'.'
            elif not (expresion[cont] in operators) and expresion[cont+1] == ')':
                new += expresion[cont]
            elif (not (expresion[cont] in operators) and not (expresion[cont+1] in operators)) or (not (expresion[cont] in operators) and (expresion[cont+1] == '(')):
                new += expresion[cont]+'.'
            else:
                new += expresion[cont]
        
            cont += 1
        return new

    # Crea las transiciones del grafo
    def create_transitions(self):
        f = {}
        for t in self.transiciones:
            i, s, fi = [*t]

            if i not in f.keys():
                f[i] = {}
            f[i][s] = fi

        return f

    # Genera los nodos y transiciones para el AFD
    def create_dfa(self):
        s0 = self.root.first_pos
        print(s0)
        s0_dfa = DFA_Node(self.get_name(), s0, True)
        self.estados.append(s0_dfa)
        self.estado_inicial = s0_dfa.name

        if self.estado_final in [u for u in s0_dfa.conjunto_nodos]:
            self.estados_aceptacion.append(s0_dfa.name)

        while not self.marked_state():
            T = self.get_unmarked_state()
            
            T.Mark()

            for s in self.simbolos:
                fp = []
                
                for u in T.conjunto_nodos:
                    if self.get_leaf(u).name == s:
                        fp += self.follow_pos[u]
                fp = {a for a in fp}
                fp = [a for a in fp]
                if len(fp) == 0:
                    continue

                U = DFA_Node(self.get_name(), fp, True)

                if U.id not in [n.id for n in self.estados]:
                    print(fp)
                    if self.estado_final in [u for u in U.conjunto_nodos]:
                        self.estados_aceptacion.append(U.name)
                    
                    self.estados.append(U)
                    print((T.conjunto_nodos, s, U.conjunto_nodos))
                    self.transiciones.append((T.name, s, U.name))
                else:
                    self.count -= 1
                    for estado in self.estados:
                        if U.id == estado.id:
                            self.transiciones.append((T.name, s, estado.name))
                            print((T.conjunto_nodos, s, estado.conjunto_nodos))

    # Obtiene la hoja a traves de su nombre
    def get_leaf(self, name):
        for n in self.nodos:
            if n.position == name:
                return n

    # Obtiene el estado unmarked
    def get_unmarked_state(self):
        for n in self.estados:
            if not n.isMarked:
                return n

    # Obtiene el nombre para asignarlo al nodo
    def get_name(self):
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

    # Se realiza el calculo de followpos
    def calculate_followpow(self):
        for n in self.nodos:
            if not n.is_operator and not n.nullable:
                self.add_followpos(n.position, [])

        for n in self.nodos:
            if n.name == '.':
                c1, c2 = [*n.children]

                for i in c1.last_pos:
                    self.add_followpos(i, c2.first_pos)

            elif n.name == '*':
                for i in n.last_pos:
                    self.add_followpos(i, n.first_pos)                

    # Revisa si existe algun estado desmarcado
    def marked_state(self):
        marks = [n.isMarked for n in self.estados]
        return functools.reduce(lambda a, b: a and b, marks)

    # Agrega un followpos
    def add_followpos(self, pos, val):
        if pos not in self.follow_pos.keys():
            self.follow_pos[pos] = []

        self.follow_pos[pos] += val
        self.follow_pos[pos] = {i for i in self.follow_pos[pos]}
        self.follow_pos[pos] = [i for i in self.follow_pos[pos]]

    # Convierte la expresion a una que pueda leer el programa
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

                if regular[i] == ')' and i < len(regular) - 1:
                    real.append(regular[i])
                    if regular[i + 1] == '+':
                        final = i + 1
                        real.append('*')
                        # real.append('.')
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

                regular_copy = regular_copy.replace(symbol + '+', '(' + symbol + '*' + symbol + ')')

        if '?' in regular_copy:
            while '?' in regular_copy:
                i = regular_copy.find('?')
                symbol = regular_copy[i - 1]

                regular_copy = regular_copy.replace(symbol + '?', '(' + symbol + '|' + epsilon + ')')

        if regular_copy.count('(') > regular_copy.count(')'):
            for i in range(regular_copy.count('(') - regular_copy.count(')')):
                regular_copy += ')'

        elif regular_copy.count('(') < regular_copy.count(')'):
            for i in range(regular_copy.count(')') - regular_copy.count('(')):
                regular_copy = '(' + regular_copy

        regular_copy = '(' + regular_copy + ')#'
        return regular_copy

    # Obtiene el ultimo elemento guardado en el stack
    def peek(self, stack):
        return stack[-1] if stack else None

    # Determina si el token es un simbolo
    def is_symbol(self, s):
        digitos = 'abcdefghijklmnopqrstuvwxyz0123456789#' + epsilon
        if s in digitos:
            return True
        return False

    # Obtiene el ID del nodo
    def get_id(self):
        self.id += 1
        return self.id

    # Implementacion de la creacion del arbol sintactico
    def apply_operator(self, operators, values):
        operator = operators.pop()
        right = values.pop()
        left = '@'

        if right not in self.simbolos and right != epsilon and right != '@' and right != '#':
            self.simbolos.append(right)

        if operator != '*' and operator != '+' and operator != '?':
            left = values.pop()

            if left not in self.simbolos and left != epsilon and left != '@' and left != '#':
                self.simbolos.append(left)

        if operator == '|': return self.operator_or(left, right)
        elif operator == '.': return self.operator_concat(left, right)
        elif operator == '*': return self.operator_kleene(right)

    # Operacion kleen
    def operator_kleene(self, leaf):
        operator = '*'
        if isinstance(leaf, Leaf):
            root = Leaf(operator, None, True, [leaf], True)
            self.nodos += [root]
            return root

        else:
            id_left = None
            if leaf != epsilon:
                id_left = self.get_id()

            left_leaf = Leaf(leaf, id_left, False, [], False)
            root = Leaf(operator, None, True, [left_leaf], True)
            self.nodos += [left_leaf, root]

            return root

    # Operacion OR
    def operator_or(self, left, right):
        operator = '|'
        if isinstance(left, Leaf) and isinstance(right, Leaf):
            root = Leaf(operator, None, True, [left, right], left.nullable or right.nullable)
            self.nodos += [root]
            return root

        elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_left = None
            id_right = None
            if left != epsilon:
                id_left = self.get_id()
            if right != epsilon:
                id_right = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [left_leaf, right_leaf], left_leaf.nullable or right_leaf.nullable)

            self.nodos += [left_leaf, right_leaf, root]

            return root

        elif isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_right = None
            if right != epsilon:
                id_right = self.get_id()
            
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [left, right_leaf], left.nullable or right_leaf.nullable)

            self.nodos += [right_leaf, root]
            return root

        elif not isinstance(left, Leaf) and isinstance(right, Leaf):
            id_left = None
            if left != epsilon:
                id_left = self.get_id()
            
            left_leaf = Leaf(left, id_left, False, [], False)
            root = Leaf(operator, None, True, [left_leaf, right], left_leaf.nullable or right.nullable)

            self.nodos += [left_leaf, root]
            return root

    # Operacion concatenacion
    def operator_concat(self, left, right):
        operator = '.'
        if isinstance(left, Leaf) and isinstance(right, Leaf):
            root = Leaf(operator, None, True, [left, right], left.nullable and right.nullable)
            self.nodos += [root]
            return root

        elif not isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_left = None
            id_right = None
            if left != epsilon:
                id_left = self.get_id()
            if right != epsilon:
                id_right = self.get_id()

            left_leaf = Leaf(left, id_left, False, [], False)
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [left_leaf, right_leaf], left_leaf.nullable and right_leaf.nullable)

            self.nodos += [left_leaf, right_leaf, root]
            return root

        elif isinstance(left, Leaf) and not isinstance(right, Leaf):
            id_right = None
            if right != epsilon:
                id_right = self.get_id()
            
            right_leaf = Leaf(right, id_right, False, [], False)
            root = Leaf(operator, None, True, [left, right_leaf], left.nullable and right_leaf.nullable)

            self.nodos += [right_leaf, root]
            return root
        
        elif not isinstance(left, Leaf) and isinstance(right, Leaf):
            id_left = None
            if left != epsilon:
                id_left = self.get_id()
            
            left_leaf = Leaf(left, id_left, False, [], False)
            root = Leaf(operator, None, True, [left_leaf, right], left_leaf.nullable and right.nullable)

            self.nodos += [left_leaf, root]
            return root

    # Obtiene la precedencia entre dos operadores
    def greater_precedence(self, op1, op2):
        precedences = {'|' : 0, '.' : 1, '*' : 2}
        return precedences[op1] >= precedences[op2]
    
    # Implementacion de la creacion del arbol sintactico
    def evaluate(self, expression):
        values = []
        operators = []
        for token in expression:
            if self.is_symbol(token):
                values.append(token)

            elif token == '(':
                operators.append(token)

            elif token == ')':
                top = self.peek(operators)

                while top is not None and top != '(':
                    raiz = self.apply_operator(operators, values)
                    values.append(raiz)
                    top = self.peek(operators)
                operators.pop()

            else:
                top = self.peek(operators)

                while top is not None and top not in '()' and self.greater_precedence(top, token):
                    raiz = self.apply_operator(operators, values)
                    values.append(raiz)
                    top = self.peek(operators)
                operators.append(token)

        while self.peek(operators) is not None:
            raiz = self.apply_operator(operators, values)
            values.append(raiz)
        self.root = values.pop()
            
class Leaf():
    def __init__(self, name, position, is_operator, children, nullable):
        self.name = name
        self.position = position
        self.is_operator = is_operator
        self.children = children
        self.nullable = nullable

        self.first_pos = []
        self.last_pos = []
        self.follow_pos = []

        if self.name == epsilon:
            self.nullable = True

        self.AddFirstPos()
        self.AddLastPos()

    # Obtiene el nombre de la hoja
    def GetName(self):
        return f'{self.name} - {self.position}'

    # Agrega el firstpos de la hoja
    def AddFirstPos(self):
        if self.is_operator:
            if self.name == '|':
                self.first_pos = self.children[0].first_pos + self.children[1].first_pos
            elif self.name == '.':
                if self.children[0].nullable:
                    self.first_pos = self.children[0].first_pos + self.children[1].first_pos
                else:
                    self.first_pos += self.children[0].first_pos
            elif self.name == '*':
                self.first_pos += self.children[0].first_pos
        else:
            if self.name != epsilon:
                self.first_pos.append(self.position)

    # Agrega el lastpos de la hoja
    def AddLastPos(self):
        if self.is_operator:
            if self.name == '|':
                self.last_pos = self.children[0].last_pos + self.children[1].last_pos
            elif self.name == '.':
                if self.children[1].nullable:
                    self.last_pos = self.children[0].last_pos + self.children[1].last_pos
                else:
                    self.last_pos += self.children[1].last_pos
            elif self.name == '*':
                self.last_pos += self.children[0].last_pos
        else:
            if self.name != epsilon:
                self.last_pos.append(self.position)



exp = input('Ingrese expresion regular: ')
w = input('Ingrese una cadena: ')
print('\n')

# ------------------------- METODO DIRECTO ---------------------------------------------

try:
    print('\n-- AFD DIRECTO --')
    syntax = SyntaxTree(exp)

    states = {s.name for s in syntax.estados}
    initial_state = syntax.estado_inicial
    accepting_state = {s for s in syntax.estados_aceptacion}
    alphabet = {a for a in syntax.simbolos}
    transition_function = syntax.create_transitions()
    alphabet, alphabet_print = utilities.getAlphabet(transition_function)

    start = perf_counter()
    resultado = syntax.Simulate_DFA(w)
    total = (perf_counter() - start)

    print(f'¿{w} cumple con {exp}?', resultado)
    print(' -- %.8f seconds --' % total)
    utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'grafos/DIRECT_AFD')

    syntax_file = f'''
    EXPRESION: {exp}
    ESTADOS = {states}
    SIMBOLOS = {alphabet_print}
    INICIO = {initial_state}
    ACEPTACION = {accepting_state}
    TRANSICION = {utilities.GetTransitions(transition_function)}
    '''

    utilities.write_file(syntax_file, 'RESULTADO_DIRECT_DFA.txt')
except:
    print('HA OCURRIDO UN ERROR CON METODO DIRECTO.')

# ------------------------- MINIMIZACION METODO DIRECTO ---------------------------------------------

try:
    minimization_directo = Minimization(syntax.transiciones, [e for e in states], [e for e in accepting_state], [s for s in alphabet_print], initial_state)
    utilities.graph_automata(
        minimization_directo.GetStates(),
        alphabet,
        minimization_directo.estado_inicial,
        {a for a in minimization_directo.estados_aceptacion},
        minimization_directo.CreateTransitionFunction(),
        'grafos/DIRECT_AFD_MINIMIZADO'
    )
except:
    print('HA OCURRIDO UN ERROR CON MINIMIZACION DE METODO DIRECTO.')

# ------------------------- METODO AFN ---------------------------------------------

try:
    print('\n-- AFN --')
    afn = AFN(exp)

    states = afn.GetStates()
    initial_state = str(afn.estado_inicial.id)
    accepting_state = {str(afn.estado_final.id)}
    transition_function = afn.CreateTransitionFunction()
    alphabet, alphabet_print = utilities.getAlphabet(transition_function)

    afn_file = f'''
    EXPRESION: {exp}
    ESTADOS = {states}
    SIMBOLOS = {alphabet_print}
    INICIO = {initial_state}
    ACEPTACION = {accepting_state}
    TRANSICION = {utilities.GetTransitions(transition_function)}
    '''
    utilities.write_file(afn_file, 'RESULTADO_AFN.txt')

    begin_time1 = perf_counter()
    respuesta = afn.Simulate_NFA(w)
    total_time1 = (perf_counter() - begin_time1)

    print(f'¿{w} cumple con {exp}?', respuesta)
    print(' -- %.8f seconds --' % total_time1)

    utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'grafos/NFA')

except:
    print('HA OCURRIDO UN ERROR CON AFN.')

# ------------------------- METODO AFD ---------------------------------------------

try:
    print('\n-- AFD --')
    dfa = DFA([s for s in alphabet_print], afn.estado_inicial, afn.estado_final)

    states = dfa.GetStates()
    initial_state = dfa.estado_inicial.name
    accepting_state = dfa.GetAcceptingStates()
    transition_function = dfa.CreateTransitionFunction()
    alphabet, alphabet_print = utilities.getAlphabet(transition_function)

    afd_file = f'''
    EXPRESION: {exp}
    ESTADOS = {states}
    SIMBOLOS = {alphabet_print}
    INICIO = {initial_state}
    ACEPTACION = {accepting_state}
    TRANSICION = {utilities.GetTransitions(transition_function)}
    '''
    utilities.write_file(afd_file, 'RESULTADO_AFD.txt')

    begin_time2 = perf_counter()
    resultado = dfa.Simulate_DFA(w)
    total_time2 = (perf_counter() - begin_time2)

    print(f'¿{w} cumple con {exp}?', resultado)
    print(' -- %.8f seconds --' % total_time2)

    utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function, 'grafos/DFA')

except:
    print('HA OCURRIDO UN ERROR CON AFD.')

# ------------------------- MINIMIZACION METODO AFD ---------------------------------------------

try:
    minimization = Minimization(dfa.transiciones, [e for e in states], [e for e in accepting_state], [s for s in alphabet_print], initial_state)
    utilities.graph_automata(
        minimization.GetStates(),
        alphabet,
        minimization.estado_inicial,
        {a for a in minimization.estados_aceptacion},
        minimization.CreateTransitionFunction(),
        'grafos/AFD_MINIMIZACION'
    )
except:
    print('HA OCURRIDO UN ERROR CON MINIMIZACION DE AFD.')