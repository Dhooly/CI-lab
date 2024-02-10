from src import status
from flask import Flask, request

app = Flask(__name__)

COUNTERS = {}

# We will use the app decorator and create a route called slash counters.
# specify the variable in route <name>
# let Flask know that the only methods that is allowed to called
# on this function is "POST".


@app.route('/counters/<name>', methods=['POST'])
def create_counter(name):
    global COUNTERS

    """Create a counter"""
    app.logger.info(f"Request to create counter: {name}")

    if name in COUNTERS:
        return {"Message": f"Counter {name} already exists"}, status.HTTP_409_CONFLICT

    COUNTERS[name] = 0

    return {name: COUNTERS[name]}, status.HTTP_201_CREATED


@app.route('/counters/<name>', methods=['PUT'])
def update_counter(name):
    """Check if counter exists"""

    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist!"}, status.HTTP_404_NOT_FOUND

    COUNTERS[name] += request.get_json()

    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['GET'])
def get_counter(name):
    """Check if counter exists"""

    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist!"}, status.HTTP_404_NOT_FOUND

    return {name: COUNTERS[name]}, status.HTTP_200_OK


@app.route('/counters/<name>', methods=['DELETE'])
def delete_counter(name):
    """Check if counter exists"""

    if name not in COUNTERS:
        return {"Message": f"Counter {name} doesn't exist!"}, status.HTTP_404_NOT_FOUND

    COUNTERS.pop(name, None)
    return '', status.HTTP_204_NO_CONTENT
