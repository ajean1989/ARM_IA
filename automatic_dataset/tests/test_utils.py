from automatic_dataset.utils import Utils
from pprint import pprint
import shutil
import os
import httpx

from automatic_dataset.config import *

headers = {"X-API-Key" : list(API_KEYS.keys())[0]}

def test_hello_world():
    res = httpx.get(f"http://localhost/api-ia/", headers=headers)
    print(res)
    assert res.status_code == 200

# def test_get_api():
#     res = httpx.get(f"http://localhost/api-ia/dataset/0", headers=headers)
#     print(res)
#     assert res.status_code == 200

def test_pproc_frame(df_anotation):

    shutil.copy(os.path.join("data", "sample", "pesto.png"), os.path.join("automatic_dataset", "temp", "img_1.png"))

    utils = Utils()
    formated_frames = utils.pproc_frame(df_anotation)
    pprint(formated_frames)

def test_pproc_frame_send_to_api(df_anotation):
    utils = Utils()
    frame = utils.pproc_frame(df_anotation)[0]
    pprint(frame)
    res = httpx.post(f"http://localhost/api-ia/dataset/frames/", files=frame, headers=headers, timeout=None)
    print (res.content)
    print ("!!!00")

    assert res.status_code == 200