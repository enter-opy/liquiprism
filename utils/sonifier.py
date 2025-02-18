import mido
import time
import numpy as np

class Sonifier:
    def __init__(self, midi_port='', grid_size=4, pitch_scale=[-1, 0, 2, 6, 7, 11, 12], threshold=2):
        '''
        :param
            midi_port (str): name of the MIDI port to send messages to
            grid_size (int): size of the grid
            pitch_scale (list): list of pitch classes to choose from
        '''
        self.grid_size = grid_size
        self.midi_out = mido.open_output(midi_port)
        self.notes = np.array([int(pitch_scale[i % len(pitch_scale)]) for i in range(self.grid_size ** 2)])
        self.velocities = np.array([int(velocity) for velocity in np.random.randint(50, 100, self.grid_size ** 2)])
        self.threshold = threshold

    def push_midi(self, curr_face, prev_face, channel, interval, base_note=60):
        '''
        Send MIDI messages to the output port

        :param
            current_grid (np.array): current state of the grid
            previous_grid (np.array): previous state of the grid
            channel (int): MIDI channel to send messages to
            interval (float): time interval between note_on and note_off messages
            base_note (int): base note to play
        '''

        # Check for newly activated cells
        newly_activated_states = np.logical_and(curr_face, np.logical_not(prev_face)).astype(bool)
        newly_activated_cells = np.where(newly_activated_states)[0]

        if len(newly_activated_cells) > 0:
            selected_cells = newly_activated_cells[:min(self.threshold, len(newly_activated_cells))]
            notes = base_note + self.notes[selected_cells]
            velocities = self.velocities[selected_cells]

            for note, velocity in zip(notes, velocities):
                self.midi_out.send(mido.Message('note_on', note=int(note), velocity=int(velocity), channel=channel))

            time.sleep(interval/2)

            for note, velocity in zip(notes, velocities):
                self.midi_out.send(mido.Message('note_off', note=int(note), velocity=int(velocity), channel=channel))
