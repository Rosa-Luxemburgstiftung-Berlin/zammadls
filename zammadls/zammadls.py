# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python

"""helper config functions for zammad helper scripts"""

import logging
import argparse
import urllib3
import hiyapyco

# https://zammad-py.readthedocs.io/en/latest/usage.html
from zammad_py import ZammadAPI

logger = logging.getLogger(__name__)


class LoggingAction(argparse.Action):
    """logger level helper class"""
    # pylint: disable=redefined-outer-name
    def __call__(self, parser, namespace, values, option_string=None):
        """logger level helper"""
        logger = logging.getLogger()
        logger.setLevel(values)
        setattr(namespace, self.dest, values)

class ZammadlConfigException(Exception):
    """dummy Exception raised on wrong config"""

class Zammadl:
    """zammad config and connection"""
    def __init__(self, parser):
        self.parser = parser
        self.args = self._argParse()
        self._config()
        self._connect()
        
    def _argParse(self):
        """set default args and parse"""
        self.parser.add_argument(
            '-l', '--loglevel',  
            help='set loglevel', 
            type=str,
            choices=[k for k in list(logging.getLevelNamesMapping().keys()) if isinstance(k, str)],
            action=LoggingAction 
            )
        self.parser.add_argument( 
            '-c','--config', 
            nargs='+',
            action="append", 
            help='config file'
            )
        return self.parser.parse_args()

    def _config(self):
        """setup config"""
        cfgfiles = ['config.yml', 'config/config.yml']
        if self.args.config:
            cfgfiles = [item for sublist in self.args.config for item in sublist]
        logger.info('loading config from: %s', ':'.join(cfgfiles))
        self.config = hiyapyco.load(
            cfgfiles, method=hiyapyco.METHOD_MERGE,
            usedefaultyamlloader=True,
            failonmissingfiles=False,
            loglevel=logging.ERROR)
        if not self.config:
            raise ZammadlConfigException('no config found')
        self._checkConfig()

        if not self.get('verify', True):
            urllib3.disable_warnings()

    def _checkConfig(self):
        if not 'baseurl' in self.config:
            raise ZammadlConfigException('missing baseurl')
        if not 'authtoken' in self.config:
            if not 'authuser' in self.config or not 'authpass' in self.config:
                raise ZammadlConfigException('missing auth')

    def _connect(self):
        logger.info('zammad connection %s ...', self.get('baseurl'))
        zammad = ZammadAPI(
            url=self.get('baseurl'),
            username=self.get('authuser', None),
            password=self.get('authpass', None),
            http_token=self.get('authtoken', None),
            )
        zammad.session.verify = self.get('verify', True)  # ssl verification
        logger.info('... connections established')
        return zammad

    def getZammadlConfig(self):
        return self.config

    def get(self, key, defaultvalue=None):
        """get a config value"""
        return self.config.get(key, defaultvalue)
