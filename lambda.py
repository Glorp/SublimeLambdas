import sublime, sublime_plugin

class BetaReduceCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        line = self.view.line(self.view.sel()[0].begin());
        expression = parse(self.view.substr(line))
        allNames = expression.allNames()
        res, s = reduceOrRename(expression)
        if res is None:
            res = expression
        p = line.end()
        p = p + self.view.insert(edit, line.end(), s + u"\n" + res.__unicode__())
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(p))
        self.view.show(p)

class BetaReduceLotsCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        line = self.view.line(self.view.sel()[0].begin());
        expression = parse(self.view.substr(line))
        allNames = expression.allNames()
        res = u""
        i = 0
        p = line.end()
        while True:
            expression, s = reduceOrRename(expression)
            i = i + 1
            if expression is None or i == 1000:
                break
            p = p + self.view.insert(edit, p, s + u"\n" + expression.__unicode__())
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(p))
        self.view.show(p)
    

class LambdaExpandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        defs = makeDefinitions(self.view)
        line = self.view.line(self.view.sel()[0].begin());
        expression = parse(self.view.substr(line), defs)
        p = line.end()
        p = p + self.view.insert(edit, p, u"\n" + expression.__unicode__())
        self.view.sel().clear()
        self.view.sel().add(sublime.Region(p))
        self.view.show(p)

def reduceOrRename(expression):
    allNames = expression.allNames()
    reducible = expression.find(lambda x: x.isReducible())
    if reducible is None:
        return None, u""
    s = expression.followPath(reducible).findConflict()
    if s is None:
        return expression.followPathThen(reducible, lambda x: x.betaReduce()), u""
    scope = expression.findScope(reducible, s)
    newName = uniqueName(s, allNames)
    if scope is None:
        expression = expression.replace(s, Symbol(newName))
    else:
        expression = expression.rename(s, newName, scope)
    return expression, u" | " + s + u" -> " + newName
                

def withParens(s):
    return u"(" + s + u")"

def makeDefinitions(view):
    res = {}
    lines = view.find_all(u":=")
    for region in lines:
        line = view.substr(view.line(region.begin()))
        x = line.partition(u":=")
        name = x[0].strip()
        res[name] = parse(x[2], res)
    return res

def uniqueName(s, allNames):
    num = s
    s = ""
    while len(num) > 0 and not num.isdigit():
        s = s + num[0]
        num = num[1:]
    if len(num) == 0:
        num = 1
    else:
        num = int(num) + 1
    for existing in allNames:
        if existing.startswith(s):
            existingNum = existing[len(s):]
            if existingNum.isdigit() and int(existingNum) >= num:
                num = int(existingNum) + 1
    return s + str(num)

class Term:
    def followPathThen(self, path, f):
        if len(path) == 0:
            return f(self)
        i = path[0]
        children = self.children()
        children = children[:i] + [children[i].followPathThen(path[1:], f)] + children[i + 1:]
        return self.__class__(*self.parameters() + children)
    def parameters(self):
        return []
    def children(self):
        return []
    def followPath(self, path):
        res = self
        for i in path:
            res = res.children()[i]
        return res
    def replaceOne(self, path, new):
        return self.followPathThen(path, lambda x: new)
    def replace(self, old, new, scope = []):
        return self.followPathThen(scope, lambda x: x.privReplace(old, new))
    def privReplace(self, old, new):
        children = map(lambda x: x.privReplace(old, new), self.children())
        return self.__class__(*self.parameters() + children)
    def rename(self, old, new, scope):
        return self.followPathThen(scope, lambda x: x.privRename(old, new))
    def find(self, pred):
        path = []
        def step(current):
            if pred(current):
                return True
            i = 0
            for child in current.children():
                path.append(i)
                if step(child):
                    return True
                path.pop()
                i = i + 1
            return None
        if step(self):
            return path
        return None
    def isReducible(self):
        return False
    def findScope(self, path, s):
        res = None
        tmp = []
        exp = self
        if isinstance(exp, Lambda) and exp.param == s:
                res = tmp[:]
        for i in path:
            tmp.append(i)
            exp = exp.children()[i]
            if isinstance(exp, Lambda) and exp.param == s:
                res = tmp[:]
        return res
    def privFindConflict(self, param, freeSymbols, possibleConflicts = set([])):
        for child in self.children():
            res = child.privFindConflict(param, freeSymbols, possibleConflicts)
            if res is not None:
                return res
        return None
    def freeSymbols(self, env = set([])):
        res = set([])
        for child in self.children():
            res = res.union(child.freeSymbols(env))
        return res
    def allNames(self):
        res = set([])
        for child in self.children():
            res = res.union(child.allNames())
        return res


class Lambda(Term):
    def __init__(self, param, term):
        self.param = param
        self.term = term
    def __unicode__(self):
        return u"\u03bb" + self.param + u"." + self.term.__unicode__()
    def lispy(self):
        return u"(\u03bb " + self.param + u" " + self.term.lispy() + u")"
    def parameters(self):
        return [self.param]
    def children(self):
        return [self.term]
    def freeSymbols(self, env = set([])):
        env = env.copy()
        env.add(self.param)
        return self.term.freeSymbols(env)
    def allNames(self):
        res = self.term.allNames()
        res.add(self.param)
        return res
    def privFindConflict(self, param, freeSymbols, possibleConflicts = set([])):
        if param == self.param:
            return None
        if self.param in freeSymbols:
            possibleConflicts = possibleConflicts.copy()
            possibleConflicts.add(self.param)
        return self.term.privFindConflict(param, freeSymbols, possibleConflicts)
    def privReplace(self, old, new):
        if old == self.param:
            return self
        else:
            return Term.privReplace(self, old, new)
    def privRename(self, old, new):
        return Lambda(new, self.term.privReplace(old, Symbol(new)))

class Application(Term):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2
    def __unicode__(self):
        s1 = self.term1.__unicode__()
        if isinstance(self.term1, Lambda):
            s1 = withParens(s1)
        s2 = self.term2.__unicode__()
        if isinstance(self.term2, Lambda) or isinstance(self.term2, Application):
            s2 = withParens(s2)
        return s1 + u" " + s2
    def lispy(self):
        return "(apply " + self.term1.lispy() + " " + self.term2.lispy() + ")"
    def children(self):
        return [self.term1, self.term2]
    def isReducible(self):
        return isinstance(self.term1, Lambda)
    def findConflict(self):
        return self.term1.term.privFindConflict(self.term1.param, self.term2.freeSymbols())
    def betaReduce(self):
        return self.term1.term.replace(self.term1.param, self.term2)


class Symbol(Term):
    def __init__(self, name):
        if not isinstance(name, unicode):
            raise "eep"
        self.name = name
    def __unicode__(self):
        return self.name
    def lispy(self):
        return self.name
    def freeSymbols(self, env = set([])):
        if self.name in env:
            return set([])
        return set([self.name])
    def allNames(self):
        return set([self.name])
    def parameters(self):
        return [self.name]
    def privFindConflict(self, param, freeSymbols, possibleConflicts = set([])):
        if self.name in possibleConflicts:
            return self.name
        return None
    def privReplace(self, old, new):
        if self.name == old:
            return new
        return self

class Parser:
    def __init__(self, s, defs):
        self.s = s
        self.defs = defs
        self.i = 0
        self.updateC()

    def readNext(self):
        self.i = self.i + 1
        return self.updateC()

    def updateC(self):
        if self.i < len(self.s):
            self.c = self.s[self.i]
            return True
        else:
            self.c = None
            return False
        
    def readTerm(self):
        if self.c == u'\u03bb':
            self.readNext()
            return self.readLambda()
        elif self.c == '(':
            self.readNext()
            return self.readParen()
        else:
            return self.readSymbol()
    
    def readExpression(self):
        self.fwd()
        res = self.readTerm()
        while self.fwd():
            res = Application(res, self.readTerm())
        return res

    def readSymbol(self):
        start = self.i
        while self.c is not None and self.c != ' ':
            self.readNext()
        name = self.s[start:self.i]
        if self.defs.has_key(name):
            return self.defs[name]
        return Symbol(name)

    def readLambda(self):
        start = self.i
        while self.c != '.':
            self.readNext()
        p = self.s[start:self.i]
        self.readNext()
        return Lambda(p, self.readExpression())

    def readParen(self):
        start = self.i
        count = 1
        while self.c is not None:
            if self.c == '(':
                count = count + 1
            elif self.c == ')':
                count = count - 1
                if count == 0:
                    self.readNext()
                    return parse(self.s[start:self.i - 1], self.defs)
            self.readNext()

    def fwd(self):
        while self.c is not None:
            if self.c != ' ':
                return True
            self.readNext()
        return False

def parse(s, defs = {}):
    return Parser(s.partition("|")[0], defs).readExpression()
