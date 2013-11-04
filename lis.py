def tokenize(s):
    return s.replace('(',' ( ').replace(')', ' ) ').split()

def parse(tokens):
    #import pdb;pdb.set_trace()
    if len(tokens)==0:
        raise SyntaxError('unespected EOF while reading')

    token = tokens.pop(0)

    if token=='(':
        L = []
        while tokens[0]!=')':
            L.append(parse(tokens))
            #BUG FIX: parsing '(()'
            if not tokens:
                raise SyntaxError('need ")"')
        tokens.pop(0)
        return L

    elif token ==')':
        raise SyntaxError('unespected ")"')
    else:
        return token


def car(x):
    if not isinstance(x, list):
        raise SyntaxError('%s is not list' %x)
    if not x:
        raise SyntaxError("%s is empty" %x)
    return x[0]

global_env = {
        '+':lambda x, y:x+y,        
        '-':lambda x, y:x-y,        
        '*':lambda x, y:x*y,        
        '/':lambda x, y:x/y,        
        'eq':lambda x, y: x==y,
        'car':car,
        'cdr':lambda x:x[1:],
        'atom':lambda x: x is str,
        }


def eval(x, env=global_env):
    if isinstance(x, str):
        try:
            try:
                return int(x)
            except:
                return float(x)
        except:
            if not env.get(x):
                raise NameError('undefined symbol %s' % x)
            return env[x]

    elif not x:
        return []

    elif x[0] == 'quote':
        return x[1]

    elif x[0] == 'define':
        _, var, exp = x
        env[var] = eval(exp, env) #

    elif x[0] == 'lambda':
        _, var, exp = x
        def wrapper(*args):
            env.update(zip(var, args))
            return eval(exp, env)
        return wrapper
    else:
        exps = [eval(exp, env) for exp in x]
        proc = exps.pop(0)
        return proc(*exps)


def to_string(x):
    pass

def repl(prompt='lis.py>'):
    while True:
        try:
            val =  eval(parse(tokenize(raw_input(prompt))))
            print val 
        except SyntaxError as e:
            print e

repl()
