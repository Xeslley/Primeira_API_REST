import pytest
import requests

class TestAPI:

    #estas fixture sao para poder reaproveitar essas etapas injetando em outros testes
    @pytest.fixture(scope="class")
    def data(self):
        test_data = [1, 2, 3, 4]

        return test_data

    @pytest.fixture(scope="class")
    def url(self):
        url = "http://localhost:5000/data"

        return url

    #uma fixture pode ser injetada com outras fixtures
    #neste caso o scopo foi mudado para essa fixture rodar somente uma vez por classe
    #Possible values for scope are: function, class, module, package or session.
    @pytest.fixture(scope="class")
    def uuid(self,url,data):
        response = requests.post(url, json= {"data":data})

        return response.json()["uuid"]

    #sempre comecar com a palavra test para o pytest saber que eh teste
    def test_save_data(self, uuid):

        assert uuid is not None

    def test_get_data(self, url, uuid, data):
        response = requests.get(f"{url}/{uuid}")

        assert response.ok
        assert response.json()["data"] == data

    def test_calc_mean(self, url, uuid):
        response = requests.get(f"{url}/{uuid}/mean")

        assert response.ok
        assert response.json()["result"] == pytest.approx(2.5)

    def test_calc_min(self, url, uuid):
        response = requests.get(f"{url}/{uuid}/min")

        assert response.ok
        assert response.json()["result"] == 1

    def test_calc_max(self, url, uuid):
        response = requests.get(f"{url}/{uuid}/max")

        assert response.ok
        assert response.json()["result"] == 4

    def test_calc_median(self, url, uuid):
        response = requests.get(f"{url}/{uuid}/median")

        assert response.ok
        assert response.json()["result"] == pytest.approx(2.5)

    def test_calc_range(self, url, uuid):
        response = requests.get(f"{url}/{uuid}/range")

        assert response.ok
        assert response.json()["result"] == pytest.approx(3)

    @pytest.mark.parametrize("operation, expected_result", [("mean",2.5),("min",1),("max",4),("median",2.5),("range",3)])
    def test_calc_param(self,url,uuid, operation, expected_result):
        response = requests.get(f"{url}/{uuid}/{operation}")

        assert response.ok
        assert pytest.approx(expected_result) == response.json()["result"]