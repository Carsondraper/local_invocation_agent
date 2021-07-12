import yaml
import logging
from os import path
from datetime import datetime

# Initializing the paths to the config files as class variables
lia_cfg_file = r'../conf/lia_config.yml'
log_cfg_file = r'../conf/lia_logger_config.yml'
default_log_dir = r'../log'
default_log_name = f'LIA_{datetime.strftime(datetime.today(), "%m_%d_%Y_%H_%M_%S")}.log'
log_level_dict = \
    {
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "FATAL": logging.FATAL
    }


class Configuration:
    """
    The class that handles all configuration parsing, config value storing, and application of said config values
    """
    def get_config(self):
        for config_file_path in [log_cfg_file, lia_cfg_file]:
            if path.isfile(config_file_path):
                # Opening the yml file
                stream = open(config_file_path, "r")
                logging.info(f'{config_file_path} has been opened')
                # loading the yml file's contents to a dictionary for parsing
                yaml_cfg_dict = yaml.safe_load(stream)
                logging.info(f'yaml config dictionary has been made')
                stream.close()
                logging.info(f'{config_file_path} has been closed')
                if config_file_path is log_cfg_file:
                    apply_configuration("log", yaml_cfg_dict)
                else:
                    lia_cfg = apply_configuration("lia", yaml_cfg_dict)
                    setattr(self, "lia_cfg", lia_cfg)
                    for k, v in lia_cfg.items():
                        setattr(self, k, v)
                        logging.info(f'Class instance variable {k} has been set to {v}')
                    return lia_cfg
            else:
                logging.error(f'The config yaml file expected to be at {config_file_path} '
                              f'is not present in the conf directory!')
                logging.info(f'The default config options will be applied')


def apply_configuration(cfg_name: str, config_file_dict: dict) -> dict:
    """
    The function that is used to validate and apply the configuration that is in the config files
    function then applies the configuration values to the class instance that is passed as a parameter as class
    instance variables.
    This is done by using .yml files and the python yaml module. We parse the yaml and convert it to a dict,
    then we grab the options that are expected and save them as class instance variables for the class
    """
    # Parsing the logging config file to log with the configured settings
    parsed_cfg = dict()
    if cfg_name == "log":
        cfg_dict = \
            {
                "log_dir": "DIRECTORY",
                "log_file_prefix": "FILENAMEPREFIX",
                "log_level": "LEVEL"
            }
        for variable, identifier in cfg_dict.items():
            config_value = value_from_dict_recursively(config_file_dict, identifier)
            if identifier == "DIRECTORY":
                if path.isdir(config_value):
                    logging.info(f'Logging Directory {config_value} exists')
                    absolute_path_directory = path.abspath(config_value)
                    logging.info(f'Absolute Path of {config_value} is {absolute_path_directory}')
                    parsed_cfg[variable] = absolute_path_directory
                else:
                    logging.error(f'Logging Directory {config_value} does not exist')
                    logging.info(f'Setting logging directory to default of {default_log_dir}')

            elif identifier == "FILENAMEPREFIX":
                parsed_cfg[variable] = config_value
                logging.info(f'FILENAMEPREFIX has been set to {config_value}')

            # The option that defines what logging level, logging will be taking place at
            elif identifier == "LEVEL":
                if config_value in log_level_dict.keys():
                    parsed_cfg[variable] = config_value
                    logging.info(f'Log Level configuration is set to {config_value}')
                else:
                    logging.error(f'The log level in the config file {config_value} is invalid')
                    logging.info(f'Valid configurations for the log level are '
                                 f'"INFO", "DEBUG", "WARNING", "ERROR", "FATAL"')
                    logging.info(f'Defaulting to log level of INFO')
                    parsed_cfg[variable] = "INFO"
        else:
            logging.info(f'Logging Configuration parse complete')
            datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")
            logging.basicConfig(level=parsed_cfg["log_level"],
                                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                                datefmt='%Y-%m-%d_%H:%M:%S',
                                filename=f'{parsed_cfg["log_dir"]}\\{parsed_cfg["log_file_prefix"]}_'
                                         f'{datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")}.log',
                                filemode='w')
            return parsed_cfg

    else:
        cfg_dict = \
            {
                "local_host_addr": "HOST",
                "local_host_port": "PORT",
                "api_host_addr": "API_HOST",
                "api_port": "API_PORT",
                "https": "HTTPS"
            }
        for variable, identifier in cfg_dict.items():
            config_value = value_from_dict_recursively(config_file_dict, identifier)
            if identifier == "HOST":
                parsed_cfg[variable] = config_value
                logging.info(f'The host to run the LIA is configured with a value of {config_value}')
            elif identifier == "PORT":
                parsed_cfg[variable] = config_value
                logging.info(f'The port the LIA is configured to run on is {config_value}')

            elif identifier == "API_HOST":
                parsed_cfg[variable] = config_value
                logging.info(f'The host that the api is configured to be on is {config_value}')
            elif identifier == "API_PORT":
                parsed_cfg[variable] = config_value
                logging.info(f'The port that the api is configured to be on is {config_value}')
            elif identifier == "HTTPS":
                parsed_cfg[variable] = config_value
                logging.info(f'The API HTTPS configuration option is {config_value}')
        else:
            logging.info(f'Configuration parse for the LOCAL and API Section is complete')
            return parsed_cfg


def value_from_dict_recursively(dictionary: dict, key: str) -> str:
    """
    Function that looks recursively in a dictionary and grabs the value for a specified key.
    """
    for k, v in dictionary.items():
        if k == key:
            return v
        elif isinstance(v, dict):
            value = value_from_dict_recursively(v, key)
            if value is not None:
                return value
            else:
                continue
        else:
            continue


if __name__ == '__main__':
    # The code to be ran upon startup of the application to read configuration settings in the yaml files
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d_%H:%M:%S',
                        filename=f'{path.abspath(default_log_dir)}\\{default_log_name}',
                        filemode='w')

    logging.error(f'{__file__} should not be ran as __main__. '
                  f'Please reference the documentation in order to run the LIA correctly')
    exit(1)
