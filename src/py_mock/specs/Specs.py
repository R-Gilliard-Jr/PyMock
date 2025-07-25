import json
import os
from functools import singledispatchmethod
from typing import MutableMapping, Self

import pandas as pd

from py_mock.utilities.string_utilities import clean_name


class Specs:
    _specs_path: str

    def __init__(self, path: str, instructions: MutableMapping = {}):
        self.__data: pd.DataFrame | pd.ExcelFile
        self.__specs: MutableMapping = {}
        self.__extension: str
        self.__name: str
        self.__raw_name: str
        self.__instructions: MutableMapping = instructions or {}

        name, extension = os.path.splitext(os.path.basename(path))
        self.__raw_name = name
        self.__name = clean_name(name)
        self.__specs["extension"] = self.__extension = extension
        self.__specs["file_name"] = self.__name

        if self.__extension == ".csv":
            self.__data = pd.read_csv(path)
        elif self.__extension in [".xls", ".xlsx"]:
            self.__data = pd.ExcelFile(path, engine="openpyxl")

        self.get_specs_path()

    @classmethod
    def get_specs_path(cls):
        current_dir = os.path.dirname(__file__)
        config_dir = os.path.join(current_dir, "..", "config")
        files = os.listdir(config_dir)
        if "paths.json" in files:
            with open(os.path.join(config_dir, "paths.json"), "r") as f:
                path_dict = json.load(f)
            specs_path = path_dict.get("specs_path")

        cls._specs_path = specs_path or current_dir

        return cls

    @singledispatchmethod
    def metadata_extractor(self, data: pd.DataFrame | pd.ExcelFile, name: str) -> Self:
        raise TypeError(
            f"Invalid type {type(data)}. Expected pd.DataFrame or pd.ExcelFile"
        )

    @metadata_extractor.register
    def _(self, data: pd.DataFrame, name: str) -> Self:
        def range_(series: pd.Series):
            type_ = series.dtype
            if type_ in [float, int]:
                output = [min(series), max(series)]
            else:
                output = []

            return output

        types = data.dtypes.map(lambda x: x.name)
        ranges = data.apply(range_, result_type="reduce")
        ids = data.columns.to_series().map(
            lambda x: 1 if x in self.__instructions.get("id", []) else 0
        )

        metadata = pd.concat([types, ranges, ids], axis=1)
        metadata.columns = ["type_", "range_", "id_"]

        self.__specs[name] = metadata.to_dict(orient="index")

        return self

    @metadata_extractor.register
    def _(self, data: pd.ExcelFile, name: str) -> Self:
        return self

    def extract_column_metadata(self) -> Self:
        if self.__extension == ".csv":
            self.metadata_extractor(self.__data, self.__name)
        elif self.__extension in [".xls", ".xlsx"]:
            for sheet in self.__data.sheet_names:
                data = pd.read_excel(self.__data, sheet_name=sheet)
                self.metadata_extractor(data, sheet)

        return self

    def export(self) -> Self:
        file_path = os.path.join(self._specs_path, f"_{self.__name}.json")
        with open(file_path, "w") as f:
            json.dump(self.__specs, f, indent=4)

        return self
