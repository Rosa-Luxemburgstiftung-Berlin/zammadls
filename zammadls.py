#! /usr/bin/env python3
# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python
# pylint: disable=fixme

import sys
import logging
import argparse
import zammadls.config

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
        cfg = zammadls.config.ZammadlConfig(configfiles)
    else:
        cfg = zammadls.config.ZammadlConfig()
except zammadls.config.ZammadlConfigException as e:
    logger.fatal(e)
    sys.exit(1)

