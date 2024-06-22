import os
import json
from typing import *
import toml
import tarfile
import ErrorHandler

from configparser import ConfigParser

config = ConfigParser()

class Settings:
    """
    A class to manage application settings.

    Args:
        settings_file (str): The path to the JSON settings file.

    Attributes:
        settings (dict): A dictionary containing the settings.
    """
    def __init__(self, settings_file:str) -> None:
        with open(settings_file, "r") as file:
            self.settings = json.load(file)

    def __getattr__(self, name:str):
        """
        Get the value of a setting.

        Args:
            name (str): The name of the setting to retrieve.

        Returns:
            Any: The value of the setting.
        """

        if name in self.settings:
            return self.settings[name]
        else:
            raise AttributeError(f"Setting '{name}' not found")

    def update_setting(self, name: str, value) -> None:
        """
        Update a setting.

        Args:
            name (str): The name of the setting to update.
            value: The new value of the setting.
        """
        if name in self.settings:
            self.settings[name] = value
        else:
            raise AttributeError(f"Setting '{name}' not found")

    def save_settings(self, settings_file: str) -> None:
        """
        Save the settings to the JSON file.

        Args:
            settings_file (str): The path to the JSON settings file.
        """
        with open(settings_file, 'w') as file:
            json.dump(self.settings, file, indent=4)

    def check_settings(self, required_settings: list) -> bool:
        """
        Check if all required settings are present.

        Args:
            required_settings (list): A list of required setting names.

        Returns:
            bool: True if all required settings are present, False otherwise.
        """
        for setting in required_settings:
            if setting not in self.settings:
                return False
        return True

    def make_setting(self, name: str, value) -> None:
        """
        Make a new setting.

        Args:
            name (str): The name of the setting to create.
            value: The value of the setting.
        """
        self.settings[name] = value

    def add_addon_desc(self, addon_name: str, desc_file: str) -> None:
        """
        Add an addon description to the settings.

        Args:
            addon_name (str): The name of the addon.
            desc_file (str): The path to the TOML addon description file.
        """
        with open(desc_file, 'r') as file:
            addon_desc = toml.load(file)
        self.settings['addons'][addon_name] = addon_desc

    def add_module_desc(self, module_name: str, desc_file: str) -> None:
        """
        Add a module description to the settings.

        Args:
            module_name (str): The name of the module.
            desc_file (str): The path to the TOML module description file.
        """
        with open(desc_file, 'r') as file:
            module_desc = toml.load(file)
        self.settings['modules'][module_name] = module_desc

    def content(self) -> str:
        return str(self.settings)

class _TOML_scanner:
    """
    This is a private class, please don't use this class.
    """
    def __init__(self, toml_path:str, DEFAULT_NAME:str="$AOL:useSETTINGS", DEFAULT_VERSION:str="$AOL:useSETTINGS", DEFAULT_DESC:str="This is a module/addon for AOL.", settings:Settings=None, type:str="Module") -> None:
        self.toml_path = toml_path

        if DEFAULT_NAME == "$AOL:useSETTINGS":
            if type.lower() == "module":
                self.DEFAULT_NAME = settings.MODULE["DEFAULT_NAME"]
            else:
                self.DEFAULT_NAME = settings.ADDON["DEFAULT_VERSION"]
        else:
            self.DEFAULT_NAME = DEFAULT_NAME
        if DEFAULT_NAME == "$AOL:useSETTINGS":
            if type.lower() == "module":
                self.DEFAULT_VERSION = settings.MODULE["DEFAULT_VERSION"]
            else:
                self.DEFAULT_VERSION = settings.ADDON["DEFAULT_VERSION"]
        else:
            self.DEFAULT_VERSION = DEFAULT_VERSION
        if DEFAULT_NAME == "$AOL:useSETTINGS":
            if type.lower() == "module":
                self.DEFAULT_DESC = settings.MODULE["DEFAULT_DESC"]
            else:
                self.DEFAULT_DESC = settings.ADDON["DEFAULT_VERSION"]
        else:
            self.DEFAULT_DESC = DEFAULT_DESC

        self.settings:Settings = settings

        self.metafile_data:dict = {}
        self.sections:dict = {}

    def scan(self) -> None:
        """
        Scan the AolProject.toml file and extract the data.
        """
        if not os.path.exists(self.toml_path):
            raise FileNotFoundError(f"AolProject.toml file not found. [{self.toml_path}]")

        toml_data = None

        with open(self.toml_path, 'r') as file:
            toml_file = toml.load(file)

        toml_data = toml_file.get("build", {})
        project_data = toml_file.get("project", {})

        #Extract data from TOML and save to self.metafile_data

        self.metafile_data["Name"] = toml_data.get("name", self.DEFAULT_NAME)
        self.metafile_data["Version"] = toml_data.get("version", self.DEFAULT_VERSION)
        self.metafile_data["Description"] = toml_data.get("desc", self.DEFAULT_DESC)
        self.metafile_data["Authors"] = toml_data.get("authors", [])
        self.metafile_data["Dependencies"] = toml_data.get("dependencies", {})

        readme = toml_data.get("readme", "")

        try:
            with open(os.path.join(os.path.dirname(self.toml_path), readme), 'r') as file:
                file.seek(0)
                self.metafile_data["Readme"] = file.read()
                file.close()
        except FileNotFoundError:
            raise FileNotFoundError(f"Readme file not found! Quitting! [{os.path.join(os.path.basename(self.toml_path), readme)}]")

        self.sections["build"] = toml_data
        self.sections["project"] = project_data

    def get_metadata(self) -> dict:
        """
        Get the metadata extracted from the TOML file.
        """
        return self.metafile_data, self.sections

class Builder:
    """
    A class to manage building addons and modules.

    Args:
        output_dir (str): The directory where the built files will be stored.
    """
    def __init__(self, output_dir: str, settings__:Settings) -> None:
        self.output_dir = output_dir
        self.settings__ = settings__

    def build_addon(self, addon_dir: str, addon_name: str) -> str:
        """
        Build an addon.

        Args:
            addon_dir (str): The base directory containing the main directory containing addon files.
            addon_name (str): The name of the addon.

        Returns:
            str: The path to the built addon file.

        Requires:
            The Main Directory should be named as the addon name
            The Base Directory should have these files -> (aolproject.toml, README.(md, txt), LICENSE, settings.json and the main Directory)
            The icon.(png, svg, jpeg, jpg) is not required.
        """
        addon_dir2 = addon_dir
        addon_dir = os.path.join(addon_dir, addon_name)

        if not os.path.exists(addon_dir):
            raise Exception(f"The Addon Base Dir doesn't contain the [{addon_name}] folder.")

        TOML_scanner = _TOML_scanner(os.path.join(addon_dir2, "aolproject.toml"), settings=self.settings__, type="addon")
        TOML_scanner.scan()

        toml_data, project_data = TOML_scanner.get_metadata()

        meta_file = os.path.join(addon_dir2, f"{self.addon_name}.aolMd")
        with open(meta_file, "w") as file:
            config.clear()
            config.add_section("MetaData")
            config.set("MetaData", "Name", str(toml_data["Name"]))
            config.set("MetaData", "Version", str(toml_data["Version"]))
            config.set("MetaData", "Description", str(toml_data["Description"]))
            config.set("MetaData", "Authors", str(toml_data["Authors"]))
            config.set("MetaData", "Dependencies", str(toml_data["Dependencies"]))
            config.set("MetaData", "Readme", str(toml_data["Readme"]))
            config.write(file)
            config.clear()

        addon_file = os.path.join(self.output_dir, f"{addon_name}.tar.gz")

        with tarfile.open(addon_file, "w:gz") as tar:
            tar.add(addon_dir, arcname=os.path.basename(addon_dir))
            tar.add(meta_file, arcname=os.path.basename(meta_file))

        if self.settings__.KEEP_METADATA_FILE == "False":
            os.remove(meta_file)
        elif self.settings__.KEEP_METADATA_FILE == "True":
            pass
        else:
            code = f'"KEEP_METADATA_FILE": "{self.settings__.KEEP_METADATA_FILE}"'
            ErrorHandler.BasicAExceptionHandler(code=code, specify=True, start_pos=23, end_pos=len(code) - 2, msg="Build Error: [The KEEP_META_DATA] key's value is not set to either [True, False]")

        return addon_file

    def build_module(self, module_dir: str, module_name: str) -> str:
        """
        Build a module.

        Args:
            module_dir (str): The directory containing the module files.
            module_name (str): The name of the module.

        Requires:
            The Main Directory should be named as the module name
            The Base Directory should have these files -> (aolproject.toml, README.(md, txt), LICENSE, settings.json and the main Directory)
            The icon.(png, svg, jpeg, jpg) is not required.

        Returns:
            str: The path to the built module file.
        """

        module_dir2 = module_dir
        module_dir = os.path.join(module_dir, module_name)

        if not os.path.exists(module_dir):
            raise Exception(f"The Module Base Dir doesn't contain the [{module_dir}] folder.")

        TOML_scanner = _TOML_scanner(os.path.join(module_dir2, "aolproject.toml"), settings=self.settings__, type="module")
        TOML_scanner.scan()

        toml_data, project_data = TOML_scanner.get_metadata()

        meta_file = os.path.join(module_dir2, f"{module_name}.aolMd")
        with open(meta_file, "w") as file__:
            config.clear()
            config.add_section("MetaData")
            config.set("MetaData", "Name", str(toml_data["Name"]))
            config.set("MetaData", "Version", str(toml_data["Version"]))
            config.set("MetaData", "Description", str(toml_data["Description"]))
            config.set("MetaData", "Authors", str(toml_data["Authors"]))
            config.set("MetaData", "Dependencies", str(toml_data["Dependencies"]))
            config.set("MetaData", "Readme", str(toml_data["Readme"]))
            config.write(file__)
            config.clear()

        module_file = os.path.join(self.output_dir, f"{module_name}.tar.gz")
        with tarfile.open(module_file, "w:gz") as tar:
            tar.add(module_dir, arcname=os.path.basename(module_dir))
            tar.add(meta_file, arcname=os.path.basename(meta_file))

        if self.settings__.KEEP_METADATA_FILE == "False":
            os.remove(meta_file)
        elif self.settings__.KEEP_METADATA_FILE == "True":
            pass
        else:
            code = f'"KEEP_METADATA_FILE": "{self.settings__.KEEP_METADATA_FILE}"'
            ErrorHandler.BasicAExceptionHandler(code=code, specify=True, start_pos=23, end_pos=len(code) - 2, msg="Build Error: [The KEEP_META_DATA] key's value is not set to either [True, False]")

        return module_file

def configure(settings_file: str, required_settings:list=["DEFAULT_RUNMODE", "DEFAULT_ENCODING", "DEFAULT_OUTPUT_DIR", "DEFAULT_OPTIMIZATION_LEVEL", "DEFAULT_DEBUG_LEVEL", "DEFAULT_TIMEOUT",
"VAR_DICT_FILE", "OBJ_DICT_FILE", "KEEP_METADATA_FILE"]) -> Settings:
    """
    Configure the settings object.

    Args:
        settings_file (str): The path to the JSON settings file.

    Returns:
        Settings: An instance of the Settings class initialized with the settings from the file.
    """
    required_settings:list = required_settings
    Settings_ = Settings(settings_file)

    if Settings_.check_settings(required_settings) == True:
        pass
    else:
        raise RuntimeError("REQUIRED Settings are missing from", settings_file)

    return Settings_