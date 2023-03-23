class EmployerBaseInterface:
    """Idenify the previous employers"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return []


class EducationBaseInterface:
    """Interface to fetch the education , graduation year and university"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return {}


class EmailBaseInterface:
    """Interface to parse the Email address"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class PhoneBaseInterface:
    """Interface to parse Phone number from resume"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class NameBaseInterface:
    """Interface to parse the name in the resume"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return ""


class SkillBaseInterface:
    """Interface to parse the Skills in a resume"""

    def __init__(self, config_folder) -> None:
        self.config_folder = config_folder
        pass

    def process(self, extracted_text):
        """does nothing"""
        return [""]
