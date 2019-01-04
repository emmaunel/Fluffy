class BuiltInObj():
    def __init__(self, ast):
        self.ast = ast['PrebuiltFunction']
        self.exec_string = ""

    def transpile(self):
        for ast in self.ast:

            # Get the name of the builtin function being called
            try:
                if ast['type'] == "print":
                    self.exec_string += "print("
            except:
                pass

            # Get arguments for the function being called
            # TODO Add support for more than one argument
            try:
                self.exec_string += ast['arguments'][0] + ")"
            except:
                pass

        return self.exec_string