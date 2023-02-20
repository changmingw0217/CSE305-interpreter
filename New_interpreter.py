import copy

"""
Predefine some values
"""
error = ":error:"
true = ":true:"
false = ":false:"


def interpreter(input_file_string, output_file_string):
    file_read = list()
    interpreter1 = Interpreter()
    input_file = open(input_file_string, 'r')
    output_file = open(output_file_string, 'w')
    print(input_file)
    for line in input_file:
        if line == "quit\n" or line == "quit":
            break
        file_read.append(line[:-1])

    for command in file_read:
        Interpreter.command_helper(interpreter1, file_read)

    # print(file_read)
    # print(interpreter1.stack[interpreter1.index])
    # print(interpreter1.type_stack)
    # print(interpreter1.bind_val)
    # print(interpreter1.fun_val)

    for item in interpreter1.stack[interpreter1.index]:

        output_file.write(str(item) + '\n')

    input_file.close()
    output_file.close()


class Interpreter(object):

    def __init__(self):
        self.stack = [[]]
        self.type_stack = [[]]
        self.bind_val = [{}]
        self.fun_val =[{}]
        self.index = 0
        self.command_count = 0

    def command_helper(self, file_read):
        if self.command_count < len(file_read):
            command = file_read[self.command_count]
            cmd = command.split(" ", 1)[0]
            if cmd == 'push':
                val = command.split(" ", 1)[1]
                self.stack[self.index].insert(0, self.push(val)[0])
                self.type_stack[self.index].insert(0, self.push(val)[1])
                self.command_count += 1
            elif cmd == 'pop':
                self.pop()
                self.command_count += 1
            elif cmd == 'add':
                self.add()
                self.command_count += 1
            elif cmd == 'sub':
                self.sub()
                self.command_count += 1
            elif cmd == 'mul':
                self.mul()
                self.command_count += 1
            elif cmd == 'div':
                self.div()
                self.command_count += 1
            elif cmd == 'rem':
                self.rem()
                self.command_count += 1
            elif cmd == 'neg':
                self.neg()
                self.command_count += 1
            elif cmd == 'swap':
                self.swap()
                self.command_count += 1
            elif cmd == 'cat':
                self.cat()
                self.command_count += 1
            elif cmd == 'and':
                self.And()
                self.command_count += 1
            elif cmd == 'or':
                self.Or()
                self.command_count += 1
            elif cmd == 'not':
                self.Not()
                self.command_count += 1
            elif cmd == 'equal':
                self.equal()
                self.command_count += 1
            elif cmd == 'lessThan':
                self.lessThan()
                self.command_count += 1
            elif cmd == 'bind':
                self.bind()
                self.command_count += 1
            elif cmd == 'if':
                self.If()
                self.command_count += 1
            elif cmd == 'let':
                self.let()
                self.command_count += 1
            elif cmd == 'end':
                self.end()
                self.command_count += 1
            elif cmd == 'fun' and len(command.split()) == 3:
                fun_list = file_read[self.command_count+1:]
                fun, fun_name, para = command.split()
                self.stack[self.index].insert(0, ":unit:")
                self.type_stack[self.index].insert(0, 6)
                bind_copy = copy.deepcopy(self.bind_val[self.index])
                fun_copy = copy.deepcopy(self.fun_val[self.index])
                code_list = []
                fun_counts = 1
                for item in fun_list:
                    if item == "funEnd" and fun_counts == 1:
                        self.command_count += 1
                        break
                    if "fun" in item and len(item.split()) == 3:
                        fun_counts += 1
                    if item == "funEnd":
                        fun_counts -= 1
                    code_list.append(item)
                    self.command_count += 1
                self.fun_val[self.index][fun_name] = ["push " + para, code_list, bind_copy, fun_copy, "fun"]
                self.fun_val[self.index][fun_name][3][fun_name] = ["push " + para, code_list, bind_copy, fun_copy, "fun"]
                self.command_count += 1
            elif cmd == 'inOutFun':
                fun_list = file_read[self.command_count + 1:]
                fun, fun_name, para = command.split()
                self.stack[self.index].insert(0, ":unit:")
                self.type_stack[self.index].insert(0, 6)
                bind_copy = copy.deepcopy(self.bind_val[self.index])
                fun_copy = copy.deepcopy(self.fun_val[self.index])
                code_list = []
                for item in fun_list:
                    if item == "funEnd":
                        self.command_count += 1
                        break
                    code_list.append(item)
                    self.command_count += 1
                self.fun_val[self.index][fun_name] = ["push " + para, code_list, bind_copy, fun_copy, "inOutFun"]
                self.fun_val[self.index][fun_name][3][fun_name] = ["push " + para, code_list, bind_copy, fun_copy, "inOutFun"]
                self.command_count += 1
            elif cmd == 'call':
                self.call()
                self.command_count += 1
            else:
                self.stack[self.index].insert(0, error)
                self.type_stack[self.index].insert(0, 1)
                self.command_count += 1

    def push(self, val):

        if self.is_int(val):
            val = int(val)
            return val, 2
        elif self.is_string(val):
            return val[1:-1], 3
        elif self.is_name(val):
            return val, 4
        elif self.is_bool(val):
            return val, 5
        else:
            return error, 1

    def pop(self):

        if len(self.stack[self.index]) > 0:
            self.stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def add(self):

        if self.type_checker("add") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 + num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("add") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] + num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("add") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 + self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("add") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] + self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def sub(self):

        if self.type_checker("sub") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 - num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("sub") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] - num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("sub") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 - self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("sub") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] - self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def mul(self):

        if self.type_checker("mul") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 * num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("mul") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] * num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("mul") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 * self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("mul") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] * self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def div(self):

        if self.type_checker("div") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 // num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("div") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] // num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("div") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 // self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("div") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] // self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def rem(self):

        if self.type_checker("rem") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 % num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("rem") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] % num2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("rem") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = num1 % self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        elif self.type_checker("rem") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][num1][0] % self.bind_val[self.index][num2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def neg(self):

        if self.type_checker("neg") == 1:
            self.stack[self.index][0] = -self.stack[self.index][0]
        elif self.type_checker("neg") == 2:
            self.type_stack[self.index].pop(0)
            val = self.stack[self.index].pop(0)
            self.stack[self.index].insert(0, -self.bind_val[self.index][val][0])
            self.type_stack[self.index].insert(0, 2)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def swap(self):

        if self.type_checker("swap") == 1:
            self.stack[self.index][0], self.stack[self.index][1] = self.stack[self.index][1], self.stack[self.index][0]
            self.type_stack[self.index][0], self.type_stack[self.index][1] = self.type_stack[self.index][1], self.type_stack[self.index][0]
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def cat(self):
        if self.type_checker("cat") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            str2 = self.stack[self.index].pop(0)
            str1 = self.stack[self.index].pop(0)
            res = str1 + str2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 3)
        elif self.type_checker("cat") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            str2 = self.stack[self.index].pop(0)
            str1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][str1][0] + str2
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 3)
        elif self.type_checker("cat") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            str2 = self.stack[self.index].pop(0)
            str1 = self.stack[self.index].pop(0)
            res = str1 + self.bind_val[self.index][str2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 3)
        elif self.type_checker("cat") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            str2 = self.stack[self.index].pop(0)
            str1 = self.stack[self.index].pop(0)
            res = self.bind_val[self.index][str1][0] + self.bind_val[self.index][str2][0]
            self.stack[self.index].insert(0, res)
            self.type_stack[self.index].insert(0, 3)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def And(self):

        if self.type_checker("and") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.stack[self.index].pop(0)
            bool1 = self.stack[self.index].pop(0)
            if bool1 == true and bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("and") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.stack[self.index].pop(0)
            bool1 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            if bool1 == true and bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("and") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            bool1 = self.stack[self.index].pop(0)
            if bool1 == true and bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("and") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            bool1 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            if bool1 == true and bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def Or(self):

        if self.type_checker("or") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.stack[self.index].pop(0)
            bool1 = self.stack[self.index].pop(0)
            if bool1 == true or bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("or") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.stack[self.index].pop(0)
            bool1 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            if bool1 == true or bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("or") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            bool1 = self.stack[self.index].pop(0)
            if bool1 == true or bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("or") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            bool2 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            bool1 = self.bind_val[self.index][self.stack[self.index].pop(0)][0]
            if bool1 == true or bool2 == true:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def Not(self):
        if self.type_checker("not") == 1:
            self.type_stack[self.index].pop(0)
            bool1 = self.stack[self.index].pop(0)
            if bool1 == true:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("not") == 2:
            self.type_stack[self.index].pop(0)
            bool1 = self.stack[self.index].pop(0)
            if self.bind_val[self.index][bool1][0] == true:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def equal(self):
        if self.type_checker("equal") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if num1 == num2:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("equal") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if self.bind_val[self.index][num1][0] == num2:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("equal") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if num1 == self.bind_val[self.index][num2][0]:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("equal") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if self.bind_val[self.index][num1][0] == self.bind_val[self.index][num2][0]:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def lessThan(self):
        if self.type_checker("lessThan") == 1:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if num1 < num2:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("lessThan") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if self.bind_val[self.index][num1][0] < num2:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("lessThan") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if num1 < self.bind_val[self.index][num2][0]:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        elif self.type_checker("lessThan") == 4:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            num2 = self.stack[self.index].pop(0)
            num1 = self.stack[self.index].pop(0)
            if self.bind_val[self.index][num1][0] < self.bind_val[self.index][num2][0]:
                self.stack[self.index].insert(0, true)
                self.type_stack[self.index].insert(0, 5)
            else:
                self.stack[self.index].insert(0, false)
                self.type_stack[self.index].insert(0, 5)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def bind(self):
        if self.type_checker("bind") == 1:
            val_type = self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            val = self.stack[self.index].pop(0)
            name = self.stack[self.index].pop(0)
            self.bind_val[self.index][name] = [val, val_type]
            self.stack[self.index].insert(0, ":unit:")
            self.type_stack[self.index].insert(0, 6)
        elif self.type_checker("bind") == 2:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            val = self.stack[self.index].pop(0)
            name = self.stack[self.index].pop(0)
            self.bind_val[self.index][name] = self.bind_val[self.index][val]
            self.stack[self.index].insert(0, ":unit:")
            self.type_stack[self.index].insert(0, 6)
        elif self.type_checker("bind") == 3:
            self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            val = self.stack[self.index].pop(0)
            name = self.stack[self.index].pop(0)
            self.fun_val[self.index][name] = self.fun_val[self.index][val]
            self.stack[self.index].insert(0, ":unit:")
            self.type_stack[self.index].insert(0, 6)

        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def If(self):
        if self.type_checker("if") == 1:
            val1_type = self.type_stack[self.index].pop(0)
            val2_type = self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            val1 = self.stack[self.index].pop(0)
            val2 = self.stack[self.index].pop(0)
            if_bool = self.stack[self.index].pop(0)
            if if_bool == true:
                self.stack[self.index].insert(0, val1)
                self.type_stack[self.index].insert(0, val1_type)
            else:
                self.stack[self.index].insert(0, val2)
                self.type_stack[self.index].insert(0, val2_type)
        elif self.type_checker("if") == 2:
            val1_type = self.type_stack[self.index].pop(0)
            val2_type = self.type_stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            val1 = self.stack[self.index].pop(0)
            val2 = self.stack[self.index].pop(0)
            if_bool = self.stack[self.index].pop(0)
            if self.bind_val[self.index][if_bool][0] == true:
                self.stack[self.index].insert(0, val1)
                self.type_stack[self.index].insert(0, val1_type)
            else:
                self.stack[self.index].insert(0, val2)
                self.type_stack[self.index].insert(0, val2_type)

        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def let(self):
        self.stack.append([])
        self.type_stack.append([])
        self.bind_val.append(copy.deepcopy(self.bind_val[self.index]))
        self.fun_val.append(copy.deepcopy(self.fun_val[self.index]))
        self.index += 1

    def end(self):
        self.stack[self.index - 1].insert(0, self.stack[self.index].pop(0))
        self.type_stack[self.index - 1].insert(0, self.type_stack[self.index].pop(0))
        self.stack.pop()
        self.type_stack.pop()
        self.bind_val.pop()
        self.fun_val.pop()
        self.index -= 1

    def call(self):

        if self.type_checker("call") == 1:
            closure = Interpreter()
            para = self.stack[self.index].pop(0)
            para_type = self.type_stack[self.index].pop(0)
            fun_name = self.stack[self.index].pop(0)
            self.type_stack[self.index].pop(0)
            codes = self.fun_val[self.index][fun_name][1]
            closure.bind_val[closure.index] = copy.deepcopy(self.fun_val[self.index][fun_name][2])
            closure.fun_val[closure.index] = copy.deepcopy(self.fun_val[self.index][fun_name][3])
            if para_type == 4 and para in self.bind_val[self.index]:
                closure.bind_val[closure.index][para] = self.bind_val[self.index][para]

            if self.fun_val[self.index][fun_name][-1] == "fun":
                i = 0
                while i < len(codes):
                    # print(codes[i])
                    if codes[i] == 'return':
                        result = closure.stack[closure.index][0]
                        result_type = closure.type_stack[closure.index][0]
                        if result_type == 4 and result in closure.bind_val[closure.index]:
                            res = closure.bind_val[closure.index][result][0]
                            res_type = closure.bind_val[closure.index][result][1]
                            self.stack[self.index].insert(0, res)
                            self.type_stack[self.index].insert(0, res_type)
                        elif result_type == 4 and result in closure.fun_val[closure.index]:
                            self.fun_val[self.index].update(closure.fun_val[closure.index])
                            self.stack[self.index].insert(0, result)
                            self.type_stack[self.index].insert(0, result_type)
                        else:
                            self.stack[self.index].insert(0, result)
                            self.type_stack[self.index].insert(0, result_type)
                        break
                    elif codes[i] == self.fun_val[self.index][fun_name][0]:
                        closure.stack[closure.index].insert(0, para)
                        closure.type_stack[closure.index].insert(0, para_type)
                        closure.command_count += 1
                        i += 1
                    elif 'fun' in codes[i] and len(codes[i].split()) == 3:
                        fun, func_name, func_para = codes[i].split()
                        closure.stack[closure.index].insert(0, ":unit:")
                        closure.type_stack[closure.index].insert(0, 6)
                        bind_copy = copy.deepcopy(closure.bind_val[closure.index])
                        fun_copy = copy.deepcopy(closure.fun_val[closure.index])
                        code_list = []
                        end = len(codes) - codes[::-1].index("funEnd") - 1
                        for j in range(closure.command_count + 1, end):
                            if codes[j] == self.fun_val[self.index][fun_name][0]:
                                func_arg = 'push {}'.format(para)
                                code_list.append(func_arg)
                                i += 1
                                closure.command_count += 1
                            else:
                                code_list.append(codes[j])
                                i += 1
                                closure.command_count += 1
                        closure.fun_val[closure.index][func_name] = ["push " + func_para, code_list, bind_copy, fun_copy, "fun"]
                        closure.fun_val[closure.index][func_name][3][func_name] = ["push " + func_para, code_list, bind_copy, fun_copy, "fun"]
                        i += 2
                        closure.command_count += 2
                        # print(closure.fun_val)
                    else:
                        closure.command_helper(codes)
                        i += 1
            else:

                for i in range(len(codes)):

                    if codes[i] == 'return':
                        result = closure.stack[closure.index][0]
                        result_type = closure.type_stack[closure.index][0]
                        if result_type == 4 and result in closure.bind_val[closure.index]:
                            res = closure.bind_val[closure.index][result][0]
                            res_type = closure.bind_val[closure.index][result][1]
                            self.stack[self.index].insert(0, res)
                            self.type_stack[self.index].insert(0, res_type)
                        else:
                            self.stack[self.index].insert(0, result)
                            self.type_stack[self.index].insert(0, result_type)
                        break
                    elif codes[i] == self.fun_val[self.index][fun_name][0]:
                        closure.stack[closure.index].insert(0, para)
                        closure.type_stack[closure.index].insert(0, para_type)
                        closure.command_count += 1
                        # print(closure.stack)
                    elif codes[i] == 'bind':
                        closure.bind()
                        self.bind_val[self.index].update(closure.bind_val[closure.index])
                        closure.command_count += 1
                    else:
                        closure.command_helper(codes)
                        # print(closure.stack)
        else:
            self.stack[self.index].insert(0, error)
            self.type_stack[self.index].insert(0, 1)

    def type_checker(self, cmd):

        if cmd == 'add' or cmd == 'sub' or cmd == 'mul' or cmd == 'equal' or cmd == 'lessThan':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][0] == 2 and self.type_stack[self.index][1] == 2:
                    return 1
                elif self.type_stack[self.index][0] == 2 and self.type_stack[self.index][1] == 4 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 2:
                    return 2
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 2 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 2:
                    return 3
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 2 and self.stack[self.index][1] in self.bind_val[self.index]and self.bind_val[self.index][self.stack[self.index][1]][1] == 2:
                    return 4
                else:
                    return 0
            else:
                return 0

        if cmd == 'div' or cmd == 'rem':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][0] == 2 and self.type_stack[self.index][1] == 2 and self.stack[self.index][0] is not 0:
                    return 1
                elif self.type_stack[self.index][0] == 2 and self.type_stack[self.index][1] == 4 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 2 and self.stack[self.index][0] is not 0:
                    return 2
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 2 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 2 and self.bind_val[self.index][self.stack[self.index][0]][0] is not 0:
                    return 3
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 2 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 2 and self.bind_val[self.index][self.stack[self.index][0]][0] is not 0:
                    return 4
                else:
                    return 0
            else:
                return 0

        if cmd == 'neg':
            if len(self.stack[self.index]) > 0:
                if self.type_stack[self.index][0] == 2:
                    return 1
                elif self.type_stack[self.index][0] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 2:
                    return 2
                else:
                    return 0
            else:
                return 0
        if cmd == 'swap':
            if len(self.stack[self.index]) > 1:
                return 1
            else:
                return 0
        if cmd == 'cat':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][0] == 3 and self.type_stack[self.index][1] == 3:
                    return 1
                elif self.type_stack[self.index][0] == 3 and self.type_stack[self.index][1] == 4 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 3:
                    return 2
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 3 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 3:
                    return 3
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 3 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 3:
                    return 4
                else:
                    return 0
            else:
                return 0
        if cmd == 'and' or cmd == 'or':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][0] == 5 and self.type_stack[self.index][1] == 5:
                    return 1
                elif self.type_stack[self.index][0] == 5 and self.type_stack[self.index][1] == 4 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 5:
                    return 2
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 5 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 5:
                    return 3
                elif self.type_stack[self.index][0] == 4 and self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 5 and self.stack[self.index][1] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][1]][1] == 5:
                    return 4
                else:
                    return 0
            else:
                return 0
        if cmd == 'not':
            if len(self.stack[self.index]) > 0:
                if self.type_stack[self.index][0] == 5:
                    return 1
                elif self.type_stack[self.index][0] == 4 and self.stack[self.index][0] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][0]][1] == 5:
                    return 2
                else:
                    return 0
            else:
                return 0
        if cmd == 'bind':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][1] == 4:
                    if self.type_stack[self.index][0] == 2 or self.type_stack[self.index][0] == 3 or self.type_stack[self.index][0] == 5 or self.type_stack[self.index][0] == 6:
                        return 1
                    elif self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.bind_val[self.index]:
                        return 2
                    elif self.type_stack[self.index][1] == 4 and self.stack[self.index][0] in self.fun_val[self.index]:
                        return 3
                    else:
                        return 0
                else:
                    return 0
            else:
                return 0
        if cmd == 'if':
            if len(self.stack[self.index]) > 2:
                if self.type_stack[self.index][2] == 5:
                    return 1
                elif self.type_stack[self.index][2] == 4 and self.stack[self.index][2] in self.bind_val[self.index] and self.bind_val[self.index][self.stack[self.index][2]][1] == 5:
                    return 2
                else:
                    return 0
            else:
                return 0
        if cmd == 'call':
            if len(self.stack[self.index]) > 1:
                if self.type_stack[self.index][0] is not 1 and self.stack[self.index][1] in self.fun_val[self.index]:
                    return 1
                else:
                    return 0
            else:
                return 0

    def is_int(self, val):

        try:
            int(val)
        except ValueError:
            return False
        else:
            return True

    def is_string(self, val):

        if val[0] == '"' and val[-1] == '"':
            return True
        return False

    def is_name(self, val):

        if val[0].isalpha():
            return True
        elif val[0] == "_":
            return True
        return False

    def is_bool(self, val):

        if val == true or val == false:
            return True
        return False


if __name__ == '__main__':
    interpreter('/Users/changmingwang/Downloads/input.txt',
                '/Users/changmingwang/Downloads/output.txt')
