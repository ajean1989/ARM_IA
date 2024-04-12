import pytest
import io
import json

from PIL import Image

@pytest.fixture(scope="module")
def annotation():
    annotation = [
        {
                "label" : "Object",
                "label_int" : 0,
                "bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]
          },
          {
                "label" : "bla",
                "label_int" : 2,
                "bounding_box" : [0.11, 0.11, 0.45, 0.45]
          }
    ]

    return annotation

@pytest.fixture(scope="module")
def dict_annotation():
    annotation = [{"label" : "Object","label_int" : 0,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "bla","label_int" : 2,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]
    return annotation


@pytest.fixture(scope="module")
def binary_annotation():
    # annotation = b'[{"label" : "Object","label_int" : 0,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "bla","label_int" : 2,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]'
    annotation = [{"label" : "Object","label_int" : 0,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "bla","label_int" : 2,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]
    annotation = json.dumps(annotation)
    annotation = str(annotation) # transform le jsonObject en str
    annotation = bytes(annotation, "utf-8")
    return annotation

@pytest.fixture(scope="module")
def binary_annotation_1():
    # annotation = b'[{"label" : "bli","label_int" : 4,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "blo","label_int" : 3,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]'
    annotation = [{"label" : "bli","label_int" : 4,"bounding_box" : [0.11212, 0.11, 0.4564, 0.4546]},{"label" : "blo","label_int" : 3,"bounding_box" : [0.11, 0.11, 0.45, 0.45]}]
    annotation = json.dumps(annotation)
    annotation = str(annotation) # transform le jsonObject en str
    annotation = bytes(annotation, "utf-8")
    return annotation

@pytest.fixture(scope="module")
def binary_img():
    img = Image.open("app/tests/sample/img_1.png")
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()
    return imgbyte

@pytest.fixture(scope="module")
def binary_img_1():
    img = Image.open("app/tests/sample/img_2.png")
    imgbyte = io.BytesIO()
    img.save(imgbyte, format="png")
    imgbyte = imgbyte.getvalue()
    return imgbyte

@pytest.fixture(scope="module")
def binary_metadata():
    # metadata = b'{"dataset" : [0], "dataset_extraction" : "ARM", "pretreatment" : False, "data_augmentation" : False, "test" : True}'
    
    metadata = {"dataset" : [0], "dataset_extraction" : "ARM", "pretreatment" : False, "data_augmentation" : False, "test" : True}
    metadata = json.dumps(metadata)
    metadata = str(metadata) # transform le jsonObject en str
    metadata = bytes(metadata, "utf-8")
    return metadata

@pytest.fixture(scope="module")
def dict_metadata():
    metadata = {"dataset" : [0], "dataset_extraction" : "ARM", "pretreatment" : False, "data_augmentation" : False, "test" : True}
    return metadata
