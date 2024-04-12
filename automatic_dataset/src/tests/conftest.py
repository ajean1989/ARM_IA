import pytest
import pandas as pd


@pytest.fixture(scope="module")
def df_anotation():
    data = {"name" : ["img_1.png", "img_1.png"],
            "id" : [0, 0],
            "bbxyxy" : [[127.5644, 381.28894, 576.30804, 1130.9819], [127.5, 381.2, 576.3, 1130.9]],
            "bbxywhn" : [[0.48879853, 0.5907308, 0.62325896, 0.58569756], [0.48, 0.59, 0.6, 0.5]],
            "code" : [1515, 1414]}
    df = pd.DataFrame(data=data)
    return df

