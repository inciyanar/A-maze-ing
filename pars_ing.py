from typing import Any
import os


class ConfigParser:
    """
    Handles loading, token parsing, structural validation of
    data parameters inside configuration files.
    Attributes:
        config_path (str): Location of text configurations.
        data (dict): Stored parameter records.
    """
    def __init__(self, config_path: str):
        """Initializes ConfigParser settings."""
        self.config_path: str = config_path
        self.data: dict[str, Any] = {}

    def parsing(self) -> None:
        """
        Reads files line by line, cleans syntax elements
        and stores config mappings.
        Skips comment lines prefixed with '#'.
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(
                f"Error: Config file not found: '{self.config_path}'"
            )
        with open(self.config_path, 'r', encoding="utf-8") as file:
            data: str = file.read()
            lines: list[str] = data.splitlines()
            for item in lines:
                item = item.strip()
                if not item or item[0] == '#':
                    continue
                if "=" not in item:
                    raise ValueError(
                        f"Value Error in {self.config_path}: Invalid syntax "
                        f"on line -> '{item}' (Missing '=')")
                splversion = item.split('=', 1)
                key = splversion[0].strip().upper()
                value = splversion[1].strip()
                self.data[key] = value
        for key, value in self.data.items():
            print(f"{key} = {value}")

    def check_data(self) -> None:
        """
        Runs type conversion checks, boundary assertions
        and flag validations across parameters.
        """
        mandatory_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                          "PERFECT"]
        for key in mandatory_keys:
            if key not in self.data:
                raise KeyError(f"Configuration Error: Mandatory key '{key}' is"
                               f" missing!")
        validated_data: dict[str, Any] = {}
        validated_data["OUTPUT_FILE"] = self.data["OUTPUT_FILE"]
        try:
            validated_data["WIDTH"] = int(self.data["WIDTH"])
            validated_data["HEIGHT"] = int(self.data["HEIGHT"])
        except ValueError:
            raise ValueError("Configuration Error: WIDTH and HEIGHT must be "
                             "integers!")

        try:
            entry_part = self.data["ENTRY"].split(",")
            exit_parts = self.data["EXIT"].split(",")
            validated_data["ENTRY"] = (int(entry_part[0]), int(entry_part[1]))
            validated_data["EXIT"] = (int(exit_parts[0]), int(exit_parts[1]))
        except (ValueError, IndexError):
            raise ValueError("Configuration Error: ENTRY and EXIT must be in "
                             "'x,y' integer format!")
        width = validated_data["WIDTH"]
        height = validated_data["HEIGHT"]
        entry = validated_data["ENTRY"]
        maze_exit = validated_data["EXIT"]

        if width <= 0 or height <= 0:
            raise ValueError("Configuration Error: Maze dimensions must be "
                             "greater than 0!")
        if not (0 <= entry[0] < width and 0 <= entry[1] < height):
            raise ValueError("Configuration Error: ENTRY coordinates are out "
                             "of maze bounds!")
        if not (0 <= maze_exit[0] < width and 0 <= maze_exit[1] < height):
            raise ValueError("Configuration Error: EXIT coordinates are out "
                             "of maze bounds!")

        perfect_str = str(self.data["PERFECT"]).upper()
        if perfect_str == "TRUE":
            validated_data["PERFECT"] = True
        elif perfect_str == "FALSE":
            validated_data["PERFECT"] = False
        else:
            raise ValueError("Configuration Error: PERFECT must be bool!")
        if "SEED" in self.data:
            try:
                validated_data["SEED"] = int(self.data["SEED"])
            except ValueError:
                raise ValueError("Configuration Error: SEED must "
                                 "be an integer!")
        self.data = validated_data
