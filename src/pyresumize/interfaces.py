class EmployerBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return []


class EducationBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return {}


class EmailBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class PhoneBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class NameBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class SkillBaseInterface:
    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return [""]
