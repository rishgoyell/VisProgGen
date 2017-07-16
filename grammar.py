from canvasops import canvas
import numpy as np
import ply.lex as lex
import ply.yacc as yacc
import commutation

class tree(object):
    def __init__(self, value, lnode=None, rnode=None):
        self.value = value
        self.lnode = lnode
        self.rnode = rnode


class Rules(object):
    numgen = 0      #keeps count of number of valid expressions generated
    path = '/home/rishabh/Documents/VisProgGen/test4/p6'
    exp = None        #the expression being parsed
    random = 0        #set to 1 if random expressionas are being generated and 0  if expression is provided
    visualize = False   #visualize expressions as a tree
    commutate = False

    def p_S(self, p ):
        '''S : E
        '''
        p[1].save(Rules.path+'/'+str(Rules.numgen+1), Rules.random)

        if p[1].flag:
            Rules.numgen = Rules.numgen + 1
            if Rules.random and not Rules.commutate:
                Rules.filename.write(Rules.exp+"\n")
            elif Rules.commutate:
                commexp = commutation.commutate(p[1].treeNode)
                for item in commexp:
                    Rules.filename.write(item+"\n")
                Rules.filename.write("_________________________________\n")

    def p_E1(self, p):
        '''E  : E E UNION
        '''
        if Rules.commutate:
            p[1].treeNode = tree('+', p[1].treeNode,p[2].treeNode)
        p[0] = p[1].union(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)


    def p_E2(self, p):
        '''E : E E DIFFERENCE
        '''
        if Rules.commutate:
            p[1].treeNode = tree('-', p[1].treeNode,p[2].treeNode)
        p[0] = p[1].difference(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)


    def p_E3(self, p):
        '''E : E E INTERSECTION
        '''
        if Rules.commutate:
            p[1].treeNode = tree('*', p[1].treeNode,p[2].treeNode)
        p[0] = p[1].intersection(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)




    def p_E4(self, p):
        '''E : IDENTIFIER '(' INTEGER ',' INTEGER ',' INTEGER ')'
        '''
        p[0] = canvas()
        if Rules.commutate:
            p[0].treeNode = tree(str(p[1]) + str(p[2]) + str(p[3]) + str(p[4]) + str(p[5]) + str(p[6]) + str(p[7]) + str(p[8]))
        center = [p[3], p[5]]
        scale = p[7]

        if p[1] == 'c':
            p[0].draw_circle(center, scale, Rules.random)
        elif p[1] == 's':
            p[0].draw_square(center, scale, Rules.random)
        elif p[1] == 't':
            p[0].draw_triangle(center, scale, Rules.random)
        if Rules.visualize:
            self.makenode(p)



    def p_error(self, p):
        try:
            self.successful = False
            #print("Error "+ str(p.type) + " found at line " + str(p.lineno) + " at position " + str( p.lexpos))
            if Rules.random == 0:
                Rules.numgen += 1
                w = canvas()
                w.save(Rules.path + '/err' + str(Rules.numgen), Rules.random)
            while self.parser.token():
                continue
        except:
            print('Error. Please check, you may not receive the right metrics if you run metrics.py on the generated images.')
