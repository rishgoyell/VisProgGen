import canvasops as ops

class Rules(object):
    def p_S(self, p ):
        '''S : E
        '''
        print(p[1])

    def p_E1(self, p):
        '''E  : E E UNION
        '''
        p[0] = ops.union(p[1],p[2])

    def p_E2(self, p):
        '''E : E E DIFFERENCE
        '''
        p[0] = ops.difference(p[1],p[2])


    def p_E3(self, p):
        '''E : E E INTERSECTION
        '''
        p[0] = ops.intersection(p[1],p[2])


    def p_E4(self, p):
        '''E : IDENTIFIER '(' INTEGER ',' INTEGER ',' INTEGER ')'
        '''
        x = ops.canvas()
        center = [p[3], p[5]]
        scale = p[7]

        if p[1] == 'c':
            x.draw_circle(center, scale)
        elif p[1] == 's':
            x.draw_square(center, scale)
        elif p[1] == 't':
            x.draw_triangle(center, scale)

        p[0] = x.canvasID

    def p_error(self, p):
        try:
            self.successful = False
            print("Error "+ str(p.type) + " found at line " + str(p.lineno) + " at position " + str( p.lexpos))
            parser.errok()
        except:
            print('Unknown error')

