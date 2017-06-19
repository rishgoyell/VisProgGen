#i!/usr/bin/env python
import ply.yacc as yacc
import os, re
import ply.lex as lex
from grammar import Rules
import genexp
import pydot
from canvasops import canvas


numexs = 25000
numops = 3
opcolor = {'+': 'yellow', '-': 'red', '*':'blue'}

class Parser(Rules):
    global numexs
    def __init__(self, graph = None):
        from token_file import build_lexer
        self.tokens, self.lexer = build_lexer(debug_mode=False)
        self.parser = yacc.yacc(module=self)
        self.successful = True  #set to True as long as parsing is proceeding correctly
        self.graph = graph
        self.nnodes = 0
        self.numdraws = 0


    def processFile(self, exp, count):
        Rules.exp = exp
        self.parser.parse(Rules.exp)
        if self.successful:
            if Rules.visualize:
                self.plot_parse_tree(Rules.path +'/vis'+str(count))      #save the visualization graph
        else:
            print('Could not parse expression number '+ str(count) + ': ' + exp)

        #remove unwanted intermediate canvases
        for f in os.listdir(Rules.path):
            if re.search(r'temp[0-9]+', f):
                os.remove(os.path.join(Rules.path, f))


    def processExp(self, exp):
        #end if num of generated samples equals num of required samples
        if Parser.numgen == numexs:
            Rules.filename.close()
            return 0
        else:
            self.numdraws = 0   #keeps track of number of operations, including draws
            Rules.exp = exp
            self.parser.parse(exp)
            if not self.successful:
                print('Could not parse' + exp + 'successfully')
            elif Rules.visualize:
                self.plot_parse_tree('visual'+str(Rules.numgen)+'.png')
            return 1


    def makenode(self, p):
        global numdraws
        global opcolor
        '''
        p : stack
        returns root node
        '''
        parent_id = self.get_unique_id()

        tempimage = Rules.path + '/temp' + str(self.numdraws)
        p[0].save(tempimage, 0)
        self.numdraws = self.numdraws+1

        if len(p) == 4:
            parent = pydot.Node(parent_id, shape='square', image=tempimage+'.png', fontcolor='transparent')
            self.graph.add_node(parent)
            self.graph.add_edge(pydot.Edge(p[1].nodeID, parent_id, fontsize='30',label=p[3]))
            self.graph.add_edge(pydot.Edge(p[2].nodeID, parent_id))
        else:
            parent = pydot.Node(parent_id, fontcolor='transparent', shape='square', image=tempimage+'.png')
            self.graph.add_node(parent)
        p[0].nodeID = parent_id


    def plot_parse_tree(self, filename):
        # self.graph.write_dot(filename + '.dot')
        self.graph.write_png(filename + '.png')

    def get_unique_id(self):
        self.nnodes += 1
        return 'NODE' + str(self.nnodes)



if __name__ == '__main__':
    import sys
    p1 = Parser()
    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):
            Rules.numgen = 0
            Rules.random = 0
            print(sys.argv[i])
            Rules.path = os.path.dirname(sys.argv[i])
            assert type(sys.argv[i]) is str
            try:
                fp = open(sys.argv[i], 'r')
                # if sys.argv[i].endswith('.txt'):
                #     filename = sys.argv[i][:-4]
                count = 0
                for exp in fp:
                    count = count + 1
                    p1.graph = pydot.Dot(graph_type='digraph')
                    p1.successful = True
                    p1.processFile(exp, count)
            except IOError:
                print("Unable to find " + sys.argv[i])

    else:
        flag = 1
        Rules.visualize = False
        Rules.random = 1
        Rules.filename = open(Rules.path+'/expressions.txt', 'w')  #file that stores list of expressions corresonding to all data
        while flag:
            p1.successful = True
            exp = genexp.fixedSizeExp(numops)
            flag = p1.processExp(exp)
