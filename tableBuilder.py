class Table():
    ''' A class to represent a Table '''

    def __init__(self, title = "", columnNames = [], listOfEntries = []):
        '''(Table, str, list of lists) -> NoneType
        This function builds a table with the given title, column names, and
        rows (list of entries).
        REQ: title is a string
        REQ: columnNames is the ordered column names of the table
        REQ: listOFEntries is the list of rows of the table, where each row is
             a list of str, that is ordered with respect to the column names.
        '''
        self.title = title
        self.columnNames = columnNames
        self.listOfEntries = listOfEntries

    def get_column(self, columnName):
        '''(Chart, str) -> list of str
        This function returns the column in the table that corresponds to the
        given columnName.
        REQ: columnName must belong in the columnNames of the table
        '''
        columnIndex = (self.columnNames).index(columnName)
        column = []
        for entry in self.listOfEntries:
            column.append(entry[columnIndex])
        return column

    def add_entry(self, entry):
        ''' (Table, list of str) -> NoneType
        This function will add a row to the table that represents the given
        entry
        REQ: the entry's ordered elements must correspond to the ordered
             column names of the Table
        '''
        (self.listOfEntries).append(entry)

    def build_table(self, filename):
        '''(Table, str) -> NoneType
        This function helps build a table easier using a text file that is in
        the format indicated below

        REQ: the filename must be the name of a file in the same folder as this
             .py file
        '''
        # ============ File Format ============
        # | People                            | <= Table Name
        # | Age, Name, Favourite Color        | <= Ordered Column Names
        # | -15, Bob, Red                     | <= entry 1 (ordered input)
        # | -20, Alexander, Green             | <= entry 2 (ordered input)
        # | -30, Cindy, Orange                | <= entry 3 (ordered input)
        # =====================================
        file = open(filename)

        entryID = 0
        for line in file:
            line = line.strip()
            if line[0] != "-":
                if line.find(',') != -1:
                    self.columnNames = ['ID'] + line.split(', ')
                else:
                    self.title = line
            else:
                entry = [str(entryID)] + line[1:].split(", ")
                self.add_entry(entry)
                entryID += 1
        file.close()

    def add_column(self, columnName, column):
        '''(Table, name, list of str) -> NoneType
        This function adds a column to the Table with the given columnName and
        column.
        REQ: the column must be ordered correspondingly to the entries
        '''
        (self.columnNames).append(columnName)

        i = 0
        for entry in self.listOfEntries:
            entry.append(column[i])
            i += 1

    def edit_element(self, entryID, columnName, edit):
        '''(Table, int, str, str) -> NoneType
        '''
        columnNum = (self.columnNames).index(columnName)
        (self.listOfEntries[entryID])[columnNum] = edit

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
        NUMBER_OF_COLUMNS = len(self.listOfEntries[0])
        CHART_WIDTH = 1

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
        print("| " + self.title + " "*(spaceCount) + " |" )
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

            # print divider if this entry is the temporary column name entry
            if entry == self.columnNames:
                print("-"*CHART_WIDTH)

        # 3. PRINT BOTTOM OF TABLE
        print("-"*CHART_WIDTH)

        # ** REMOVING TEMPORARY ENTRY **
        self.listOfEntries = self.listOfEntries[1:]