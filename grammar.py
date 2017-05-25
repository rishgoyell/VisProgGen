from canvasops import canvas
import numpy as np


class Rules(object):
    numgen = 0      #keeps count of number of valid expressions generated
    path = '/home/rishabh/Documents/VisProgGen/test/'
    filename = open(path+'expressions.txt', 'w')  #file that stores list of expressions corresonding to all data
    exp = None        #the expression being parsed
    random = 1        #set to 1 if random expressionas are being generated and 0  if expression is provided
    visualize = True     #visualize expressions as a tree


    def p_S(self, p ):
        '''S : E
        '''
        p[1].save(Rules.path+str(Rules.numgen+1), Rules.random)
        if p[1].flag and Rules.random:
            Rules.filename.write(Rules.exp+"\n")
            Rules.numgen = Rules.numgen + 1


    def p_E1(self, p):
        '''E  : E E UNION
        '''
        p[0] = p[1].union(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)


    def p_E2(self, p):
        '''E : E E DIFFERENCE
        '''
        p[0] = p[1].difference(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)


    def p_E3(self, p):
        '''E : E E INTERSECTION
        '''
        p[0] = p[1].intersection(p[2], Rules.random)
        if Rules.visualize:
            self.makenode(p)



    def p_E4(self, p):
        '''E : IDENTIFIER '(' INTEGER ',' INTEGER ',' INTEGER ')'
        '''
        p[0] = canvas()
        center = [p[3], p[5]]
        scale = p[7]

        if p[1] == 'c':
            p[0].draw_circle(center, scale)
        elif p[1] == 's':
            p[0].draw_square(center, scale)
        elif p[1] == 't':
            p[0].draw_triangle(center, scale)
        if Rules.visualize:
            self.makenode(p)



    def p_error(self, p):
        try:
            self.successful = False
            print("Error "+ str(p.type) + " found at line " + str(p.lineno) + " at position " + str( p.lexpos))
            parser.errok()
        except:
            print('Unknown error')

