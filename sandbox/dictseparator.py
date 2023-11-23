input_strings = {"I1": "10111", "I2": "10010"}

digits = len(list(input_strings["I1"]))

for i in range(digits):
    input_rn = input_strings.copy()
    for j in input_rn:
        input_rn[j] = list(input_rn[j])[i]
    print(input_rn)