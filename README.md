# Paper Implementation

[*Paper*](http://www.icad.org/websiteV2.0/Conferences/ICAD2002/proceedings/36_AlanDorin.pdf)
## Instructions
**Install dependencies**
```bash
pip install -r requirements.txt
```

**Connect MIDI channels**

1. Open a DAW (Digital Audio Workstation) like Ableton Live, FL Studio, etc.
2. Connect MIDI channels 1 - 6 to different sound sources.
3. Set the `MIDI_PORT` in the script to the DAW's MIDI port.

**Adjustable parameters**
```python
# Adjustable parameters
MIDI_PORT = 'LoopBe Internal MIDI 1'
GRID_SIZE = 4
SCALE = [-1, 0, 2, 6, 7, 11, 12]
STEP_DURATIONS = [1/4, 1/3, 1/2, 1/4, 1/5, 1/3]
BASE_NOTE = 62
```
- `MIDI_PORT (str)`: Set the midi port to which the midi is to be send.
- `GRID_SIZE (int)`: Set your preffered grid size (Number of grids in a row/column)
- `SCALE (list)`: Set your preffered scale.
- `STEP_DURATIONS (list)`: Set the channel step durations in seconds.
- `BASE_NOTE (int): set the base note (62 is middle C)

**Run the script**
```bash
python main.py
```

## Demo
[**Watch Demo in YouTube**](https://www.youtube.com/watch?v=e_6AsjG45FI)
