import ast


class TextUtils:

    @staticmethod
    def reformat_using_ast(data):
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
