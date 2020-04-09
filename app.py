#imports das libs padrao do python

#imports de terceiros
from flask import Flask, request, jsonify
from loguru import logger

#imports do proprio prj
from statsapi import data_store
app = Flask(__name__)

#save received list
@app.route("/data",methods=["POST"])
def save_data():
    logger.info(f"Saving data...")

    content = request.get_json()

    uuid = data_store.save(content["data"])

    logger.info(f"Data saved with UUID '{uuid}' successfully")

    return jsonify({"status": "success", "message": "data saved successfully", "uuid":uuid})

@app.route("/data/<uuid>", methods=["GET"])
def retrieve_data(uuid):
    logger.info(f"Retrieving data associated with UUID '{uuid}' ...")

    try:
        stored_data = data_store.get(uuid)
    except KeyError:
        logger.warning(f"Cannot retrieve data associated with UUID '{uuid}'.")

        return jsonify({"status": "failed", "message": "data cannot be retrieved.", "data": []})

    logger.info(f"Data associated with UUID '{uuid}' retrieved successfully")

    return jsonify({"status": "success", "message": "data retrieved successfuly.",
                    "data": stored_data})


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)