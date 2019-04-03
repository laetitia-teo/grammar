import numpy as np
from tree import BNode, UNode

class CFG():
    """
    Context-Free Grammar.
    
    Args :
        - variables : the list of all variables in the grammar, e.g. non-terminal
        symbols;
        - rules (list of str): list of production rules for the grammar, of the 
        form:
            "s -> np, vp";  --for non-terminal production rules
            "n -> dog"      --for terminal production rules
        - S : starting symbol, at the root of the sentence tree.
    """
    def __init__(self, variables, rules, S):
        # non terminal symbols
        self.variables = variables
        # production rules
        self.rules = {}
        self._parse_rules(rules)
        # terminal symbols
        self.terminals = []
        self._init_terminals()
        # start symbol
        self.S = S
        # symbols leading to terminal symbols
        self.unit_symbols = {}
        self._init_unit_productions()
        # separate dict of non-terminal rules
        self.nt_rules = {}
        self._init_non_terminal_rules()
    
    def _parse_rules(self, rules):
        """
        Parse the rules, given as a list of productions in string form, into
        a rule dict.
        """
        for rule in rules:
            rule = rule.replace(',', '')
            items = rule.split(' ')
            symbols = []
            prod = False
            for s in items:
                if prod:
                    symbols.append(s)
                if s == '->':
                    prod = True
            try:
                self.rules[items[0]].append(tuple(symbols))
            except KeyError:
                self.rules[items[0]] = [tuple(symbols)]
    
    def _init_terminals(self):
        """
        Builds the list of terminals from self.variables and self.rules
        """
        for rules in self.rules.values():
            for rule in rules:
                if len(rule) == 1:
                    if rule[0] not in self.variables \
                        and rule[0] not in self.terminals:
                        self.terminals.append(rule[0])
    
    def _sample_sentence(self, var):
        """
        Samples a sentence according to rule, by sampling sub-structures
        according to one of their rules, at random.
        """
        if var in self.terminals:
            return var
        else:
            s = ''
            rank = np.random.randint(len(self.rules[var]))
            prod = self.rules[var][rank]
            for v in prod:
                s += self._sample_sentence(v) + ' '
            return s[:-1]
        
    def sample_sentence(self):
        """
        Samples a random sentence belonging to the grammar.
        """
        return self._sample_sentence(self.S)
    
    def tokenize(self, sentence):
        """
        Converts a sentence into a list of tokens.
        """
        return sentence.split(' ')
    
    def symbol_idx(self, args):
        """
        Returns the index number for the symbol passed as arguments.
        """
        if type(args) == str:
            return self._symbol_idx_str(args)
        elif type(args) == tuple or type(args) == list:
            t = []
            for arg in args:
                t.append(self._symbol_idx_str(arg))
            return t
    
    def _symbol_idx_str(self, s):
        """
        Returns the index number for the symbol passed as arguments.
        """
        idx = 0
        for symb in self.variables:
            if symb == s:
                return idx
            idx += 1
        for symb in self.terminals:
            if symb == s:
                return idx
            idx += 1
    
    def chomsky_nf(self):
        """
        Returns True if grammar is in Chomsky Normal Form, False otherwise.
        """
        return True # TODO : implement this.
    
    def _init_non_terminal_rules(self):
        """
        Returns a dict of non-terminal rules.
        """
        for r, prods in self.rules.items():
            for p in prods:
                if len(p) > 1 or p[0] not in self.terminals: 
                    # ^ leave out the last part if in chomsky normal form
                    try:
                        self.nt_rules[r].append(p)
                    except KeyError:
                        self.nt_rules[r] = [p]
    
    def _init_unit_productions(self):
        """
        Builds a dict mapping terminals to their preceding symbols.
        """
        for terminal in self.terminals:
            for r, prods in self.rules.items():
                for p in prods:
                    if len(p) == 1 and terminal in p:
                        try:
                            self.unit_symbols[terminal].append(r)
                        except KeyError:
                            self.unit_symbols[terminal] = [r]
    
    def unit_rule_indices(self, word):
        """
        Returns the list of indices corresponding to the symbols able to 
        produce word, according to the production rules.
        """
        symbols = self.unit_symbols[word]
        return self.symbol_idx(symbols)
    
    def member(self, sentence): # TODO : Fix this !
        """
        Returns True if the sentence is part of the grammar, False otherwise.
        Grammar must be in Chomsky Normal Form.
        """
        assert(self.chomsky_nf())
        tokens = self.tokenize(sentence)
        n = len(tokens)
        r = len(self.variables)
        P = np.zeros([n+1, n+1, r+1], dtype=bool)
        for s, word in enumerate(tokens):
            try:
                for i in self.unit_rule_indices(word):
                    P[1, s+1, i+1] = True
            except KeyError:
                return False
        for l in range(2, n+1): # length of span
            for s in range(1, n-l+2): # position of the start of span
                for p in range(1, l): # different partition of the span
                    for Ra, prods in self.nt_rules.items():
                        a = self.symbol_idx(Ra) + 1 # index of production symbol
                        for prod in prods:
                            print(prod)
                            Rb, Rc = prod # indices of productions
                            b = self.symbol_idx(Rb) + 1
                            c = self.symbol_idx(Rc) + 1
                            if P[p, s, b] and P[l-p, s+p, c]:
                                P[l, s, a] = True
        return P[n, 1, 1] # assuming S is position one, must change this
    
    def parse_tree(self, sentence): # TODO : Fix this !
        """
        Return a parse tree of the sentence. If the sentence is not part of the
        grammar, returns None.
        """
        assert(self.chomsky_nf())
        tokens = self.tokenize(sentence)
        n = len(tokens)
        r = len(self.variables)
        P = np.zeros([n+1, n+1, r+1], dtype=bool)
        mem = {}
        for s, word in enumerate(tokens):
            try:
                for i in self.unit_rule_indices(word):
                    P[1, s+1, i+1] = True
                    mem[(1, s+1)] = UNode(self.variables[i], word)
            except KeyError:
                return None
        for l in range(2, n+1): # length of span
            for s in range(1, n-l+2): # position of the start of span
                for p in range(1, l): # different partition of the span
                    for Ra, prods in self.nt_rules.items():
                        a = self.symbol_idx(Ra) + 1 # index of production symbol
                        for prod in prods:
                            Rb, Rc = prod # indices of productions
                            b = self.symbol_idx(Rb) + 1
                            c = self.symbol_idx(Rc) + 1
                            if P[p, s, b] and P[l-p, s+p, c]:
                                P[l, s, a] = True
                                mem[(l, s)] = BNode(self.variables[a-1],
                                                    mem[(p, s)],
                                                    mem[(l-p, s+p)])
        if P[n, 1, 1]:
            return mem[(n, 1)] # assuming S is position one, must change this
        
        

































