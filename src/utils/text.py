import ast
from typing import Union, Any


class TextUtils:
    """Text utils"""

    @staticmethod
    def reformat_using_ast(data: str) -> Any:
        """
        Check if data is a dict, list, tuple, set, str
        then convert it to dict, list, tuple, set, str using ast.literal_eval
        :param data:
        :return: dict, list, tuple, set, str
        """
        if (data.startswith("{") and data.endswith("}")) or \
                (data.startswith("[") and data.endswith("]")) or \
                (data.startswith("(") and data.endswith(")")) or \
                (data.startswith("<") and data.endswith(">")):
            return ast.literal_eval(data)
        return data

    @staticmethod
    def boolean_from_str_to_bool(data: str) -> Union[bool, str]:
        """
        Convert string "True" to bool True and "False" to bool False else just return the data
        """
        return True if data == "True" else False if data == "False" else data

    @staticmethod
    def str_to_float(data: str) -> Union[int, float, str]:
        """
        Convert string to int
        if it's not int then convert to float
        else just return the data
        """
        try:
            if data.isnumeric():
                return int(data)
            return float(data)
        except ValueError:
            return data
        except AttributeError:
            return data

    @classmethod
    def convert_str_to_data_type(cls, data: str) -> Any:
        """
        Convert string to any data type
        :param data: str
        :return data: dict, list, tuple, set, str, float, int, bool
        """
        if isinstance(data, bytes):
            return data
        data = cls.reformat_using_ast(data)
        data = cls.str_to_float(data)
        data = cls.boolean_from_str_to_bool(data)
        return data



