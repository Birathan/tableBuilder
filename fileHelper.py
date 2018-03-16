import listHelper

def add_line(filename, text, lineIndex):
    '''(str, str, int) -> NoneType
    This function takes a filename, text and lineIndex, and adds the text on a
    new line at lineIndex (where the first line has index 0).
    REQ: the filename must be the name of a file in the same folder as this
         .py file
    '''
    file = open(filename, 'r')

    # Get all lines of file as a list and add line to list at given index
    lines = file.readlines()
    lines = lines[:lineIndex] + [text+'\n'] + lines[lineIndex:]
    file.close()

    # Rewrite the file with updated set of lines
    file = open(filename, 'w')
    file.writelines(lines)
    file.close()

def read_table(filename):
    '''(str) -> Table
    This function helps build a table easier using a text file that is in
    the format indicated below and named [tableTitle + ' Table.txt']
    '''
    # ============ File Format ============
    # | People                            | <= Table Name
    # | Age, Name, Favourite Color        | <= Ordered Column Names
    # | -15, Bob, Red                     | <= entry 1 (ordered input)
    # | -20, Alexander, Green             | <= entry 2 (ordered input)
    # | -30, Cindy, Orange                | <= entry 3 (ordered input)
    # =====================================
    file = open(filename, 'r')
    lines = file.readlines()
    file.close()

    title = lines[0].strip()

    columnNames = lines[1].strip()
    columnNames=  columnNames.split(',')
    clean_list(columnNames)

    outputTable = Table(title, columnNames)

    for i in range(2, len(lines)):
        lines[i] = lines[i][1:].strip()
        lines[i] = lines[i].split(',')
        clean_list(lines[i])

        outputTable.add_entry(lines[i])

    return outputTable


def save_changes(table):
    '''(Table) -> NoneType
    This function updates the Table file to save the changes made to the
    Table.
    '''
    # 1. EMPTY FILE
    file = open(table.filename, 'w')
    file.close()

    # 2. REWRITE FILE
    add_line(table.filename, table.title, 0)
    add_line(table.filename, listHelper.list_to_str(table.columnNames), 1)
    for i in range(0, len(table.listOfEntries)):
        entry = listHelper.list_to_str(table.listOfEntries[i])
        add_line(table.filename, '-' + entry, i+2)
