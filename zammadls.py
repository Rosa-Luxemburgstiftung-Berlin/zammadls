#! /usr/bin/env python3
# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python
# pylint: disable=fixme

import sys
import logging
import argparse

import zammadls.zammadls

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.WARN,
    format='%(asctime)s %(levelname)-8s\t[%(name)s] %(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
    )

parser = argparse.ArgumentParser(
    description='zammad helper script',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

zammadl = zammadls.zammadls.Zammadl(parser)

