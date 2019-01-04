from v2.src.Objects.VarObj import VariableObj
from v2.src.Objects.printObj import BuiltInObj
from v2.src.Objects.CommentObj import Comment
from v2.src.Objects.ConditionObj import Condition
from v2.src.Objects.LoopObj import LoopObj


class ObjectGenerator:
    def __init__(self, source_ast):
        self.source_ast = source_ast['main_scope']
        self.exec_string = ""

    def object_generation(self, body):
        for ast in self.source_ast:
            if self.check_ast('VariableDeceleration', ast):
                var = VariableObj(ast)
                self.exec_string = var.transpile() + '\n'

            # # Create dictionary condition object and append exec string global exec string
            if self.check_ast('ConditionalStatement', ast):
                gen_condition = Condition(ast, 1)
                self.exec_string += gen_condition.transpile() + '\n'

            # Create dictionary builtin object and append exec string global exec string
            if self.check_ast('PrebuiltFunction', ast):
                gen_builtin = BuiltInObj(ast)
                self.exec_string += gen_builtin.transpile() + "\n"

            # # Create dictionary comment object and append exec string to global exec string when return from
            # transpile method
            if self.check_ast('Comment', ast):
                gen_comment = Comment(ast)
                self.exec_string += gen_comment.transpile() + "\n"
            #
            # # Create dictionary repetition object and append exec string global exec string
            if self.check_ast('ForLoop', ast):
                gen_loop = LoopObj(ast, 1)
                self.exec_string += gen_loop.transpile() + "\n"

        return self.exec_string

    def print_ast(self):
        for i in self.source_ast:
            print(i)

    def check_ast(self, deceleration_name, ast):
        try:
            if ast[deceleration_name]:
                return True
        except:
            return False
