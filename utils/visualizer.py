from ursina import Ursina, Entity, color, scene, destroy, time, camera, sin, cos, window
import queue
import numpy as np

class Visualizer():
    def __init__(self, grid_size=4, state=np.array([np.random.randint(2, size=(4, 4)) for _ in range(6)])):
        '''
        :param
            grid_size (int): size of the grid
            cells (np.array): initial state of the cells
        '''
        self.app = Ursina()
        self.grid_size = grid_size
        self.origin = Entity(alpha=0)
        self.origin.update = self.update
        self.state = state
        self.queue = queue.Queue()
        self.create_grids()
        window.size = (800, 800)

    def create_grid(self, position, data, rotation):
        '''
        Create a grid of cells

        :param
            position (tuple): position of the grid
            data (np.array): state of the cells
            rotation (tuple): rotation of the grid
        '''
        grid_entity = Entity(model='quad', scale=(1, 1, 1), position=position, rotation=rotation, alpha=0)
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                grid_color = color.green if data[row, col] else color.red
                Entity(model='quad', scale=(1/self.grid_size, 1/self.grid_size, 1), position=(col/self.grid_size - 0.5 + 1/(2*self.grid_size), row/self.grid_size - 0.5 + 1/(2*self.grid_size), 0),
                            color=grid_color, parent=grid_entity)
                outline_thickness = 0.2
                Entity(model='line', position=(col/self.grid_size - 0.5 + 1/(2*self.grid_size), row/self.grid_size- 0.5 + 1/(self.grid_size), 0),
                    scale=(1/self.grid_size, outline_thickness, 1), color=color.white, parent=grid_entity)
                Entity(model='line', position=(col/self.grid_size - 0.5 + 1/(self.grid_size), row/self.grid_size - 0.5 + 1/(2*self.grid_size), 0),
                    scale=(1/self.grid_size, 1/self.grid_size, 1), rotation=(0, 0, 90), color=color.white, parent=grid_entity)

    def create_grids(self):
        '''
        Create grids for each face of the cube
        '''
        self.create_grid(position=(0, 0, -0.51), data=self.state[0], rotation=(0, 0, 0))
        self.create_grid(position=(0, 0, 0.51), data=self.state[1], rotation=(0, 180, 0))
        self.create_grid(position=(-0.51, 0, 0), data=self.state[2], rotation=(0, 90, 0))
        self.create_grid(position=(0.51, 0, 0), data=self.state[3], rotation=(0, -90, 0))
        self.create_grid(position=(0, 0.51, 0), data=self.state[4], rotation=(90, 0, 0))
        self.create_grid(position=(0, -0.51, 0), data=self.state[5], rotation=(-90, 0, 0))

    def set_state(self, face, current_state):
        '''
        Set the state of a face of the cube

        :param
            face_index (int): index of the face to update
            current_state (np.array): current state of the face
        '''
        self.state[face] = current_state

    def update(self):
        '''
        Ursina update function
        '''
        while not self.queue.empty():
            face_index, current_state = self.queue.get()
            self.set_state(face_index, current_state)

        for entity in scene.entities:
            if entity != self.origin:
                destroy(entity)

        self.create_grids()

        camera.position = (sin(time.time()) * 5, 3, cos(time.time()) * 5)
        camera.look_at(self.origin)

    def update_queue(self, face_index, current_state):
        '''
        Safely add update to the visualizer queue

        :param
            face_index (int): index of the face to update
            current_state (np.array): current state of the face
        '''
        self.queue.put((face_index, current_state))
