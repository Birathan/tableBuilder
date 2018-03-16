import fileHelper
import listHelper

class Table():
    ''' A class to represent a Table '''

    def __init__(self, title, columnNames, listOfEntries=[]):
        '''(Table, str, list of str, list of str) -> NoneType
        This function builds a table with the given title, column names, and
        rows (list of entries).
        REQ: title is a string
        REQ: columnNames is a string with the ordered column names of the
             table, seperated by ','.
        REQ: listOFEntries is the l ist of rows of the table, where each row is
             a string seperated with commas (ordered with respect to
             the column names)
        '''
        # Setup Table variables
        self.title = title
        self.columnNames = columnNames
        self.listOfEntries = listOfEntries[:]
        self.filename = title + ' Table.txt'
        fileHelper.save_changes(self)

    def get_column(self, colname):
        index = (self.columnNames).index(colname)
        col = []
        for entry in self.listOfEntries:
            col.append(entry[index])
        return col

    def get_entries_under_condition(condition):
        operators = ['<', '>', '=', '-', '+', '/', '*', 'and', 'or']
        elements = condition.split(' ')
        # int only operations

        # int or other operations

    def add_entry(self, entry):
        ''' (Table, list of str) -> NoneType
        This function will add a row to the table that represents the given
        entry
        REQ: the entry's ordered elements (seperated by ',') must correspond
             to the ordered column names of the Table
        '''
        (self.listOfEntries).append(entry)
        fileHelper.save_changes(self)

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
