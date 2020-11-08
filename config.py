import configparser


def get_config(section=None):
    config = configparser.ConfigParser()
    config.read("config.ini")

    if section:
        return config[section]
    return config
