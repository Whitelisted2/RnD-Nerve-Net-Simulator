from lark import Lark, Transformer
import json

# input_path = "inputs/input1.in"
# input_strings = {
#     'I1': "1111"
#     }

with open("config.json", "r") as json_file:
    data = json.load(json_file)

input_path = data["input_path"]
input_strings = data["input_strings"]
verbose = bool(data["verbose_roundwise"])

grammar = r"""
    start: input_lines "\n" output_lines "\n" neuron_count "\n" threshold_value "\n" axons
    input_lines: NUMBER
    output_lines: NUMBER
    neuron_count: NUMBER
    threshold_value: NUMBER (" " NUMBER)*
    axons: axon_info*

    axon_info: neuron_or_input " " neuron_or_output " " delay (" " in_or_ex)? "\n"
    neuron_or_input: NEURON | INPUT
    neuron_or_output: NEURON | OUTPUT
    delay: NUMBER

    in_or_ex: /[01]/

    NEURON: /\d+/
    INPUT: /[I]\d+/
    OUTPUT: /[O]\d+/
    NUMBER: /\d+/

    # %ignore /\s+/
    # %ignore /\/\/.*/

    """

class AxonTransformer(Transformer):
    def start(self, items):
        # print("ttt")
        input_lines, output_lines, neuron_count, threshold, axons = items

        # print(threshold.children[0])
        threshold_list = []
        for t in threshold.children:
            threshold_list.append(int(t.value))
        # print(axons.children[0])

        axon_dict = {}
        neuron_in_dict = {}
        neuron_out_dict = {}
        axon_id = 0
        for axon in axons.children:
            # print(axon.children[0].children[0])
            start_point = axon.children[0].children[0].value
            end_point = axon.children[1].children[0].value
            axon_delay = int(axon.children[2].children[0].value)

            # for each neuron, construct in_dict, out_dict.
            if end_point not in neuron_in_dict:
                neuron_in_dict[end_point] = [axon_id]
            else:
                neuron_in_dict[end_point].append(axon_id)

            if start_point not in neuron_out_dict:
                neuron_out_dict[start_point] = [axon_id]
            else:
                neuron_out_dict[start_point].append(axon_id)


            junction_values = [0 for _ in range(axon_delay+1)]

            # print(axon.children[3])
            i_or_e = -1
            if len(axon.children) == 4:
                i_or_e = int(axon.children[3].children[0])
            else:
                i_or_e = None

            axon_dict[axon_id] = {
                "start_point" : start_point,
                "end_point": end_point,
                "axon_delay": axon_delay,
                "i_or_e": i_or_e,
                "junction_values": junction_values
                }
            
            
            axon_id+=1
            
        #     axon_id = len(axon_dict) + 1
        #     axon_dict[axon_id] = axon
        
        neuron_value_now = [0 for _ in range(int(neuron_count.children[0].value))]
        
        nn_dict = {
            "input_lines": int(input_lines.children[0].value),
            "output_lines": int(output_lines.children[0].value),
            "neuron_count": int(neuron_count.children[0].value),
            "neuron_value_now": neuron_value_now,
            "threshold": threshold_list,
            "axons": axon_dict
        }
        # print(nn_dict)
        return nn_dict, neuron_in_dict, neuron_out_dict
    


parser = Lark(grammar, parser='lalr', transformer=AxonTransformer())

lines = ""
with open(input_path, 'r') as f:
    lines = f.read()
# print(lines)

input_data = lines
# parser_no_t = Lark(grammar, parser='lalr')
# result = parser_no_t.parse(input_data).pretty()
# print(result)

result, in_dict, out_dict = parser.parse(input_data)
# print(result)
# print(in_dict)
# print(out_dict)

num_iter = -1
if len(input_strings) == 0:
    print("How many iterations would you like to run the simulation for? Enter a value: ", end="")
    num_iter = int(input())
else:
    num_iter = len(input_strings["I1"])

def update_neurons(result):
    # global result
    result_copy = result.copy()
    for neuron_id in range(1, result_copy["neuron_count"]+1):
        inputs = in_dict[str(neuron_id)]
        # print(neuron_id, "has input lines", inputs)
        # print(in_dict)
        threshold_n = result_copy["threshold"][neuron_id-1]
        fire = 0
        for i in inputs:
            # print(neuron_id, i, result["axons"][i]["i_or_e"])
            # print(neuron_id,"i_or_e:",result_copy["axons"][i]["i_or_e"], "value", result_copy["axons"][i]["junction_values"][0])
            if (result_copy["axons"][i]["i_or_e"] == 1) and (result_copy["axons"][i]["junction_values"][0] == 1):
                fire += 1
            elif (result_copy["axons"][i]["i_or_e"] == 0) and (result_copy["axons"][i]["junction_values"][0] == 1):
                fire -= 1
        if fire >= threshold_n:
            result_copy["neuron_value_now"][neuron_id-1] = 1
            next_axon = out_dict[str(neuron_id)]
            for j in next_axon:
                result_copy["axons"][j]["junction_values"][-1] = 1
        else:
            result_copy["neuron_value_now"][neuron_id-1] = 0
            next_axon = out_dict[str(neuron_id)]
            for j in next_axon:
                result_copy["axons"][j]["junction_values"][-1] = 0
        
    return result_copy

def update_neurons_loop(result):
    while(result != update_neurons(result)):
        result = update_neurons(result)
    return result

def shift(junc_array, new_ele):
    junc_array.pop(0)
    junc_array.append(new_ele)
    return junc_array

# occurs once per timeslot
def update_axons(result, input_now): # input contains the values that I1, I2, etc will provide in this round
    # global result
    for a_id in result["axons"]:
        # dest_neuron = result["axons"][a_id]["end_point"]
        src_neuron = result["axons"][a_id]["start_point"]
        push_ele = -1
        if list(src_neuron)[0] == "I":
            push_ele = input_now[src_neuron]
        else:
            push_ele = result["neuron_value_now"][int(src_neuron) - 1] # push source neuron value onto axon
        result["axons"][a_id]["junction_values"] = shift(result["axons"][a_id]["junction_values"], push_ele)
    result = update_neurons_loop(result)
    return result

def print_axons_state(result):
    print("Axons  : ", end="")
    for a_id in result["axons"]:
        print(str(a_id)+ ":" + str(result["axons"][a_id]["junction_values"]) + "; ", end="")
    print()

def print_neurons_state(result):
    i = 1
    print("Neurons: ",end="")
    for ele in result["neuron_value_now"]:
        print(str(i) + ":[" + str(ele) + "]; ", end="")
        i+=1
    print()

def get_zero_delay_axons(result):
    no_delay = []
    for ele in result["axons"]:
        if(result["axons"][ele]["axon_delay"] == 0):
            no_delay.append(ele)
    return no_delay

def update_zero_delay_axons(result):
    result_copy = result.copy()
    zero_delay_axons = get_zero_delay_axons(result_copy)
    for a_id in zero_delay_axons:
        # dest_neuron = result["axons"][a_id]["end_point"]
        src_neuron = result_copy["axons"][a_id]["start_point"]
        push_ele = -1
        if list(src_neuron)[0] == "I":
            continue
        else:
            push_ele = result_copy["neuron_value_now"][int(src_neuron) - 1]
        result_copy["axons"][a_id]["junction_values"] = shift(result_copy["axons"][a_id]["junction_values"], push_ele)
    return result_copy

def update_zero_delay_axon_and_neuron_loop(result):
    new_result = update_neurons_loop(result)
    new_result = update_zero_delay_axons(new_result)
    while(result != new_result):
        result = new_result.copy()
        new_result = update_neurons_loop(result)
        new_result = update_zero_delay_axons(new_result)
    return result

def get_outputs(result):
    output_dict = {}
    for axon_id in result["axons"]:
        if result["axons"][axon_id]["end_point"][0] == 'O':
            output_dict[result["axons"][axon_id]["end_point"]] = result["axons"][axon_id]["junction_values"][0]
    return output_dict


# digits = len(list(input_strings["I1"]))

time=1
if verbose:
    print("At time 0")
    print_neurons_state(result)
    print_axons_state(result)
for i in range(num_iter):
    input_rn = input_strings.copy()
    for j in input_rn:
        input_rn[j] = int(list(input_rn[j])[i])

    result = update_zero_delay_axon_and_neuron_loop(result)
    result = update_axons(result, input_rn)
    result = update_zero_delay_axon_and_neuron_loop(result)

    curr_outputs = get_outputs(result)
    if verbose:
        print(input_rn, "at time", time)
        print_neurons_state(result)
        print_axons_state(result)
        print(curr_outputs)
        print()
    time+=1

if not verbose:
   print(curr_outputs)

# multiple input lines
# abab could be 01, 10, 01, 10 => {0101, 1010}

