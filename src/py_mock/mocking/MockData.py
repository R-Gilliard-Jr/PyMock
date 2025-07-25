"""Class for mocking data"""

import os

import numpy as np
import pandas as pd

from py_mock.mocking.helper_functions import get_id_func, get_value_func


class MockData:
    def __init__(self, specs: dict):
        self.__specs = specs
        self.__extension = specs.get("extension")
        self.__file_name: str = specs.get("file_name", "")
        self.__data_frames: dict[str, pd.DataFrame] = {}

    def generate_rows(self, name: str, metadata: dict[str, dict]):
        def get_funcs(details: dict):
            id_ = details.get("id_")
            range_: list = details.get("range_", [])
            type_: str = details.get("type_", "")

            if id_:
                func = get_id_func(np.dtype(type_))
            else:
                func = get_value_func(type_, range_)

            return func

        base_row = {key: get_funcs(value) for key, value in metadata.items()}

        rows = []
        for i in range(500):
            new_row = {column: func() for column, func in base_row.items()}
            rows.append(new_row)

        self.__data_frames[name] = pd.DataFrame.from_records(rows)
        return self

    def generate_data(self):
        specs = self.__specs.copy()
        extension = specs.pop("extension")
        file_name = specs.pop("file_name")

        if extension == ".csv":
            for key, value in specs.items():
                self.generate_rows(file_name, value)
        # ADD LOGIC FOR EXCEL
        elif extension in [".xls", ".xlsx"]:
            pass

        return self

    def export(self, path: str):
        assert os.path.isdir(path), "Path is not a directory."

        out_path = os.path.join(path, f"{self.__file_name}{self.__extension}")

        if self.__extension == ".csv":
            self.__data_frames.get(self.__file_name, pd.DataFrame()).to_csv(
                out_path, index=False
            )
        elif self.__extension in [".xls", ".xlsx"]:
            pass
