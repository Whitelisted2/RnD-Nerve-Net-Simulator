from lark import Lark, Transformer
import json

input_path = "inputs/input1.in"

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

    # def axon_info(self, items):
    #     start, end, delay, inhibitory = items
    #     return {
    #         "start": start,
    #         "end": end,
    #         "delay": int(delay),
    #         "inhibitory": inhibitory if inhibitory is not None else None
    #     }

    # def neuron_or_input(self, items):
    #     return items[0]

    # def input(self, items):
    #     return items[0]

    # def inhibitory(self, items):
    #     return items[0]

parser = Lark(grammar, parser='lalr', transformer=AxonTransformer())

lines = ""
with open(input_path) as f:
    lines = f.read()
# print(lines)

input_data = lines
# parser_no_t = Lark(grammar, parser='lalr')
# result = parser_no_t.parse(input_data).pretty()
# print(result)

result, in_dict, out_dict = parser.parse(input_data)
print(result)
# for i in result["axons"]:
#     print(result["axons"][i])
# print(json.dumps(result, sort_keys=True, indent=4))

