import requests

def send(data):
    response = requests.post("http://localhost:5000/data", json={"data": data})

    print(response.json())

def retrieve(uuid):
    response = requests.get(f'http://localhost:5000/data/{uuid}')

    print(response.json())


def main():
    #x = send([1,2,3,4])
    retrieve("5a2fd555-a1bf-4d48-8bf2-4c5f95e71c0f")

if __name__ == '__main__':
    main()
