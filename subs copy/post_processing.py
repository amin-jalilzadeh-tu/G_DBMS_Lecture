# ver 01.01
import json

def post_process_chain_response(response_of_chain):
    response_1 = json.dumps(response_of_chain)
    response_2 = json.loads(response_1)
    response_3 = json.loads(response_2)

    plot_info = None
    prompt_info = None

    if "plot" in response_3:
        plot_info = response_3["plot"]
    else:
        print("Warning: 'plot' key not found in response.")

    if "output_of_chain1" in response_3:
        if response_3["output_of_chain1"] == "I do not know.":
            prompt_info = "Sorry, I cannot answer the question."
        else:
            prompt_info = response_3["output_of_chain1"]
    else:
        print("Warning: 'output_of_chain1' key not found in response.")

    return plot_info, prompt_info
