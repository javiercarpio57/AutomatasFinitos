import functools 
import utilities

epsilon = 'ε'

class AFN:
    def __init__(self, expresion_regular):
        self.estado_inicial = None
        self.estado_final = None
        self.estados = []
        self.funcion_transicion = {}
        self.simbolos = []
        self.ids = 0

        self.Evaluar(expresion_regular)

    def e_closure(self, state):
        eclosure = [state.id]
        primeraVez = True
        newStates = []

        while not newStates or primeraVez:
            if primeraVez:
                primeraVez = False
            
            print('a')

        return eclosure

    def AgregarTransicion(self, estado_i, trans, estado_f):
        if (estado_i, trans) in self.funcion_transicion.keys():
            self.funcion_transicion[(estado_i, trans)].append(estado_f)
        else:
            self.funcion_transicion[(estado_i, trans)] = [estado_f]

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

            # Funcion de transicion
            self.AgregarTransicion(nodoI.id, epsilon, nodoInicialA.id)
            self.AgregarTransicion(nodoI.id, epsilon, nodoInicialB.id)
            self.AgregarTransicion(nodoInicialA.id, a, nodoFinalA.id)
            self.AgregarTransicion(nodoInicialB.id, b, nodoFinalB.id)
            self.AgregarTransicion(nodoFinalA.id, epsilon, nodoF.id)
            self.AgregarTransicion(nodoFinalB.id, epsilon, nodoF.id)

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

                # Funcion de transicion
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicialA.id)
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicialB.id)
                self.AgregarTransicion(nodoInicialA.id, a, nodoFinalA.id)
                self.AgregarTransicion(nodoInicialB.id, b, nodoFinalB.id)
                self.AgregarTransicion(nodoFinalA.id, epsilon, nodoF.id)
                self.AgregarTransicion(nodoFinalB.id, epsilon, nodoF.id)

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

                # Funcion de transicion
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicial.id)
                self.AgregarTransicion(nodoI.id, epsilon, nodoIB.id)
                self.AgregarTransicion(nodoFA.id, epsilon, nodoF.id)
                self.AgregarTransicion(nodoFinal.id, epsilon, nodoF.id)

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

                # Funcion de transicion
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicial.id)
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicialB.id)
                self.AgregarTransicion(nodoInicialB.id, b, nodoFinalB.id)
                self.AgregarTransicion(nodoFinal.id, epsilon, nodoF.id)
                self.AgregarTransicion(nodoFinalB.id, epsilon, nodoF.id)

                return nodoI, nodoFA, nodoI, nodoF
                
            elif a != None and b == None:
                nodoF = Node(self.ids + 4, [])

                nodoFinalA = Node(self.ids + 3, [(epsilon, nodoF)])
                nodoInicialA = Node(self.ids + 2, [(a, nodoFinalA)])

                nodoI = Node(self.ids + 1, [(epsilon, nodoInicial), (epsilon, nodoInicialA)])
                nodoFinal.AddTransition(epsilon, nodoF)

                self.ids += 4

                # Estados
                self.estados.append(nodoF)
                self.estados.append(nodoFinalA)
                self.estados.append(nodoInicialA)
                self.estados.append(nodoI)

                # Funcion de transicion
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicial.id)
                self.AgregarTransicion(nodoI.id, epsilon, nodoInicialA.id)
                self.AgregarTransicion(nodoInicialA.id, a, nodoFinalA.id)
                self.AgregarTransicion(nodoFinal.id, epsilon, nodoF.id)
                self.AgregarTransicion(nodoFinalA.id, epsilon, nodoF.id)

                return nodoI, nodoI, nodoIB, nodoF

    def CreateCATNodes(self, a, b, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFinal = None):
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

            self.AgregarTransicion(node1, a, node2)
            self.AgregarTransicion(node2, b, node3)

            return node1, node3
        else:
            if a != None and b != None:
                nodoProvisionalB = Node(self.ids + 2, [])
                nodoProvisionalA = Node(self.ids + 1, [(b, nodoProvisionalB)])
                
                self.estados.append(nodoProvisionalA)
                self.estados.append(nodoProvisionalB)

                nodoFinal.AddTransition(a, nodoProvisionalA)
                self.AgregarTransicion(nodoFinal, a, nodoProvisionalA)
                self.AgregarTransicion(nodoProvisionalA, b, nodoProvisionalB)

                return nodoInicial, nodoProvisionalB
            # elif a == None and b == None:

            elif a != None:
                nodoProvisional = Node(self.ids + 1, [(a, nodoInicial)])
                self.estados.append(nodoProvisional)
                self.AgregarTransicion(nodoProvisional, a, nodoInicial)
                self.ids += 1

                return nodoProvisional, nodoFinal
            elif b != None:
                nodoProvisional = Node(self.ids + 1, [])
                self.estados.append(nodoProvisional)
                self.AgregarTransicion(nodoFinal, b, nodoProvisional)
                nodoFinal.AddTransition(b, nodoProvisional)
                self.ids += 1

                return nodoInicial, nodoProvisional

    def CreateSTARNodes(self, a, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFinal = None):
        if not haGeneradoPrimerGrafo:
            # Nodo final de CAT
            node4 = Node(self.ids + 4, [])

            # Nodo en medio final de CAT
            node3 = Node(self.ids + 3, [(epsilon, node4)])

            # Nodo en medio inicial de CAT
            node2 = Node(self.ids + 2, [(a, node3)])

            # Nodo inicial de CAT
            node1 = Node(self.ids + 1, [(epsilon, node2), (epsilon, node4)])

            node4.AddTransition(epsilon, node2)
            self.ids += 4

            self.estados.append(node1)
            self.estados.append(node2)
            self.estados.append(node3)
            self.estados.append(node4)

            self.AgregarTransicion(node1, epsilon, node2)
            self.AgregarTransicion(node1, epsilon, node4)
            self.AgregarTransicion(node2, a, node3)
            self.AgregarTransicion(node3, epsilon, node4)
            self.AgregarTransicion(node4, epsilon, node2)

            return node1, node4
        else:
            # Nodo final de CAT
            node4 = Node(self.ids + 2, [(epsilon, nodoInicial)])

            # Nodo inicial de CAT
            node1 = Node(self.ids + 1, [(epsilon, nodoInicial), (epsilon, node4)])

            nodoFinal.AddTransition(epsilon, node4)
            self.ids += 2

            self.estados.append(node1)
            self.estados.append(node4)

            self.AgregarTransicion(node1, epsilon, nodoInicial)
            self.AgregarTransicion(node1, epsilon, node4)
            self.AgregarTransicion(nodoFinal, epsilon, node4)
            self.AgregarTransicion(node4, epsilon, nodoInicial)

            return node1, node4

    def ObtenerPrecedencia(self, operator):
        if operator == '|':
            return 1
        if operator == '.':
            return 2
        if operator == '*':
            return 3
        return 0

    def Operar(self, x, y, operator, haGeneradoPrimerGrafo = False, nodoInicial = None, nodoFA = None, nodoIB = None, nodoFinal = None):
        if operator == '|': return self.CreateORNodes(x, y, haGeneradoPrimerGrafo, nodoInicial, nodoFA, nodoIB, nodoFinal)
        if operator == '.': return self.CreateCATNodes(x, y, haGeneradoPrimerGrafo, nodoInicial, nodoFinal)
        if operator == '*': return self.CreateSTARNodes(y, haGeneradoPrimerGrafo, nodoInicial, nodoFinal)

    def EsSimbolo(self, digit):
        digitos = 'abcdefghijklmnopqrstuvwxyz'
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

                    if op != '*':
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

                    if op != '*':
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

            if op != '*':
                val1 = simbolos.pop()
            
            self.estado_inicial, intermedioA, intermedioB, self.estado_final = self.Operar(val1, val2, op, haGeneradoPrimerGrafo, self.estado_inicial, intermedioA, intermedioB, self.estado_final)

            simbolos.append(None)

            if not haGeneradoPrimerGrafo:
                haGeneradoPrimerGrafo = True

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



exp = input('Ingrese expresion regular: ')

afn = AFN(exp)

for n in afn.estados:
    print(n.toString())

print('------------------------------')

for keys, values in afn.funcion_transicion.items():
    print(f'({keys[0]}, {keys[1]}): {list(map(lambda nodo: nodo, values))}')

# utilities.graph_automata()
states = utilities.getStates(afn.estados)
initial_state = str(afn.estado_inicial.id)
accepting_state = {str(afn.estado_final.id)}
transition_function = utilities.getTransitionFunction(afn.funcion_transicion)
alphabet = utilities.getAlphabet(transition_function)

utilities.graph_automata(states, alphabet, initial_state, accepting_state, transition_function)
