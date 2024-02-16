import httpx
import os

from automatic_dataset.automatic_dataset_creation import automatic_dataset


process = automatic_dataset("data/sample/video_test_2.mp4")

def test_retrieve_off():

    res = httpx.delete(f"http://localhost/api-backend/items/8000500310427", headers = process.headers)

    res = process.retrieve_off("8000500310427")
    print(res)
    assert res.status_code == 200

    res = httpx.get(f"http://localhost/api-backend/items/", headers = process.headers)
    print(res.content)
    assert res.status_code == 200

    res = httpx.get(f"http://localhost/api-backend/items/8000500310427", headers = process.headers)
    print(res.content)
    assert res.status_code == 200



def test_reset_temp():

    with open (os.path.join("automatic_dataset", "temp", "test.txt"), "w") as txt :
        txt.write("hello")

    temp_folder = os.listdir(os.path.join("automatic_dataset", "temp"))
    assert len(temp_folder) > 0

    process.reset_temp()

    temp_folder = os.listdir(os.path.join("automatic_dataset", "temp"))
    assert len(temp_folder) == 0

     
def test_video_detection():
    process.detection()
    temp_folder = os.listdir(os.path.join("automatic_dataset", "temp"))
    assert len(temp_folder) > 0
    process.code()