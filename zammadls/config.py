# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python

"""helper config functions for zammad helper scripts"""

import logging
import hiyapyco

logger = logging.getLogger(__name__)

class ZammadlConfigException(Exception):
    """dummy Exception raised on wrong config"""

class ZammadlConfig:
    """handle config"""
    def __init__(self, cfgfiles=['config.yml', 'config/config.yml']):
        self.config = hiyapyco.load(
            cfgfiles, method=hiyapyco.METHOD_MERGE,
            usedefaultyamlloader=True,
            failonmissingfiles=False,
            loglevel=logging.ERROR)
        if not self.config:
            raise ZammadlConfigException('no config files found')
        self._checkConfig()

    def _checkConfig(self):
        if not 'baseurl' in self.config:
            raise ZammadlConfigException('missing baseurl')
        if not 'authtoken' in self.config:
            if not 'authuser' in self.config or not 'authpass' in self.config:
                raise ZammadlConfigException('missing auth')
