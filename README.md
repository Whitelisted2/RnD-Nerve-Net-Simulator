# RnD-NerveNetSimulator
This repository contains files related to RnD Project (Autumn 2023).

### Instructions
- You can edit input file path in the file ```config.json```, and also enter the input string there. (An example is explained below.) The ```verbose_roundwise``` option allows you to view the internal junction/neuron values at each timeslot.
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

### Example 1: ```buzzer.in```
A buzzer net is represented by the following figure (Assume that the input line is ```I1```, and that output ```O1``` is the value on the feedback axon just before the delay element):

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/8a61d106-8e75-4aca-aacd-344e82182037)

For this example, ```config.json``` is specified as:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/3d506ede-0932-446c-b77e-3774652d6628)

Here, the attribute ```I1``` denotes the input stream incident to input line ```I1```. Also, the contents of ```inputs/buzzer.in``` specify the buzzer net as follows:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/e973022e-9401-4126-9bff-43793d1a2678)

With ```"verbose_roundwise": true```, and ```"I1": "11111"```, on running ```python3 src/simulator.py``` the following output is observed, depicting the values of the neurons, axons, and I/O lines:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/391b36d9-887c-488d-9603-aea7052b9ab2)

Note that the event at ```O1``` is denoted by $(\Sigma^{*}0~~ U ~~~\lambda)(11)*1$

