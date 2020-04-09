#imports das libs padrao do python
import json

#imports de terceiros
from flask import Flask, request, jsonify
from loguru import logger

#imports do proprio prj
from statsapi import data_store, operation


app = Flask(__name__)

#save received list
@app.route("/data",methods=["POST"])
def save_data():
    logger.info(f"Saving data...")

    content = request.get_json()

    uuid = data_store.save(content["data"])

    logger.info(f"Data saved with UUID '{uuid}' successfully")

    return jsonify({"status": "success", "message": "data saved successfully", "uuid":uuid})

def atempt_get_data(uuid):
    raw_stored_data = []
    try:
        raw_stored_data = data_store.get(uuid)
    except KeyError:
        logger.warning(f"Cannot retrieve data associated with UUID '{uuid}'.")

        return jsonify({"status": "failed", "message": "data cannot be retrieved.", "data": []})
    return raw_stored_data

@app.route("/data/<uuid>", methods=["GET"])
def retrieve_data(uuid):
    logger.info(f"Retrieving data associated with UUID '{uuid}' ...")
    stored_data = atempt_get_data(uuid)
    logger.info(f"Data associated with UUID '{uuid}' retrieved successfully")

    return jsonify({"status": "success", "message": "data retrieved successfuly.",
                    "data": stored_data})


@app.route("/data/<uuid>/<operation>", methods=["GET"])
def process_operation(uuid, operation):
    logger.info(f"Prossecing operation '{operation}' on data associated with UUID '{uuid}'...")

    stored_data = atempt_get_data(uuid)

    if not stored_data:
        return jsonify(
            {"status": "failed", "message": "data cannot be retrieved.",
             "result": None})
    try:
        operation_func = get_operation(operation)
        logger.info(f"operation {operation} = {operation_func}")
    except NoSuchOperationError:
        logger.warning(f"Cannot find operation '{operation}'.")

        return jsonify({"status": "failed", "message": f"no such {operation}",
                    "result": None})

    result = operation_func(stored_data)

    logger.info(f"Operation '{operation}' on data associated with UUID '{uuid}' finished successfully!")

    return jsonify({"status": "success", "message": "result completed successfuly.",
                "result": result})

class NoSuchOperationError(Exception):
    pass

def get_operation(operation_name):
    if operation_name == 'min':
        return operation.op_min
    elif operation_name == 'max':
        return operation.op_max
    elif operation_name == 'mean':
        return operation.op_mean
    elif operation_name == 'median':
        return operation.op_median
    # elif operation_name == 'mode':
    #     return operation.op_mode
    elif operation_name == 'range':
        return operation.op_range
    else:
        raise NoSuchOperationError



if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)