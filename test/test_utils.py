import numpy as np
import pytest

from src.utils.image import ImageUtils
from src.utils.text import TextUtils


@pytest.mark.parametrize("in_image", [np.zeros((100, 100, 3), np.uint8)])
class TestImageUtils:

    def test_image_to_base64_and_base64_to_image(self, in_image):
        image_str = ImageUtils.image_to_base64(in_image)
        assert image_str is not None
        assert isinstance(image_str, str)

        image = ImageUtils.base64_to_image(image_str)
        assert image is not None
        assert image.shape == in_image.shape
        assert isinstance(image, np.ndarray)


class TestTextUtils:

    @pytest.mark.parametrize("in_data, out_data", [
        ("{'a': 1, 'b': 2}", {'a': 1, 'b': 2}),
        ("[1, 2, 3]", [1, 2, 3]),
        ("1", "1"),
        ("1.0", "1.0"),
        ("True", "True"),
        ("False", "False")
    ])
    def test_reformat_using_ast(self, in_data, out_data):
        assert TextUtils.reformat_using_ast(in_data) == out_data

    @pytest.mark.parametrize("in_data, out_data", [
        ("1.0", "1.0"),
        ("1", "1"),
        ("True", True),
        ("False", False),
        ("None", "None"),
        ("[1, 2, 3]", "[1, 2, 3]"),
        ("{'a': 1, 'b': 2}", "{'a': 1, 'b': 2}")
    ])
    def test_boolean_from_str_to_bool(self, in_data, out_data):
        assert TextUtils.boolean_from_str_to_bool(in_data) == out_data

    @pytest.mark.parametrize("in_data, out_data", [
        ("1.0", 1.0),
        ("1", 1),
        ("True", "True"),
        ("False", "False"),
        ("None", "None"),
        ("[1, 2, 3]", "[1, 2, 3]"),
        ("{'a': 1, 'b': 2}", "{'a': 1, 'b': 2}")
    ])
    def test_str_to_float(self, in_data, out_data):
        assert TextUtils.str_to_float(in_data) == out_data

    @pytest.mark.parametrize("in_data, out_data", [
        ("1.0", 1.0),
        ("1", 1),
        ("True", True),
        ("False", False),
        ("None", "None"),
        ("[1, 2, 3]", [1, 2, 3]),
        ("{'a': 1, 'b': 2}", {'a': 1, 'b': 2})
    ])
    def test_convert_str_to_data_type(self, in_data, out_data):
        assert TextUtils.convert_str_to_data_type(in_data) == out_data


