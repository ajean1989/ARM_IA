import httpx
from config import *
# Tests des différentes ressources


# API KEY

headers = {'X-API-Key': list(API_KEYS.keys())[0]}


# def test_helloworld_raw() :
#     response = httpx.get(f"http://api-ia:6002/", headers = headers)
#     assert response.status_code == 200


def test_helloworld_traefik() :
    response = httpx.get(f"https://traefik/api-ia/", headers = headers, verify=False)
    assert response.status_code == 200


def test_helloworld_mlflow() :
    response = httpx.get(f"https://traefik/mlflow/", headers = headers, verify=False)
    assert response.status_code == 200

def test_helloworld_gradio() :
    response = httpx.get(f"https://traefik/gradio/", headers = headers, verify=False)
    assert response.status_code == 200
