import math
class Cell:
    ''' Represents a single cell of a map.  Cells know their neighbors
        and know if they are linked (connected) to each.  Cells have
        four potential neighbors, in NSEW directions.
    '''  
    def __init__(self, row, column):
        assert row >= 0
        assert column >= 0
        self.row = row
        self.column = column
        self.links = {}
        self.north = None
        self.south = None
        self.east  = None
        self.west  = None
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None
        
    def link(self, cell, bidirectional=True):
        ''' Carve a connection to another cell (i.e. the maze connects them)'''
        assert isinstance(cell, Cell)
        self.links[cell] = True
        if bidirectional:
            cell.link(self, bidirectional=False)
        
    def unlink(self, cell, bidirectional=True):
        ''' Remove a connection to another cell (i.e. the maze 
            does not connect the two cells)
            
            Argument bidirectional is here so that I can call unlink on either
            of the two cells and both will be unlinked.
        '''
        assert isinstance(cell, Cell)
        del self.links[cell]
        if bidirectional:
            cell.unlink(self, bidirectional=False)
            
    def is_linked(self, cell):
        ''' Test if this cell is connected to another cell.
            
            Returns: True or False
        '''
        assert isinstance(cell, Cell)
        if cell in self.links:
            return True
        return False
        
    def all_links(self):
        ''' Return a list of all cells that we are connected to.'''
        list = []
        for key,value in self.links.items():
            assert isinstance(key, Cell)
            list.append(key)
        return list
        
    def link_count(self):
        ''' Return the number of cells that we are connected to.'''
        list = self.all_links()
        count = len(list)
        return count
        
    def neighbors(self):
        ''' Return a list of all geographical neighboring cells, regardless
            of any connections.  Only returns actual cells, never a None.
        '''
        neighbor_list = []
        list = [self.north, self.south, self.east, self.west,self.northeast,self.northwest,self.southeast, self.southwest]
        for i in list:
             if i is not None:
                 neighbor_list.append(i)
        return neighbor_list

    def quater_neighbors(self,cell):
        assert isinstance(cell,Cell)
        dx = cell.column - self.column
        dy = cell.row - self.row
        if dy>0 and dx>0:
            return [self.southeast,self.east,self.south]
        elif dy<0 and dx>0:
            return [self.northeast,self.east,self.north]
        elif dy>0 and dx<0:
            return [self.southwest,self.west,self.south]
        elif dy<0 and dx<0:
            return [self.northwest,self.west,self.north]
        elif dy == 0 and dx>0:
            return [self.east]
        elif dy == 0 and dx<0:
            return [self.west]
        elif dy>0 and dx == 0:
            return [self.south]
        elif dy<0 and dx == 0:
            return [self.north]
        else:
            return None

    def octile_distance(self,cell):
        assert isinstance(cell, Cell)
        dx = abs(self.column - cell.column)
        dy = abs(self.row - cell.row)
        return math.sqrt(2) * min(dx, dy) + abs(dx - dy)

    def move(self,d,num):
        current = self
        if d == 'E':
            for i in range(num):
                current = current.east
                if not current:
                    return None
            return current
        if d == 'SE':
            for i in range(num):
                current = current.southeast
                if not current:
                    return None
            return current
        if d == 'S':
            for i in range(num):
                current = current.south
                if not current:
                    return None
            return current
        if d == 'SW':
            for i in range(num):
                current = current.southwest
                if not current:
                    return None
            return current
        if d == 'W':
            for i in range(num):
                current = current.west
                if not current:
                    return None
            return current
        if d == 'NW':
            for i in range(num):
                current = current.northwest
                if not current:
                    return None
            return current
        if d == 'N':
            for i in range(num):
                current = current.north
                if not current:
                    return None
            return current
        if d == 'NE':
            for i in range(num):
                current = current.northeast
                if not current:
                    return None
            return current

    def __lt__(self, other):
        ''' Needed for heaps when priority/distance is the same.'''
        if not self.row == other.row:
            return self.row < other.row
        else:
            return self.column < other.column  
                
    def __str__(self):
        return f'Cell at {self.row}, {self.column}'
        
class Grid:
    def __init__(self,num_rows,num_columns):
        assert num_rows > 0
        assert num_columns > 0
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.grid = self.create_cells()
        self.connect_cells()

    def create_cells(self):
        ''' Call the cells into being.  Keep track of them in a list
            for each row and a list of all rows (i.e. a 2d list-of-lists).
            
            Do not connect the cells, as their neighbors may not yet have
            been created.
        '''
        list = []
        for row_index in range(self.num_rows):
            row = []
            for col_index in range(self.num_columns):
                cell = Cell(row_index,col_index)
                row.append(cell)
            list.append(row)

        return list
    
    def connect_cells(self):
        ''' Now that all the cells have been created, connect them to 
            each other. 
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                north_index = row-1 if row-1>=0 else None
                south_index = row+1 if row+1<= self.num_rows-1 else None
                west_index = col-1 if col-1>=0 else None
                east_index = col+1 if col+1 <= self.num_columns-1 else None
                north_east_row = north_west_row= row-1 if row-1>=0 else None
                south_east_row = south_west_row= row+1 if row+1< self.num_rows else None
                north_east_col = south_east_col = col+1 if col+1< self.num_columns else None
                north_west_col = south_west_col = col-1 if col-1 >= 0 else None

                if north_index is not None:
                    self.grid[row][col].north = self.grid[north_index][col]
                if south_index is not None:
                    self.grid[row][col].south = self.grid[south_index][col]
                if west_index is not None:
                    self.grid[row][col].west = self.grid[row][west_index]
                if east_index is not None:
                    self.grid[row][col].east = self.grid[row][east_index]
                if north_east_row is not None and north_east_col is not None:
                    self.grid[row][col].northeast = self.grid[north_east_row][north_east_col]
                if north_west_row is not None and north_west_col is not None:
                    self.grid[row][col].northwest = self.grid[north_west_row][north_west_col]
                if south_east_row is not None and south_east_col is not None:
                    self.grid[row][col].southeast = self.grid[south_east_row][south_east_col]
                if south_west_row is not None and south_west_col is not None:
                    self.grid[row][col].southwest = self.grid[south_west_row][south_west_col]
                    

        
    def cell_at(self, row, column):
        ''' Retrieve the cell at a particular row/column index.'''
        return self.grid[row][column]
        
    def deadends(self):
        ''' Return a list of all cells that are deadends (i.e. only link to
            one other cell).
        '''
        deadends = []
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                num_linked = self.grid[row][col].link_count()
                if num_linked==1:
                    deadends.append(self.grid[row][col])
        return deadends
                            
    def each_cell(self):
        ''' A generator.  Each time it is called, it will return one of 
            the cells in the grid.
        '''
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                c = self.cell_at(row, col)
                yield c
                
    def each_row(self):
        ''' A row is a list of cells.'''
        for row in self.grid:
            yield row
        
    def size(self):
        ''' How many cells are in the grid? '''
        return self.num_rows* self.num_columns

        
    def set_markup(self, markup):
        ''' Warning: this is a hack.
            Keep track of a markup, for use in representing the grid
            as a string.  It is used in the __str__ function and probably
            shouldn't be used elsewhere.
        '''
        self.markup = markup
        
    def __str__(self):
        ret_val = '+' + '---+' * self.num_columns + '\n'
        for row in self.grid:
            ret_val += '|'
            for cell in row:
                cell_value = self.markup[cell]
                ret_val += '{:^3s}'.format(str(cell_value))
                if not cell.east:
                    ret_val += '|'
                elif cell.east.is_linked(cell):
                    ret_val += ' '
                else:
                    ret_val += '|'
            ret_val += '\n+'
            for cell in row:
                if not cell.south:
                    ret_val += '---+'
                elif cell.south.is_linked(cell):
                    ret_val += '   +'
                else:
                    ret_val += '---+'
            ret_val += '\n'
        return ret_val
    
class Markup:
    ''' A Markup is a way to add data to a grid.  It is associated with
        a particular grid.
        
        In this case, each cell can have a single object associated with it.
        
        Subclasses could have other stuff, of course
    '''
    
    def __init__(self, grid, default=' '):
        self.grid = grid
        self.marks = {}  # Key: cell, Value = some object
        self.default = default
        
    def reset(self):
        self.marks = {}
        
    def __setitem__(self, cell, value):
        self.marks[cell] = value
        
    def __getitem__(self, cell):
        return self.marks.get(cell, self.default)
        
    def set_item_at(self, row, column, value):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            self.marks[cell]=value
        else:
            raise IndexError
    
    def get_item_at(self, row, column):
        assert row >= 0 and row < self.grid.num_rows
        assert column >= 0 and column < self.grid.num_columns
        cell = self.grid.cell_at(row, column)
        if cell:
            return self.marks.get(cell)
        else:
            raise IndexError
            
    def max(self):
        ''' Return the cell with the largest markup value. '''
        return max(self.marks.keys(), key=self.__getitem__)

    def min(self):
        ''' Return the cell with the smallest markup value. '''
        return min(self.marks.keys(), key=self.__getitem__)
        

    def is_obstacle(self,row,col):
        if Markup.get_item_at(self,row,col)=='*':
            return True
        else:
            return False
        

            
