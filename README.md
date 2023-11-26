# RnD-Nerve-Net-Simulator
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

---
### Example 1: ```buzzer.in```
A buzzer net is represented by the following figure (Assume that the input line is ```I1```, and that output ```O1``` is the value on the feedback axon just before the delay element):

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/8a61d106-8e75-4aca-aacd-344e82182037)

For this example, ```config.json``` is specified as:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/3d506ede-0932-446c-b77e-3774652d6628)

Here, the attribute ```I1``` denotes the input stream incident to input line ```I1```. Also, the contents of ```inputs/buzzer.in``` specify the buzzer net as follows:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/e973022e-9401-4126-9bff-43793d1a2678)

With ```"verbose_roundwise": true```, and ```"I1": "11111"```, on running ```python3 src/simulator.py``` the following output is observed, depicting the values of the neurons, axons, and I/O lines:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/391b36d9-887c-488d-9603-aea7052b9ab2)

Note that the event at ```O1``` is denoted by $(\Sigma^{*}0~~ \cup ~~\lambda)(11)*1$, where Σ = {0, 1}. Hence, a string with an odd number of ones, or a string with an odd number of ones after the last occurring zero character, would be accepted. Thus, the above case has ```{"O1": 1}``` as the final output, signifying acceptance/occurrence of the desired event.

If the same were to be run with the string ```1111``` as input on ```I1```, then the same output trace would be generated EXCEPT the last timeslot. Hence, ```{"O1": 0}``` would signify the string **not** being accepted.

---
### Example 2: ```input2.in```
The file ```inputs/input2.in``` encodes the following nerve net (Assume that ```B``` is ```I1```, and ```C``` is ```I2```, while ```D``` is ```O1```):

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/a0136c43-97f9-4fe7-a455-83f09ec9a150)

For this example, ```config.json``` is specified as:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/09925725-8333-4fa9-ba75-7f431536bae3)

The encoding is as follows:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/05c17a0a-f4b7-4f0d-9dd8-ac9e666ef633)

For the inputs specified in the above two images, running ```python3 src/simulator.py``` results in the following output:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/cd01cdbe-e31c-41ca-922d-e4e2473326b2)

Clearly, the input strings, and any equal-length prefixes of the inputs are not accepted as high-signal events at ```O1```. To describe the event at ```O1```, we assume the following alphabet-encoding: 0 : (C : 0, B : 0); 1 : (C : 0, B : 1); 2 : (C : 1, B : 0); 3 : (C : 1, B : 1), and Σ = {0, 1, 2, 3}. Here, the event at ```O1``` is given by $\Sigma^{ *}(1 \cup 3)\Sigma^{ *}2$. Thus, the following configuration should result in an accepting scenario for the same nerve net:

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/66a5d45a-7431-4de2-a316-8bf7d2712883)

Let us check the output stream to verify this!

![image](https://github.com/Whitelisted2/RnD-Nerve-Net-Simulator/assets/90827725/e6ba728d-16f1-4a94-86de-65c78dc93cc6)

Thus any scenario where the final input is 2 **with a 1 or 3 at some point in the prior past** is accepted, with ```{"O1": 1}``` at the final timeslot.

---
### Other Info
- If your nerve net has some amount of 'delay' with respect to its output, the input string must also have extra characters to compensate, since the event described could be something along the lines of $(0101)^{*}\Sigma\Sigma$ if the nerve net accepts $(0101)*$ with a delay of two time slots after the end of the last 'processed' character. Hence, be diligent when entering an input string.
- If ```verbose_roundwise``` is set to ```false```, then the output will just be the value of ```O1``` at the final timeslot.


