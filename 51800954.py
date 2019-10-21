import itertools

def readInfix(filename):
    with open(filename) as f:
        Infix = f.readlines()
    return Infix[0]


##########################################Student do these 2 function
stack = []


def Infix2Postfix(Infix):
    Postfix = []
    for i in Infix:
        if isOperator(i) == -2:
            Postfix.append(i)
        else:
            if isOperator(i) == 2:  # tra ve 0 co nghia do la dau (
                stack.append(i)
            elif isOperator(i) == 3:  # tra ve -1 co nghia do la dau )
                while (isEmpty(stack) == False) and stack[-1] != '(':
                    Postfix.append(stack.pop())
                stack.pop()
            else:
                while (isEmpty(stack) == False) and (getPriority(i) > getPriority(stack[-1])):
                    Postfix.append(stack.pop())
                stack.append(i)
    while (stack):
        Postfix.append(stack.pop())
    return Postfix


def Postfix2Truthtable(Postfix):
    listDic = {}

    variableTemp = [i for i in Postfix if isOperator(i) == -2]

    variableTemp = set(variableTemp)

    variable = [i for i in variableTemp]
    variable.sort()

    for v in range(len(variable)):
        listDic[variable[v]] = v

    table1 = list(itertools.product([False, True], repeat=len(variable)))
    Truthtable = []

    for i in table1:
        listTemp = []
        for j in i:
            listTemp.append(j)
        Truthtable.append(listTemp)

    for i in range(2 ** len(variable)):
        stack = []
        for j in Postfix:
            if isOperator(j) == -2:
                stack.append(j)
            elif j == '&':
                if isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == -2:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] & Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == 0:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] & stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-1]) == -2 and isOperator(stack[-2]) == 0:
                    stack[-2] = stack[-2] & Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                else:
                    stack[-2] = stack[-2] & stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
            elif j == '~':
                if isOperator(stack[-1]) == -2:
                    stack[-1] = not Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-1])
                elif isOperator(stack[-1]) == 0:
                    stack[-1] = not stack[-1]
                    Truthtable[i].append(stack[-1])
            elif j == '|':
                if isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == -2:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] or Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == 0:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] or stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-1]) == -2 and isOperator(stack[-2]) == 0:
                    stack[-2] = stack[-2] or Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                else:
                    stack[-2] = stack[-2] or stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
            elif j == '>':
                if isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == -2:
                    stack[-2] = implies(Truthtable[i][listDic[stack[-2]]], Truthtable[i][listDic[stack[-1]]])
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == 0:
                    stack[-2] = implies(Truthtable[i][listDic[stack[-2]]], stack[-1])
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-1]) == -2 and isOperator(stack[-2]) == 0:
                    stack[-2] = implies(stack[-2], Truthtable[i][listDic[stack[-1]]])
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                else:
                    stack[-2] = implies(stack[-2], stack[-1])
                    Truthtable[i].append(stack[-2])
                    stack.pop()
            else:
                if isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == -2:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] == Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-2]) == -2 and isOperator(stack[-1]) == 0:
                    stack[-2] = Truthtable[i][listDic[stack[-2]]] == stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                elif isOperator(stack[-1]) == -2 and isOperator(stack[-2]) == 0:
                    stack[-2] = stack[-2] == Truthtable[i][listDic[stack[-1]]]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
                else:
                    stack[-2] = stack[-2] == stack[-1]
                    Truthtable[i].append(stack[-2])
                    stack.pop()
    for i in range(len(Truthtable)):
        Truthtable[i] = tuple(Truthtable[i])
    return Truthtable

def implies(a, b):
    if a:
        return b
    else:
        return True


def getPriority(operator):
    listPriority = {'~': 1, '&': 2, '|': 3, '>': 4, '=': 5}
    try:
        result = listPriority[operator]
        return result
    except KeyError:
        return 6


def isOperator(char):
    listContainer = {1: 0, 0: 0, '(': 2, ')': 3, '~': 1, '&': 1, '|': 1, '>': 1, '=': 1}
    ## quy uoc 1 la toan tu va 0 la cac dau mo dong ngoac
    try:
        result = listContainer[char]
        return result
    except KeyError:
        return -2  # tra ve -1 voi quy uoc doi so truyen vao la chu hoac khong phai la toan tu


def isEmpty(stack):
    return True if not (stack) else False


##########################################End student part
def writeTruthtable(table):
    import sys
    outfile = sys.argv[0]
    outfile = outfile[0:-2]
    outfile += "txt"
    with open(outfile, 'w') as f:
        for lines in table:
            for item in lines:
                f.write("%s\t" % item)
            f.write("\n")
    f.close()


def main():
    Infix = readInfix("Logicexpression.txt")
    Postfix = Infix2Postfix(Infix)
    Truthtable = Postfix2Truthtable(Postfix)
    writeTruthtable(Truthtable)
main()
