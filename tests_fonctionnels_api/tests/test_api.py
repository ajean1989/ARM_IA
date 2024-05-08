import httpx
from config import *
# Tests des différentes ressources


# API KEY

headers = {'X-API-Key': list(API_KEYS.keys())[0]}


# def test_helloworld_raw() :
#     response = httpx.get(f"http://api-ia:6002/", headers = headers)
#     assert response.status_code == 200


def test_helloworld_traefik() :
    response = httpx.get(f"http://traefik/api-ia/", headers = headers)
    assert response.status_code == 200


def test_helloworld_mlflow() :
    response = httpx.get(f"http://traefik/mlflow/", headers = headers)
    assert response.status_code == 200

def test_helloworld_gradio() :
    response = httpx.get(f"http://traefik/gradio/", headers = headers)
    assert response.status_code == 200
