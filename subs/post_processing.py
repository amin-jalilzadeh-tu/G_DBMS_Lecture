# ver 01.01
import json

def post_process_chain_response(response_of_chain):
    """
    Attempt to parse the chain response as JSON.
    If it fails, return a fallback structure.
    """
    try:
        return json.loads(response_of_chain)
    except json.JSONDecodeError:
        return {"answer": response_of_chain}
