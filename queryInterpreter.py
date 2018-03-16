def split_on(expression, operations):
    '''(str, list of str) -> list of str
    Splits the expression into its components relative to the operations in
    one level.
    '''
    elements = []
    brackets = []
    word = ''
    for char in expression:
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


        for special in operations:
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
