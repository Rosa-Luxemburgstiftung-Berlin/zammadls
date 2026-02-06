#! /usr/bin/env python3
# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python
# pylint: disable=fixme

"""
Zammad helper script to delete or change tags

Example:
  ./retag.py -l INFO -t TESTREPLACETAG -a NEWREPLACETAG
"""

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
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

parser.add_argument('-t', '--tags',
    help='tag to remove',
    nargs='+',
    action="append",
    required=True
    )
parser.add_argument('-a', '--addtags',
    help='tag to add to all tickets that have the old tag',
    nargs='+',
    action="append",
    )

zammadl = zammadls.zammadls.Zammadl(parser)

# flatten tag list
removetags = [item for sublist in zammadl.args.tags for item in sublist]
logger.info('will remove tags %s', ', '.join(removetags))

addtags = []
if zammadl.args.addtags:
    # flatten tag list
    addtags = [item for sublist in zammadl.args.addtags for item in sublist]
if addtags:
    logger.info('will add tags %s', ', '.join(addtags))
    for ntag in addtags:
        zammadl.zammad.taglist.create({'name': ntag})

# check if tags exists
logger.info('fetching all tags from instance ...')
alltags = zammadl.zammad.taglist.all()
alltagnames = set([t['name'] for t in alltags])
rtags = list(set(removetags) - alltagnames)
for t in rtags:
    logger.warn('tag %s not found, ignoring', t)
    removetags.remove(t)
if rtags:
    logger.info('remaining tags to remove: %s', ', '.join(removetags))

for rtag in removetags:
    # fetch all tickets
    tickets = zammadl.zammad.ticket.search(f'tags:{rtag}')
    logger.info('tag %s : found %s tickets', rtag, len(tickets))
    for ticket in tickets:
        logger.debug('ticket id:%s ...', ticket['id'])
        if not zammadl.args.dryrun:
            zammadl.zammad.ticket_tag.remove(ticket['id'], rtag)
        logger.debug(' ... removed tag %s', rtag)
        for ntag in addtags:
            if not zammadl.args.dryrun:
                zammadl.zammad.ticket_tag.add(ticket['id'], ntag)
            logger.debug(' ... added tag %s', ntag)
