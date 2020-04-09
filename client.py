import argparse
import json

import requests
from loguru import logger

def send(data):
    response = requests.post("http://localhost:5000/data", json={"data": json.loads(data)})

    return response.json()

def retrieve(uuid):
    response = requests.get(f'http://localhost:5000/data/{uuid}')

    return response.json()

def request_operation(uuid, operation):
    response = requests.get(f'http://localhost:5000/data/{uuid}/{operation}')

    return response.json()


def main():
    parser = argparse.ArgumentParser(description='Test our API')
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--get", action="store_true")
    parser.add_argument("--calc", action="store_true")
    parser.add_argument("--data", dest="data", type=str)
    parser.add_argument("--uuid", dest="uuid", type=str)
    parser.add_argument("--op", dest="op", type=str)

    args = parser.parse_args()

    if args.send and args.data:
        logger.info(f"Sending data '{args.data}'")

        response = send(args.data)

        logger.info(f"Response: '{response}'")
    elif args.get and args.uuid:
        logger.info(f"Retrieving data using UUID '{args.uuid}'")

        response = retrieve(args.uuid)

        logger.info(f"Response: '{response}'")
    elif args.calc and args.uuid and args.op:
        logger.info(f"Requesting operation '{args.op}' using UUID '{args.uuid}'")

        response = request_operation(args.uuid, args.op)
        #response = retrieve(args.uuid)

        logger.info(f"Response: '{response}'")
    else:
        logger.info("No action")


if __name__ == '__main__':
    main()
