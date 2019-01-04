class VariableObj():
    def __init__(self, ast):
        # The ast will hold the dictionary version of the ast which is like a blueprint
        self.ast = ast['VariableDeceleration']
        # This will hold the exec string for variable deceleration
        self.exec_string = ""

    def transpile(self):
        #print(self.ast)
        """
        This method will use the AST in order to create a python version of the tachyon
        generated dictionary AST.

        :return: exec_string -> Translation to python code
        """

        # Loop through each dictionary value items
        for i in self.ast:
            #print(i)
            #self.exec_string = i['name'] + " = " + i['value']
            # Get the name of the variable
            try:
                self.exec_string += i['name'] + " = "
            except:
                pass

            # Get the value of the variable
            try:
                self.exec_string += str(i['value'])
            except:
                pass

        return self.exec_string
