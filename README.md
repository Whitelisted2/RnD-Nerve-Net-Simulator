# RnD-NerveNetSimulator
This repository contains files related to RnD Project (Autumn 2023).

### Instructions
- You can edit input file path in the file ```config.json```, and also enter the input string there. The ```verbose``` option allows you to view the internal junction/neuron values at each timeslot.
- Run ```python3 src/simulator.py``` to simulate the nerve net and print output at the time of the last input character(s) being sent into the system.
- ```sandbox/``` contains code that consists of snippets dealing with graphical approach, dictionary separation, etc.

### Input Format
Input files must be of the following format:
- Line 1: Number of input lines (I1, I2, ...)
- Line 2: Number of output lines (O1, O2, ...)
- Line 3: Number of neurons (1, 2, ...)
- Line 4: Threshold values for neurons ordered by neuron ID
- Line 5 onwards: Axon specifications, in the format: ```<start-point> <end-point> <delay> <nature>``` where:
  - ```<start-point>``` can be a neuron or an input line.
  - ```<end-point>``` can be a neuron or an output line.
  - ```<delay>``` is a non-negative integer.
  - ```<nature>``` is either 0 (inhibitory) or 1 (excitory).
