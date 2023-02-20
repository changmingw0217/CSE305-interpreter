
import copy
def interpreter(input_f, output):
    list_stack = [[]]
    list_type_stack = [[]]
    list_bind_dict = [{}]
    let_c = 0
    input_file = open(input_f, 'r')
    output_file = open(output, 'w')
    for line in input_file:
        if "quit" in line:
            break
        if "let" in line[0:3]:
            let_c += 1
            list_stack.append([])
            list_type_stack.append([])
            val = copy.deepcopy(list_bind_dict[-1])
            list_bind_dict.append(val)
        elif 'end' in line[0:3]:
            let_c -= 1
            val = list_stack[-1].pop()
            t = list_type_stack[-1].pop()
            list_stack.pop()
            list_type_stack.pop()
            list_stack[-1].append(val)
            list_type_stack[-1].append(t)
            list_bind_dict.pop()
        else:
            checkline(line, list_stack, list_type_stack, list_bind_dict,let_c)

    list_stack[0].reverse()

    for item in list_stack[0]:
        output_file.write(str(item) + '\n')


def checkline(string, list_stack, list_type_stack, list_bind_dict,let_c):

    string = string[:-1]
    if 'push' in string[0:4]:
        string = string[5:]
        Push(string, list_stack, list_type_stack,let_c)
    elif 'pop' in string[0:3]:
        Pop(list_stack, list_type_stack,let_c)
    elif 'neg' in string[0:3]:
        Neg(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'add' in string[0:3]:
        Add(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'sub' in string[0:3]:
        Sub(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'mul' in string[0:3]:
        Mul(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'div' in string[0:3]:
        Div(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'rem' in string[0:3]:
        Rem(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'swap' in string[0:4]:
        Swap(list_stack, list_type_stack,let_c)
    elif 'cat' in string[0:3]:
        Cat(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'and' in string[0:3]:
        And(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'or' in string[0:2]:
        Or(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'not' in string[0:3]:
        Not(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'equal' in string[0:5]:
        Equel(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'lessThan' in string[0:8]:
        LessThan(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'bind' in string[0:4]:
        Bind(list_stack, list_type_stack, list_bind_dict,let_c)
    elif 'if' in string[0:2]:
        If(list_stack, list_type_stack, list_bind_dict,let_c)
    else:
        list_stack[let_c].append(":error:")
        list_type_stack[let_c].append(4)


def Push(string, stack, type_stack,let_c):
    if check_num(string):
        string = int(string)
        stack[let_c].append(string)
        type_stack[let_c].append(0)  # 0 means num
    elif string[0] == '"' and string[-1] == '"':
        string = string[1:]
        string = string[:-1]
        stack[let_c].append(string)
        type_stack[let_c].append(1)  # 1 means stringing
    elif string == ':error:':
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)  # 4 means error
    elif string[0] == ':' and string[-1] == ':':
        stack[let_c].append(string)
        type_stack[let_c].append(2)  # 2 means bool
    elif string[0].isalpha():
        stack[let_c].append(string)
        type_stack[let_c].append(3)  # 3 means name
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)  # 4 means error


def Pop(stack,type_stack,let_c):

    if len(stack[let_c]) > 0:
        stack[let_c].pop()
        type_stack[let_c].pop()
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Neg(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) > 0:
        if type_stack[let_c][-1] == 0:
            stack[let_c][-1] = -stack[let_c][-1]
        elif type_stack[let_c][-1] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    val = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(-bind_dict[let_c][val][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Add(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 + val1)
            type_stack[let_c].append(0)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 + bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] + val1)
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] + bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Sub(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 - val1)
            type_stack[let_c].append(0)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 - bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] - val1)
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] - bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Mul(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 * val1)
            type_stack[let_c].append(0)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 * bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] * val1)
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] * bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)

def Div(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0 and stack[let_c][-1] != 0:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 // val1)
            type_stack[let_c].append(0)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-1]][0] != 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 // bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3 and stack[let_c][-1] != 0:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] // val1)
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0 and bind_dict[let_c][stack[let_c][-1]][0] != 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] // bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Rem(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0 and stack[let_c][-1] != 0:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 % val1)
            type_stack[let_c].append(0)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-1]][0] != 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 % bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3 and stack[let_c][-1] != 0:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] % val1)
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0 and bind_dict[let_c][stack[let_c][-1]][0] != 0:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] % bind_dict[let_c][val1][0])
                    type_stack[let_c].append(0)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Swap(stack,type_stack,let_c):

    if len(stack[let_c]) >= 2:
        stack[let_c][-1], stack[let_c][-2] = stack[let_c][-2], stack[let_c][-1]
        type_stack[let_c][-1], type_stack[let_c][-2] = type_stack[let_c][-2], type_stack[let_c][-1]
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Cat(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 1 and type_stack[let_c][-2] == 1:
            val1 = stack[let_c].pop()
            type_stack[let_c].pop()
            val2 = stack[let_c].pop()
            type_stack[let_c].pop()
            stack[let_c].append(val2 + val1)
            type_stack[let_c].append(1)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 1:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 1:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(val2 + bind_dict[let_c][val1][0])
                    type_stack[let_c].append(1)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 1 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 1:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] + val1)
                    type_stack[let_c].append(1)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 1 and bind_dict[let_c][stack[let_c][-2]][1] == 1:
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(bind_dict[let_c][val2][0] + bind_dict[let_c][val1][0])
                    type_stack[let_c].append(1)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def And(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 2 and type_stack[let_c][-2] == 2:
            if stack[let_c][-1] == ":true:" and stack[let_c][-2] == ":true:":
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":true:")
                type_stack[let_c].append(2)
            else:
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":false:")
                type_stack[let_c].append(2)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 2:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-1]][0] == ":true:" and stack[let_c][-2] == ":true:":
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 2 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 2:
                    if stack[let_c][-1] == ":true:" and bind_dict[let_c][stack[let_c][-2]][0] == ":true:":
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 2 and bind_dict[let_c][stack[let_c][-2]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-1]][0] == ":true:" and bind_dict[let_c][stack[let_c][-2]][0] == ":true:":
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Or(stack, type_stack, bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 2 and type_stack[let_c][-2] == 2:
            if stack[let_c][-1] == ":true:" or stack[let_c][-2] == ":true:":
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":true:")
                type_stack[let_c].append(2)
            else:
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":false:")
                type_stack[let_c].append(2)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 2:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-1]][0] == ":true:" or stack[let_c][-2] == ":true:":
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 2 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-2]][0] == ":true:" or stack[let_c][-1] == ":true:":
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 2 and bind_dict[let_c][stack[let_c][-2]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-1]][0] == ":true:" or bind_dict[let_c][stack[let_c][-2]][0] == ":true:":
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)

        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Not(stack, type_stack, bind_dict,let_c):

    if not len(stack[let_c]) == 0:
        if type_stack[let_c][-1] == 2:
            if stack[let_c][-1] == ":true:":
                stack[let_c][-1] = ":false:"
            else:
                stack[let_c][-1] = ":true:"
        elif type_stack[let_c][-1] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-1]][0] == ":true:":
                        stack[let_c][-1] = ":false:"
                    else:
                        stack[let_c][-1] = ":true:"
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Equel(stack, type_stack, bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0:
            if stack[let_c][-1] == stack[let_c][-2]:
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":true:")
                type_stack[let_c].append(2)
            else:
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":false:")
                type_stack[let_c].append(2)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-1]][0] == stack[let_c][-2]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-2]][0] == stack[let_c][-1]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-1]][0] == bind_dict[let_c][stack[let_c][-2]][0]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def LessThan(stack, type_stack, bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 0:
            if stack[let_c][-1] > stack[let_c][-2]:
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":true:")
                type_stack[let_c].append(2)
            else:
                stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(":false:")
                type_stack[let_c].append(2)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 0:
            if bind_dict[let_c].__contains__(stack[let_c][-1]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-1]][0] > stack[let_c][-2]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 0 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-2]][0] < stack[let_c][-1]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        elif type_stack[let_c][-1] == 3 and type_stack[let_c][-2] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-1]) and bind_dict[let_c].__contains__(stack[let_c][-2]):
                if bind_dict[let_c][stack[let_c][-1]][1] == 0 and bind_dict[let_c][stack[let_c][-2]][1] == 0:
                    if bind_dict[let_c][stack[let_c][-1]][0] > bind_dict[let_c][stack[let_c][-2]][0]:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":true:")
                        type_stack[let_c].append(2)
                    else:
                        stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(":false:")
                        type_stack[let_c].append(2)
                else:
                    stack[let_c].append(":error:")
                    type_stack.append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def Bind(stack,type_stack,bind_dict,let_c):

    if len(stack[let_c]) >= 2:
        if type_stack[let_c][-2] == 3 and type_stack[let_c][-1] != 4:
            if type_stack[let_c][-1] != 3 and type_stack[let_c][-1] != 5:
                val1 = stack[let_c].pop()
                t = type_stack[let_c].pop()
                val2 = stack[let_c].pop()
                type_stack[let_c].pop()
                bind_dict[let_c][val2] = [val1,t]
                stack[let_c].append(":unit:")
                type_stack[let_c].append(5)
            elif type_stack[let_c][-1] == 3:
                if bind_dict[let_c].__contains__(stack[let_c][-1]):
                    val1 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    val2 = stack[let_c].pop()
                    type_stack[let_c].pop()
                    bind_dict[let_c][val2] = bind_dict[let_c][val1]
                    stack[let_c].append(":unit:")
                    type_stack[let_c].append(5)
                else:
                    stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].pop()
                    type_stack[let_c].pop()
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            elif type_stack[let_c][-1] == 5:
                stack[let_c].pop()
                type_stack[let_c].pop()
                val = stack[let_c].pop()
                type_stack[let_c].pop()
                bind_dict[let_c][val] = [":unit:", 5]
                stack[let_c].append(":unit:")
                type_stack[let_c].append(5)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)


def If(stack, type_stack, bind_dict,let_c):

    if len(stack[let_c]) >= 3:
        if type_stack[let_c][-3] == 2:
            if stack[let_c][-3] == ":true:":
                stack[let_c].pop()
                type_stack[let_c].pop()
                val = stack[let_c].pop()
                t = type_stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(val)
                type_stack[let_c].append(t)
            else:
                val = stack[let_c].pop()
                t = type_stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].pop()
                type_stack[let_c].pop()
                stack[let_c].append(val)
                type_stack[let_c].append(t)
        elif type_stack[let_c][-3] == 3:
            if bind_dict[let_c].__contains__(stack[let_c][-3]):
                if bind_dict[let_c][stack[let_c][-3]][1] == 2:
                    if bind_dict[let_c][stack[let_c][-3]][0] == ":true:":
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        val = stack[let_c].pop()
                        t = type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(val)
                        type_stack[let_c].append(t)
                    else:
                        val = stack[let_c].pop()
                        t = type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].pop()
                        type_stack[let_c].pop()
                        stack[let_c].append(val)
                        type_stack[let_c].append(t)
                else:
                    stack[let_c].append(":error:")
                    type_stack[let_c].append(4)
            else:
                stack[let_c].append(":error:")
                type_stack[let_c].append(4)
        else:
            stack[let_c].append(":error:")
            type_stack[let_c].append(4)
    else:
        stack[let_c].append(":error:")
        type_stack[let_c].append(4)



def check_num(string):
    flag = False
    for char in range(len(string)):
        if string[char] == '0' or string[char] == '1' or string[char] == '2' or string[char] == '3' or string[
            char] == '4' or string[char] == '5' or string[char] == '6' or string[char] == '7' or string[char] == '8' or \
                string[char] == '9' or string[char] == '-':
            flag = True
        else:
            flag = False
            break
    return flag

