from canvasops import canvas

class Rules(object):
    def p_S(self, p ):
        '''S : E
        '''
        p[1].display()

    def p_E1(self, p):
        '''E  : E E UNION
        '''
        p[0] = p[1].union(p[2])

    def p_E2(self, p):
        '''E : E E DIFFERENCE
        '''
        p[0] = p[1].difference(p[2])


    def p_E3(self, p):
        '''E : E E INTERSECTION
        '''
        p[0] = p[1].intersection(p[2])


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


    def p_error(self, p):
        try:
            self.successful = False
            print("Error "+ str(p.type) + " found at line " + str(p.lineno) + " at position " + str( p.lexpos))
            parser.errok()
        except:
            print('Unknown error')

