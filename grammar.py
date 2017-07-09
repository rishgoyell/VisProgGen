from canvasops import canvas
import numpy as np
import ply.lex as lex
import ply.yacc as yacc

class Rules(object):
    numgen = 0      #keeps count of number of valid expressions generated
    path = '/home/rishabh/Documents/VisProgGen/testrot/p4'
    exp = None        #the expression being parsed
    random = 0        #set to 1 if random expressionas are being generated and 0  if expression is provided
    visualize = True   #visualize expressions as a tree

    def p_S(self, p ):
        '''S : E
        '''
        p[1].save(Rules.path+'/'+str(Rules.numgen+1), Rules.random)

        if p[1].flag:
            Rules.numgen = Rules.numgen + 1
            if Rules.random:
                Rules.filename.write(Rules.exp+"\n")

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
        | IDENTIFIER '(' INTEGER ',' INTEGER ',' INTEGER ',' INTEGER ')'
        '''
        p[0] = canvas()
        center = [p[3], p[5]]
        scale = p[7]
        if len(p)==11:
            angle = p[9]
        if p[1] == 'c':
            p[0].draw_circle(center, scale, Rules.random)
        elif p[1] == 's':
            p[0].draw_square(center, scale, angle, Rules.random)
        elif p[1] == 't':
            p[0].draw_triangle(center, scale, angle, Rules.random)
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
