from typing import Union

from src.core.keys import Encryption, Decryption
from src.utils.text import TextUtils


class ParsingUtils:
    """
    This class is used to parse a dictionary or list and encrypt or decrypt the values.
    :param obj: The dictionary or list to parse.
    :param method: The method to use to encrypt or decrypt the values.
    :return: The parsed dictionary or list.
    """

    @classmethod
    def parse_object(
            cls, obj: Union[dict, list], method: Union[Encryption, Decryption]
    ) -> Union[dict, list]:
        if isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict):
                    cls.parse_object(value, method)
                elif isinstance(value, list):
                    cls.parse_object(value, method)
                else:
                    obj[key] = TextUtils.convert_str_to_data_type(method.convert(value))

        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, dict):
                    cls.parse_object(item, method)
                elif isinstance(item, list):
                    cls.parse_object(item, method)
                else:
                    enc_item = TextUtils.convert_str_to_data_type(method.convert(item))
                    # replace the item in the list
                    obj[obj.index(item)] = enc_item

        return obj
