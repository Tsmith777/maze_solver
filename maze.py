from cell import Cell
import time
import random

class Maze:
    def __init__(self, x1, y1, num_rows, num_cols, cell_size_x, cell_size_y, win=None, seed=None):
        self._cells = []
        self._x1 = x1
        self._y1 = y1
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win
        if seed:
            random.seed(seed)

        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self): 
        for i in range(self._num_cols):
            col_cells = []
            for j in range(self._num_rows):
                cell = Cell(self._win)
                col_cells.append(cell)
            self._cells.append(col_cells)
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        if self._win is None:
            return
        x1 = self._x1 + i * self._cell_size_x
        y1 = self._y1 + j * self._cell_size_y
        x2 = x1 + self._cell_size_x
        y2 = y1 + self._cell_size_y
        self._cells[i][j].draw(x1, y1, x2, y2)
        self._animate()

    def _animate(self):
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self):
        self._cells[0][0].has_top_wall = False
        self._draw_cell(0, 0)
        self._cells[self._num_cols - 1][self._num_rows - 1].has_bottom_wall = False
        self._draw_cell(self._num_cols - 1, self._num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j].visited = True
        while True:
            need_to_visit = []
            if j > 0 and not self._cells[i][j - 1].visited:
                    need_to_visit.append((i, j-1))
            if j < self._num_rows - 1 and not self._cells[i][j + 1].visited:
                    need_to_visit.append((i, j+1))
            if i > 0 and not self._cells[i - 1][j].visited:
                    need_to_visit.append((i-1, j))
            if i < self._num_cols - 1 and not self._cells[i + 1][j].visited:
                    need_to_visit.append((i+1, j))
                    
            if len(need_to_visit) == 0:
                self._draw_cell(i,j)
                return
            
            next_i, next_j = random.choice(need_to_visit)
            if next_i < i:  # Moving left
                self._cells[i][j].has_left_wall = False
                self._cells[next_i][next_j].has_right_wall = False
            elif next_i > i:  # Moving right
                self._cells[i][j].has_right_wall = False
                self._cells[next_i][next_j].has_left_wall = False
            elif next_j < j:  # Moving up
                self._cells[i][j].has_top_wall = False
                self._cells[next_i][next_j].has_bottom_wall = False
            elif next_j > j:  # Moving down
                self._cells[i][j].has_bottom_wall = False
                self._cells[next_i][next_j].has_top_wall = False

            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self):
        for col in self._cells:
            for cell in col:
                cell.visited = False

    def solve(self):
         return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()
        current_cell = self._cells[i][j]
        end_cell = self._cells[self._num_cols - 1][self._num_rows - 1]
        current_cell.visited = True
        if current_cell == end_cell:
            return True
        need_to_visit = []
        if j > 0 and not current_cell.has_top_wall and not self._cells[i][j - 1].visited:
                need_to_visit.append((i, j - 1))
        if j < self._num_rows - 1 and not current_cell.has_bottom_wall and not self._cells[i][j + 1].visited:
                need_to_visit.append((i, j + 1))
        if i > 0 and not current_cell.has_left_wall and not self._cells[i - 1][j].visited:
                need_to_visit.append((i-1, j))
        if i < self._num_cols - 1 and not current_cell.has_right_wall and not self._cells[i + 1][j].visited:
                need_to_visit.append((i+1, j))
        for (next_i, next_j) in need_to_visit:
            neighbor_cell = self._cells[next_i][next_j]
            current_cell.draw_move(neighbor_cell)
            if self._solve_r(next_i, next_j):
                return True
            current_cell.draw_move(neighbor_cell, undo=True)
        return False