import ast, sys
class Norm(ast.NodeTransformer):
    def visit_Constant(self, n):
        if isinstance(n.value, str): return ast.copy_location(ast.Constant(value="<STR>"), n)
        return n
def norm(p):
    t = ast.parse(open(p,encoding='utf-8').read())
    for n in ast.walk(t):
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef,ast.Module)):
            if (n.body and isinstance(n.body[0],ast.Expr) and isinstance(n.body[0].value,ast.Constant)
                and isinstance(n.body[0].value.value,str)): n.body.pop(0)
            if not n.body: n.body=[ast.Pass()]
    return ast.dump(Norm().visit(ast.fix_missing_locations(t)))
a,b = norm(sys.argv[1]), norm(sys.argv[2])
print(sys.argv[2], "| AST (strings+docstrings normalised):", "IDENTICAL" if a==b else "DIFFERS")
