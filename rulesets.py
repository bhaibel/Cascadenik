from cssutils.tokenize2 import Tokenizer as cssTokenizer

class ParseException (Exception): pass

css = """

Layer
{
    line-width: 0;
}

.class[zoom>1],
#id[zoom="1"]
{
    line-width: 1;
}

Layer#id[zoom>2][zoom<=3]
{
    line-width: 2;
    line-width: 3 3;
}

*
{
    line-width: "hello";
}

"""

def post_attribute(tokens):

    while True:
        nname, value, line, col = tokens.next()
        
        if nname == 'IDENT':
            print '  A.', value
        
        elif (nname, value) in [('CHAR', '<'), ('CHAR', '>')]:
            _nname, _value, line, col = tokens.next()

            if (_nname, _value) == ('CHAR', '='):
                print '  B.', value, _value
            
            elif _nname in ('NUMBER', 'STRING'):
                print '  C.', value, _value
            
            else:
                raise Exception()
        
        elif (nname, value) == ('CHAR', '='):
            print '  D.', value
        
        elif nname in ('NUMBER', 'STRING'):
            print '  E.', value
        
        elif (nname, value) == ('CHAR', ']'):
            break
        
        else:
            raise Exception()

def post_block(tokens):

    while True:
        nname, value, line, col = tokens.next()
        
        if nname == 'IDENT':
            _nname, _value, line, col = tokens.next()
            
            if (_nname, _value) == ('CHAR', ':'):
                print '    a.', value
                
                while True:
                    nname, value, line, col = tokens.next()
                    
                    if (nname, value) == ('CHAR', ';'):
                        break
                    
                    elif nname != 'S':
                        print '    b.', nname, repr(value)
                
            else:
                raise Exception()
        
        if (nname, value) == ('CHAR', '}'):
            break

print css

tokens = cssTokenizer().tokenize(css)

while True:
    nname, value, line, col = tokens.next()
    
    if nname == 'IDENT':
        print '1.', nname, repr(value)
    
    elif nname == 'HASH':
        print '2.', nname, repr(value)
    
    elif (nname, value) == ('CHAR', '.'):
        
        while True:
            nname, value, line, col = tokens.next()
            
            if nname == 'IDENT':
                print '3.', nname, repr(value)
                break
            
            else:
                # something other than a class?
                raise Exception()
    
    elif (nname, value) == ('CHAR', '*'):
        print '3.', nname, repr(value)
    
    elif (nname, value) == ('CHAR', ','):
        print '- or'
    
    elif (nname, value) == ('CHAR', '['):
        post_attribute(tokens)
    
    elif (nname, value) == ('CHAR', '{'):
        print '- end selector'
        post_block(tokens)
        print '-' * 20
