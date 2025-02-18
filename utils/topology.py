import numpy as np
import random

class Topology:
    def __init__(self, grid_size):
        '''
        Handles the topology of the cube and trasition rules

        :param
            grid_size (int): size of the grid
        '''
        self.grid_size = grid_size
        self.state = np.array([
            np.random.choice([True, False], (grid_size, grid_size)) for _ in range(6)
        ])
        self.neighbor_cache = self.compute_neighbors()

    def compute_neighbors(self):
        '''
        Compute the neighbors of each cell in the cube

        :return
            cache (dict): dictionary mapping the coordinates of each cell to its neighbors
        '''
        cache = {}
        for face in range(6):
            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    cache[(face, row, col)] = self.find_neighbors(face, row, col)
        return cache

    def find_neighbors(self, face, row, col):
        '''
        Find the neighbors of a cell in the cube

        :param
            face (int): index of the face
            row (int): row index of the cell
            col (int): column index of the cell

        :return
            neighbors (list): list of neighboring cells
        '''
        neighbors = []
        offsets = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in offsets:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.grid_size and 0 <= nc < self.grid_size:
                neighbors.append((face, nr, nc))
            else:
                if nr < 0:
                    adj_face, adj_pos = self.get_adjacent(face, "up", col)
                    neighbors.append((adj_face, self.grid_size - 1, adj_pos))
                elif nr >= self.grid_size:
                    adj_face, adj_pos = self.get_adjacent(face, "down", col)
                    neighbors.append((adj_face, 0, adj_pos))
                elif nc < 0:
                    adj_face, adj_pos = self.get_adjacent(face, "left", row)
                    neighbors.append((adj_face, adj_pos, self.grid_size - 1))
                elif nc >= self.grid_size:
                    adj_face, adj_pos = self.get_adjacent(face, "right", row)
                    neighbors.append((adj_face, adj_pos, 0))

        return neighbors

    def get_adjacent(self, face, direction, index):
        '''
        Get the adjacent face and position of a cell

        :param
            face (int): index of the face
            direction (str): direction of the adjacent face
            index (int): position index

        :return
            adj_face (int): index of the adjacent face
            adj_pos (int): position index on the adjacent face
        '''
        mapping = {
            0: {"up": (4, index), "down": (5, index), "left": (3, index), "right": (1, index)},
            1: {"up": (4, index), "down": (5, index), "left": (0, index), "right": (2, index)},
            2: {"up": (4, index), "down": (5, index), "left": (1, index), "right": (3, index)},
            3: {"up": (4, index), "down": (5, index), "left": (2, index), "right": (0, index)},
            4: {"up": (3, index), "down": (1, index), "left": (0, index), "right": (2, index)},
            5: {"up": (1, index), "down": (3, index), "left": (0, index), "right": (2, index)},
        }

        return mapping[face][direction]

    def update_cell(self, face, row, col):
        '''
        Update the state of a cell in the cube

        :param
            face (int): index of the face
            row (int): row index of the cell
            col (int): column index of the cell

        :return
            state (bool): new state of the cell
        '''
        neighbors = self.neighbor_cache[(face, row, col)]
        active_neighbors = sum(self.state[f, r, c] for f, r, c in neighbors)
        below_neighbor = self.get_below_neighbor(face, row, col)

        if self.state[face, row, col]:
            return active_neighbors in (2, 3)
        else:
            return active_neighbors >= 4 or below_neighbor and random.random() < 1 / 3


    def update_face(self, face):
        '''
        Update the state of a face of the cube

        :param
            face (int): index of the face to update

        :return
            prev_state (np.array): previous state of the face
        '''
        next_state = np.copy(self.state)
        prev_state = np.copy(self.state)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                next_state[face, row, col] = self.update_cell(face, row, col)
        self.state = next_state

        prev_face = prev_state[face]

        return prev_face

    def get_below_neighbor(self, face, row, col):
        '''
        Get the state of the cell below the current cell

        :param
            face (int): index of the face
            row (int): row index of the cell
            col (int): column index of the cell

        :return
            state (bool): state of the cell below
        '''
        below_face = self.get_adjacent(face, "down", row)[0]
        below_row = (row + 1) % self.grid_size
        below_col = col
        return self.state[below_face, below_row, below_col]

    def reset_state(self):
        '''
        Reset the state of the cube
        '''
        self.state = np.array([
            np.random.choice([True, False], (self.grid_size, self.grid_size)) for _ in range(6)
        ])

    def get_state(self):
        '''
        Get the current state of the cube

        :return
            state (np.array): current state of the cube
        '''
        return self.state
