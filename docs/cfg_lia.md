<h1>cfg_lia.py</h1>
cfg_lia is only intended to be ran by lia.py
<br>
Attempting to run the file as main will result in an error<br>
<h2>PyYAML</h2>
cfg_lia.py makes use of the PyYAML module in order to parse the conf yaml files for option values.
<br>
The .yml files are the following
<br>

``````
local_invocation_agent/conf/lia_config.yml
local_invocation_agent/conf/lia_logger_config.yml
``````
The defaults for these config files are the following:
<h3>lia_config.yml</h3>
``````
# The Configuration file for the LIA
# Keep in mind that changing any of the option values to an incorrect value will result in the LIA using the default value for the respective option
# More info on this config file can be found in the docs directory
LOCAL:
  # The machine this file is on. Host must either be FQDN or IP Addr
  HOST: localhost
  # The port you would like the LIA to run, and listen for requests for the Backend on
  PORT: 7331
API:
  # The host that has the Automated health check api running
  API_HOST: localhost
  # The port that the api is on
  API_PORT: 1337
  # HTTPS Enabled or disabled. Valid settings for this option would be True, and False
  HTTPS: False
``````

<h3>lia_logger_config.yml</h3>
``````
# The config file for logging configuration.
LOGGER:
  # You can use a relative file path or a absolute file path (Both D:\log\lia\ and ../../logs work!)
  DIRECTORY: ../log
  # The FILENAMEPREFIX is the log's prefix prior to the log file name (ie. a value of LIA would generate log files with
  # LIA_07_07_2000_01_35_00.log)
  FILENAMEPREFIX: LIA
  # LEVEL options are INFO | DEBUG | ERROR | FATAL | WARNING
  # INFO is recommended as DEBUG Logs are very hard to read
  LEVEL: INFO
``````

<h2>get_config()</h3>

calling the get_config method  that resides in Configuration, the class checks for the expected .yml files in the conf dir
returns a dictionary.
<br>
Said Dictionary includes the values that are needed by components of the LIA
``````
cfg_cls = Configuration()
cfg_cls.get_config()

Output:
{
    'local_host_addr': 'localhost',
    'local_host_port': 7331,
    'api_host_addr': 'localhost',
    'api_port': 1337,
    'https': False
}
``````


