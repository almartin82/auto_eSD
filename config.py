import yaml
import os
from os.path import expanduser


def _load_secrets(path=None):
    """
    Reads sensitive user credentials from the location provided, or from esd.yml file in user's home directory..

    Args:
        path (str): A path to a .yml file that contains credentials.  See `example_esd.yml` for details

    Returns:
        dict: A dictionary of private credential key/values
    """
    if path is None:
        path = os.path.join(expanduser('~'), 'esd.yml')

    with open(path, 'r') as f:
        data_map = yaml.safe_load(f)
    return data_map

secrets = _load_secrets(os.environ.get('ESD_CONFIG'))