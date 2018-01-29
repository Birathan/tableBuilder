import os


class Table():
    ''' A class to represent a Table '''

    def __init__(self, title, columnNames, listOfEntries=[]):
        '''(Table, str, str, list of str) -> NoneType
        This function builds a table with the given title, column names, and
        rows (list of entries).
        REQ: title is a string
        REQ: columnNames is a string with the ordered column names of the
             table, seperated by ','.
        REQ: listOFEntries is the list of rows of the table, where each row is
             a string seperated with commas (ordered with respect to
             the column names)
        '''
        # columnNames can be input either as [list of str] or [str seperated
        # by ',']
        columnNames = ['ID'] + columnNames.split(',')
        clean_list(columnNames)

        # Setup Table variables
        self.title = title
        self.columnNames = columnNames
        self.listOfEntries = listOfEntries
        self.filename = title + ' Table.txt'
        self.nextEntryID = 0

        # Give option to Load or Overwrite existing Table file
        if(os.path.isfile(self.filename)):
            response = input("Press 'o' to Overwrite already existing table,"
                             "or 'l' to Load the existing table. O/L : ")
            if(response == 'o'):
                self.save_changes()
            else:
                self.read_table()
        else:
            self.save_changes()

    # ********************** NEW FUNCTION FOR SAVING **************************
    def save_changes(self):
        '''(Table) -> NoneType
        This function updates the Table file to save the changes made to the
        Table.
        '''
        # 1. EMPTY FILE
        file = open(self.filename, 'w')
        file.close()

        # 2. REWRITE FILE
        add_line(self.filename, self.title, 0)
        add_line(self.filename, list_to_str(self.columnNames), 1)
        for i in range(0, len(self.listOfEntries)):
            entry = list_to_str(self.listOfEntries[i][1:])
            add_line(self.filename, '-' + entry, i+2)

    def read_table(self):
        '''(Table) -> NoneType
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
        file = open(self.filename)

        for line in file:
            line = line.strip()
            if line[0] != "-":
                if line.find(',') == -1:
                    self.title = line
                else:
                    self.columnNames = line.split(',')
                    clean_list(self.columnNames)
            else:
                self.add_entry(line[1:])
        file.close()

    def add_entry(self, entry):
        ''' (Table, str) -> NoneType
        This function will add a row to the table that represents the given
        entry
        REQ: the entry's ordered elements (seperated by ',') must correspond
             to the ordered column names of the Table
        '''
        # Get entry as list of elements
        entry = [str(self.nextEntryID)] + entry.split(',')
        clean_list(entry)
        self.nextEntryID += 1

        # Add entries to the list of entries
        (self.listOfEntries).append(entry)

        # Save changes to a file
        self.save_changes()

    def print_table(self):
        '''(Table) -> NoneType
        This function prints a string representation of the Table as follows:
                   ---------------------------------------------------
                   | Table name                                      |
                   ---------------------------------------------------
                   | ID  | column name 1 |    ...    | column name m |
                   ---------------------------------------------------
        entry 1 -> | 0   |               |    ...    |               |
        entry 2 -> | 1   |               |    ...    |               |
        entry 3 -> | 2   |               |    ...    |               |
        entry 4 -> | 3   |               |    ...    |               |
            |      |     |       |       |    ...    |       |       |
            |      |     |       |       |    ...    |       |       |
            V      |     |       V       |    ...    |       V       |
        entry n -> | n-1 |               |    ...    |               |
                   ---------------------------------------------------
        '''
        # VARIABLE SETUP
        COLUMN_WIDTHS = []
        SPACE_COUNTS = []
        NUMBER_OF_COLUMNS = len(self.columnNames)
        CHART_WIDTH = 1

        # Starting values for format
        for i in range(0, NUMBER_OF_COLUMNS):
            columnNameLength = len(self.columnNames[i])
            COLUMN_WIDTHS.append(columnNameLength)
            SPACE_COUNTS.append(0)

        # GET FORMATTING INFORMATION
        for entry in self.listOfEntries:
            for i in range(0, len(entry)):
                # an element is an attribute/element of the entry/row
                # width is the full char length of column that does not include
                # the seperator " | "
                element_width = len(entry[i])
                if element_width > COLUMN_WIDTHS[i]:
                    COLUMN_WIDTHS[i] = element_width

        # Get width of Chart
        for i in range(0, NUMBER_OF_COLUMNS):
            CHART_WIDTH += COLUMN_WIDTHS[i] + 3

        # 1. PRINT TOP PART OF TABLE
        print("-"*CHART_WIDTH)
        spaceCount = CHART_WIDTH-len(self.title)-4
        print("| " + self.title + " "*(spaceCount) + " |")
        print("-"*CHART_WIDTH)

        # ** TEMPORARY ENTRY FOR SIMPLICITY **
        # add column names as a temporary entry
        self.listOfEntries = [self.columnNames] + self.listOfEntries

        # 2. PRINT ENTRY BY ENTRY
        for entry in self.listOfEntries:

            # 2A. GET SPACE COUNTS BEFORE EACH SEPERATOR " | "
            for i in range(0, NUMBER_OF_COLUMNS):
                entryElement = entry[i]
                SPACE_COUNTS[i] = COLUMN_WIDTHS[i] - len(entryElement)

            # 2B. PRINT ENTRY FORMATTED WITH SEPERATORS " | "
            output = "| "
            for i in range(0, NUMBER_OF_COLUMNS):
                output += entry[i] + " "*SPACE_COUNTS[i] + " | "
            print(output)

            # print divider if this entry is the temporary entry of column
            # ames
            if entry == self.columnNames:
                print("-"*CHART_WIDTH)

        # 3. PRINT BOTTOM OF TABLE
        print("-"*CHART_WIDTH)

        # ** REMOVING TEMPORARY ENTRY **
        self.listOfEntries = self.listOfEntries[1:]


# ********************** NEW FUNCTIONS FOR SAVING TO FILES ********************

# ======================== 1. FILE EDITING FUNCTIONS ==========================
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


# ================= 2. STRING REPRESENTATION HELPER FUNCTIONS =================
def list_to_str(lis):
    '''(list of str) -> str
    This function returns the string representation of the list, with elements
    of list seperated by ','
    '''
    text = ''
    for element in lis:
        text += (element+', ')
    return text[:-2]


def clean_list(lis):
    '''(list of str) -> str
    This function formats the list so that each str is formatted of its leading
    and trailing spaces
    '''
    for i in range(0, len(lis)):
        if type(lis[i]) == str:
            lis[i] = lis[i].strip()
