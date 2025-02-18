import threading
import time
import queue

from utils.topology import Topology
from utils.sonifier import Sonifier
from utils.visualizer import Visualizer

# Adjustable parameters
MIDI_PORT = 'LoopBe Internal MIDI 1'
GRID_SIZE = 5
SCALE = [-1, 0, 2, 6, 7, 11, 12]
STEP_INTERVALS = [1.5/4, 1.5/3, 1.5/2, 1.5/6, 1.5/5, 1.5/3]
BASE_NOTE = 62

def update_face(topology, sonifier, visualizer, face, interval):
    '''
    Update the state of a face of the cube and send MIDI messages to DAW
    :param
        liquiprism (Liquiprism): Instance of the Liquiprism class
        sonifier (Sonifier): Instance of the Sonifier class
        face_index (int): Index of the face to update
        interval (float): Time interval between updates
    '''
    while True:
        prev_face = topology.update_face(face)
        curr_face = topology.get_state()[face]

        # Send MIDI messages to port
        sonifier.push_midi(curr_face.flatten().tolist(), prev_face.flatten().tolist(), face, interval=interval, base_note=62)

        # Safely add update to the visualizer queue
        visualizer.update_queue(face, curr_face)

        time.sleep(interval)

def reset_state(topology):
    '''
    Reset the state of the cube
    '''
    while True:
        if topology.get_state().sum() < GRID_SIZE * 4:
            topology.reset_state()

        time.sleep(1)

def main():
    # Initialize the cube, sonifier, and visualizer
    topology = Topology(grid_size=GRID_SIZE)
    sonifier = Sonifier(midi_port=MIDI_PORT, grid_size=GRID_SIZE, pitch_scale=SCALE)
    visualizer = Visualizer(grid_size=GRID_SIZE, state=topology.get_state())

    # Start threads to update the face states
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 0, STEP_INTERVALS[0]), daemon=True).start()
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 1, STEP_INTERVALS[1]), daemon=True).start()
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 2, STEP_INTERVALS[2]), daemon=True).start()
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 3, STEP_INTERVALS[3]), daemon=True).start()
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 4, STEP_INTERVALS[4]), daemon=True).start()
    threading.Thread(target=update_face, args=(topology, sonifier, visualizer, 5, STEP_INTERVALS[5]), daemon=True).start()

    # Start thread to reset the cube
    threading.Thread(target=reset_state, args=(topology,), daemon=True).start()

    # Run the Ursina app
    visualizer.app.run()

if __name__ == '__main__':
    main()
