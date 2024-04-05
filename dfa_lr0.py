from collections import defaultdict
from graphviz import Digraph

"""
LR(0) DFA Constructor/Renderer
Ian S. Woodley
Written in Python 3.6
Rendering requires Graphviz:  https://pypi.python.org/pypi/graphviz
"""


class LRItem:
    """Simple container to express the relationship between a
    nonterminal (nt) and a production (prod)."""
    Dot = "•"
    Nullables = {'λ', 'LAMBDA'}

    def __init__(self, nt: str, prod: str):
        self.nt = nt
        self.prod = prod

    def __eq__(self, item: 'LRItem'):
        return self.nt == item.nt and self.prod == item.prod

    def __repr__(self):
        return "%s → %s" % (self.nt, self.prod)


class DFAState:
    """Each DFA state has a unique identifier applied upon construction.
    The LRItems passed as items are used to compute the closure of the
    state, preparing it for further construction."""

    def __init__(self, m_id: int, items: list('LRItem'), grammar: defaultdict(list)):
        self.id = m_id
        self.items = items
        self.computeClosure(grammar)

    def __eq__(self, state: 'DFAState'):
        return self.items == state.items

    def __repr__(self):
        return "\n".join(map(str, self.items))

    def computeClosure(self, grammar: defaultdict(list)):
        """Until computation stabilizes:
        1.  Iterate through this state's items.
        2.  If there is a nonterminal following the LR separator(Dot):
                Flag symbol as visited.
                Flag symbol for item addition.
        3.  If nothing left to add:
                Closure has stabilized. Exits loop.
            else
                Continue closure computation."""
        visited = set()
        while True:
            to_add = []
            for item in self.items:
                split = item.prod.split(' ')
                idx = split.index(LRItem.Dot)
                if idx != len(split) - 1:
                    symbol = split[idx + 1]
                    if symbol not in visited and symbol in grammar:
                        visited.add(symbol)
                        to_add.append(symbol)
            if not to_add:
                break
            for nt in to_add:
                for prod in grammar[nt]:
                    if prod in LRItem.Nullables:
                        self.items.append(LRItem(nt, LRItem.Dot))
                    else:
                        self.items.append(LRItem(nt, "%s %s" % (LRItem.Dot, prod)))

    def getNeighbors(self):
        """For each LRItem in state:
        1.  Check symbol after LRItem separator (if any). This will be
            the transition edge between this state and its neighbor.
        2.  Create new LRItem with the root being this item, moving the
            LRItem separator(Dot) forward one position.
        3.  Add to map: key=edge, val=list(LRItem)"""
        neighbors = defaultdict(list)
        for item in self.items:
            split = item.prod.split(' ')
            idx = split.index(LRItem.Dot)
            if idx != len(split) - 1:
                symbol = split[idx + 1]
                split[idx], split[idx + 1] = split[idx + 1], split[idx]
                neighbors[symbol].append(LRItem(item.nt, ' '.join(split)))

        return neighbors


class DFA:
    """Records DFAStates and their transitions as construction commences.
    Input grammar format (assignments separated by newlines):
        NT represents a nonterminal.
        PROD represents a production, with symbols separated by spaces.
        Method 1:
            NT -> PROD
            NT -> PROD2
        Method 2:
            NT -> PROD | PROD2
        E.g.
            S -> a B c
            B -> b B | λ
    """
    Root = 'Ͽ'

    def __init__(self, grammar: str):
        self.states = {}
        self.grammar = defaultdict(list)
        self.transitions = defaultdict(dict)
        self.state_id = 0
        root = self.formatGrammar(grammar)
        print(root)
        self.addState(root)
        self.construct(root)

    def addState(self, state: 'DFAState'):
        self.states[state.id] = state
        self.state_id += 1

    def addTransition(self, a: 'DFAState', b: 'DFAState', edge: str):
        self.transitions[a.id][b.id] = edge

    def formatGrammar(self, grammar: str):
        """Converts input grammar into map for accessibility,
        returning the root state from which construction begins."""
        root = None
        for line in map(str.strip, grammar.split('\n')):
            if line:
                nt, prod = map(str.strip, line.split('->'))
                prod = map(str.strip, prod.split('|'))
                if not self.grammar:
                    root = LRItem(DFA.Root, '%s %s' % (LRItem.Dot, nt))
                for p in prod:
                    self.grammar[nt].append(p)
        return DFAState(0, [root], self.grammar)

    def construct(self, root: 'DFAState'):
        """From root:
        1.  Iterate through neighbors.
        2.  If neighbor (N) matches an existing state:
                Flag N as an existing state.
                Add edge from root -> N.
            else
                Create new DFAState (D).
                Add edge from root -> D.
        3.  Continue construction recursively for each
            new state."""
        existing = set()
        n = root.getNeighbors()
        for edge, items in n.items():
            new_state = DFAState(self.state_id, items, self.grammar)
            for state_id in self.states:
                if self.states[state_id] == new_state:
                    existing.add(state_id)
                    new_state = self.states[state_id]
                    break
            else:
                self.addState(new_state)
            self.addTransition(root, new_state, edge)

        for state_id in self.transitions[root.id]:
            if state_id not in existing:
                self.construct(self.states[state_id])

    def render(self, filename='DFA', format='svg'):
        """Outputs constructed DFA as GV and passed format."""
        graph = Digraph('DFA', format=format)
        cvrt = lambda tup: '%s → %s\l' % (tup[0], ' | '.join(tup[1]))
        graph.node('Grammar',
                   'Grammar\n' + ''.join(map(cvrt, self.grammar.items())),
                   shape='box')

        for state_id in self.states:
            graph.node(str(state_id), '%s\n%s\l' % (state_id, self.states[state_id]))
        for a in self.transitions:
            for b in self.transitions[a]:
                edge = self.transitions[a][b]
                graph.edge(str(a), str(b), label=edge)
        graph.render('D:\study\pythonProject\编译原理\DFA.gv')

DFA('S -> a S | b S | c').render()