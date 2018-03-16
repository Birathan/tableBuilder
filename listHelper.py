def list_to_str(lis):
    '''(list of str) -> str
    This function returns the string representation of the list, with elements
    of list seperated by ','.

    >>> list_to_str(['a', 'b', 'c'])
    'a, b, c'

    >>> list_to_str([' a', 'b ', ' c '])
    ' a, b ,  c '
    '''
    text = ''
    for element in lis:
        text += (element+', ')
    return text[:-2]


def clean_list(lis):
    '''(list of str) -> str
    This function formats the list so that each str is formatted of its leading
    and trailing spaces

    >>> a = ['a', 'b', 'c']
    >>> clean_list(a)
    >>> a
    ['a', 'b', 'c']

    >>> a = [' a', 'b ', ' c ']
    >>> clean_list(a)
    >>> a
    ['a', 'b', 'c']
    '''
    for i in range(0, len(lis)):
        if type(lis[i]) == str:
            lis[i] = lis[i].strip(' ')
