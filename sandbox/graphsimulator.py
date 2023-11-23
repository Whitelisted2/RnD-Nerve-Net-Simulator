from lark import Lark, Transformer
import json
import networkx as nx
import matplotlib.pyplot as plt

input_path = "inputs/input1.in"
input_strings = ["1111"]

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
            if start_point not in neuron_in_dict:
                neuron_in_dict[start_point] = [axon_id]
            else:
                neuron_in_dict[start_point].append(axon_id)

            if end_point not in neuron_out_dict:
                neuron_out_dict[end_point] = [axon_id]
            else:
                neuron_out_dict[end_point].append(axon_id)


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
print(result["axons"])
# print(in_dict)
# print(out_dict)

edges = []
for axon in result["axons"]:
    # if axon["start_"]
    # print("hi", result["axons"][axon])
    edges.append(( result["axons"][axon]["start_point"], result["axons"][axon]["end_point"], 
        {
            "junction_values": result["axons"][axon]["junction_values"],
            "i_or_e": result["axons"][axon]["i_or_e"]
        }))
    
G = nx.DiGraph(edges)

plt.figure()
pos = nx.spring_layout(G, seed=0)
edge_labels = nx.get_edge_attributes(G, "junction_values")

# set node state positions
# state_pos = {n: (x+0.12, y+0.05) for n, (x,y) in pos.items()}
# draw graph
nx.draw_networkx(G, pos, node_size=600)
# draw node state labels
# nx.draw_networkx_labels(G, state_pos, labels=node_states, font_color='red')
# draw edge attributes

nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.savefig("img/img.jpg")

# num_iter = -1
# if len(input_strings) == 0:
#     print("How many iterations would you like to run the simulation for? Enter a value: ", end="")
#     num_iter = int(input())
# else:
#     num_iter = len(list(input_strings[0]))

# def init_computation():
#     for neuron_id in range(1, result["neuron_count"]+1):
#         print(neuron_id)

# init_computation()

# for iter in num_iter:
#     neuron_computation()
#     axon_updation()

# multiple input lines
# abab could be 01, 10, 01, 10 => {0101, 1010}

    

# result in_dict out_dict input_string

# for i in result["axons"]:
#     print(result["axons"][i])
# print(json.dumps(result, sort_keys=True, indent=4))

