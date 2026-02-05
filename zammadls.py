#! /usr/bin/env python3
# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python
# pylint: disable=fixme

import sys
import logging
import argparse

# https://zammad-py.readthedocs.io/en/latest/usage.html
from zammad_py import ZammadAPI

import zammadls.zammadls

class LoggingAction(argparse.Action):
    # pylint: disable=redefined-outer-name
    def __call__(self, parser, namespace, values, option_string=None):
        logger = logging.getLogger()
        logger.setLevel(values)
        setattr(namespace, self.dest, values)

logger = logging.getLogger()
logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(levelname)-8s\t[%(name)s] %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

parser = argparse.ArgumentParser(
    description='zammad helper script',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

parser.add_argument(
    '-l', '--loglevel',
    help='set loglevel',
    type=str,
    choices=[k for k in list(logging.getLevelNamesMapping().keys()) if isinstance(k, str)],
    action=LoggingAction
    )

parser.add_argument(
    '-c','--config',
    nargs='+',
    action="append",
    help='config file'
    )

args = parser.parse_args()

logger.debug('config ...')
try:
    if args.config:
        configfiles = [item for sublist in args.config for item in sublist]
        cfg = zammadls.zammadls.ZammadlConfig(configfiles)
    else:
        cfg = zammadls.zammadls.ZammadlConfig()
except zammadls.zammadls.ZammadlConfigException as e:
    logger.fatal(e)
    sys.exit(1)

if not cfg.get('verify', True):
    urllib3.disable_warnings()

# init zammad
logger.info('zammad connection %s ...', cfg.get('baseurl'))
zammad = ZammadAPI(
    url=cfg.get('baseurl'),
    username=cfg.get('authuser', None),
    password=cfg.get('authpass', None),
    http_token=cfg.get('authtoken', None),
    )
zammad.session.verify = cfg.get('verify', True)  # ssl verification
logger.info('... connections established')
