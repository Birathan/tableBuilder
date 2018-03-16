from tableBuilder import *
import os

def tab1():
    i = ""

    KEYWORDS = ["select", "from", "where"]
    try:
        while i != "exit":
            i = input("tableBuilder> ")
            i.strip()
            elements = i.split(" ")
            for i in range(0, len(elements)):
                if elements[i] == "select":
                    colnames = elements[i+1].split(',')
                elif elements[i] == "from":
                    tableNames = elements[i+1].split(',')
                    for i in range(0, len(tableNames)):
                        tableNames[i] = read_table(tableNames[i] + ' Table.txt')
                    while len(tableNames) > 1:
                        tableNames = [cross_product(tableNames[0],tableNames[1])] + tableNames[2:]
            tableNames[0].print_table()
    except:
        print('Syntax Error')

def execute_query(query):
    KEYWORDS = ["select", "from", "where"]
    query = delete_spaces(query)
    elements = split_on2(query, KEYWORDS)

    for i in range(0, len(elements)):
        if elements[i] == 'from':
            tableNames = elements[i+1].split(',')
            for a in range(0, len(tableNames)):
                tableNames[a] = read_table(tableNames[a] + ' Table.txt')
            while len(tableNames) > 1:
                tableNames = [cross_product(tableNames[0],tableNames[1])] + tableNames[2:]
            elements[i+1] = tableNames[0]
            new_table =tableNames[0]

    for i in range(0, len(elements)):
        if elements[i] == 'select':
            colnames = elements[i+1]
            table = elements[i+3]
            if colnames == '*':
                colnames = list_to_str(table.columnNames)
            new_table = projection(table, colnames)

    for i in range(0, len(elements)):
        if type(elements) == str and elements[i].count('(') != 0:
            elements[i] = execute_query(elements)


    new_table.print_table()

def execute_query2(query):
    KEYWORDS = ["select", "from", "where"]
    query = delete_spaces(query)
    elements = split_on2(query, KEYWORDS)

    # BASIC QUERIES [where ( , , ) is a list, and ( ... ) is a potential sub-query]
    # (...) UNION (...)
    # (...) EXCEPT (...)
    # (...) INTERSECT (...)
    # SELECT ( , , ) FROM (...)
    # SELECT ( , , ) FROM (...) WHERE ( , , )
    #

    # if there is a select keyword there must be a from
    if len(elements) == 1:
        elements[0].print_table()
    else:
        for i in range(0, len(elements)):
            if elements[i].count('(') != 0:
                elements[i] = execute_query2(elements[i])

        if elements[0] == 'select':
            colNames = elements[1]
            tableNames = elements[3].split(',')
            for a in range(0, len(tableNames)):
                tableNames[a] = read_table(tableNames[a] + ' Table.txt')
            while len(tableNames) > 1:
                tableNames = [cross_product(tableNames[0],tableNames[1])] + tableNames[2:]
            newTable = tableNames[0]

            if elements[5] == 'where':
                #apply conditions
                a= 1

            projection(newTable, colnames)



def clean_list(lis):
    '''(list of str) -> str
    This function formats the list so that each str is formatted of its leading
    and trailing spaces
    '''
    for i in range(0, len(lis)):
        if type(lis[i]) == str:
            lis[i] = lis[i].strip()

def delete_spaces(string):
    new_string = ''
    for char in string:
        if char != ' ':
            new_string += char
    return new_string


# ======================== 3. TABLE TO TABLE OPERATION ========================
def cross_product(table1, table2):
    entries1 = table1.listOfEntries[:]
    entries2 = table2.listOfEntries[:]
    cols1 = table1.columnNames[:]
    cols2 = table2.columnNames[:]

    for i in range(0, len(cols1)):
        if cols2.count(cols1[i]) != 0:
            index = cols2.index(cols1[i])
            cols2[index] = table2.title+'.'+cols1[i]
            cols1[i] = table1.title+'.'+cols1[i]

    entries3 = []

    for entry1 in entries1:
        for entry2 in entries2:
            entries3.append(entry1 + entry2)

    cols1.extend(cols2)

    table3 = Table("temp", cols1, entries3)
    return table3

def projection(table, colnames):
    listOfEntries =[]
    collis = []

    colnames = colnames.split(',')
    clean_list(colnames)

    for colname in colnames:
        collis.append(table.get_column(colname))

    for i in range(0, len(table.listOfEntries)):
        entry = []
        for col in collis:
            entry.append(col[i])
        listOfEntries.append(entry)
    tableOutput = Table("temp", colnames, listOfEntries)
    return tableOutput

def get_bracket_pair_index(current_bracket_index, text):
    brackets = []
    text = text[current_bracket_index:]
    for i in range(0, len(text)):
        if text[i] == '(':
            brackets.append('(')
        elif text[i] == ')':
            brackets = brackets[:-1]
        if len(brackets) == 0:
            return i + current_bracket_index

def list_to_str(lis):
    '''(list of str) -> str
    This function returns the string representation of the list, with elements
    of list seperated by ','
    '''
    text = ''
    for element in lis:
        text += (element+', ')
    return text[:-2]


def split_on(string, specialChars):
    '''
    splits string at each char while keeping priority in mind with brackets
    '''
    elements = []
    brackets = []
    word = ''
    for char in string:

        if char == '(':
            brackets.append('(')
        elif char == ')':
            brackets = brackets[:-1]

        if (char not in specialChars) or (len(brackets) != 0):
            word += char

        if (char in specialChars) and len(brackets) == 0:
            elements.append(word)
            elements.append(char)
            word = ''
    # last element that gets left out
    elements.append(word)

    return elements

def split_on2(string, strings):
    elements = []
    brackets = []
    word = ''
    for char in string:
        if char == '(':
            if len(brackets) == 0:
                if word != '':
                    elements.append(word)
                word = '('
            brackets.append('(')
        elif char == ')':
            brackets = brackets[:-1]
            if len(brackets) == 0:
                elements.append(word + ')')
                word = ''
        else:
            word += char


        for special in strings:
            if (special in word) and (len(brackets) == 0):
                index = word.index(special)
                if index != 0:
                    elements.append(word[:index])
                elements.append(special)
                word = ''

    # last element that gets left out
    if word != '':
        elements.append(word)

    return elements
