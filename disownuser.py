#! /usr/bin/env python3
# vim: set fileencoding=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent ft=python
# pylint: disable=fixme

"""
Zammad helper script to migrate all tickets and articles from one user to another

Example:
  ./disownuser.py -l INFO -u email -o fresh.fruit@rotting.vegetables -t this.machine@kills.fascists
"""

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
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
    )

parser.add_argument('-u', '--userident',
    help='field name to identify users',
    type=str,
    choices=['id', 'login', 'email'],
    default='login'
    )
parser.add_argument('-o', '--originaluser',
    help='from users',
    type=str,
    required=True)
parser.add_argument('-t', '--targetuser',
    help='to users',
    type=str,
    required=True)
parser.add_argument('-d', '--delete',
    help='delete the original user after all',
    action="store_true"
    )
parser.add_argument('-D', '--disable',
    help='disable the original user after all',
    action="store_true"
    )

try:
    zammadl = zammadls.zammadls.Zammadl(parser)
except zammadls.zammadls.ZammadlConfigException as e:
    logger.fatal(e)
    sys.exit(1)

if zammadl.args.delete and zammadl.args.disable:
    logger.fatal('delete and disable are mutualy exclusive')
    sys.exit(2)

# search user
userf = zammadl.get_user(zammadl.args.originaluser, zammadl.args.userident)
logger.debug('originaluser id: %s', userf['id'])
usert = zammadl.get_user(zammadl.args.targetuser, zammadl.args.userident)
logger.debug('zammadl.args.targetuser id: %s', usert['id'])

transform_ticket_elements = ['owner_id', 'customer_id', 'created_by_id', 'updated_by_id']
transform_article_elements = ['created_by_id', 'origin_by_id', 'sender_id', 'updated_by_id']
# ? created_by, updated_by

# get all stuff related to userf
# TODO: diff between search and find?
tickets = zammadl.zammad.ticket.search(userf['login'])
logger.info('found %s tickets to process', len(tickets))
for ticket in tickets:
    logger.info('processing ticket id:%s title:"%s" ...', ticket['id'], ticket['title'])
    # update user id references in tickets"""
    # https://docs.zammad.org/en/latest/api/ticket/index.html
    update_ticket = False
    for k in transform_ticket_elements:
        logger.debug('... check %s (%s) ...', k, ticket[k])
        if ticket[k] == userf['id']:
            logger.info('... will update %s for ticket id:%s', k, ticket['id'])
            ticket[k] == usert['id']
            update_ticket = True
        if update_ticket and not zammadl.args.dryrun:
            logger.debug('... run update for ticket id:%s title:"%s" ...', ticket['id'], ticket['title'])
            zammadl.zammad.ticket.update(id=ticket['id'], params=ticket)
    if ticket['article_count'] > 0:
        # process articles
        ticket_articles = zammadl.zammad.ticket.articles(ticket['id'])
        for article in ticket_articles:
            update_article = False
            logger.info('processing article id:%s for ticket id:%s ...', article['id'], ticket['id'])
            for k in transform_article_elements:
                logger.debug('... check %s (%s) ...', k, article[k])
                if article[k] == userf['id']:
                    logger.info('... will update %s for article id:%s', k, article['id'])
                    article[k] = usert['id']
                    update_article = True
            if update_article and not zammadl.args.dryrun:
                logger.debug('... run update for article id:%s (ticket id:%s)',  article['id'], ticket['id'])
                zammadl.zammad.ticket_article.update(id=article['id'], params=article)

# todo: set updated_by_id to me().id ?
