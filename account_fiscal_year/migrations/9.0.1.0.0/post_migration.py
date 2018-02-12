# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade
import logging
from openerp.api import Environment
from openerp import SUPERUSER_ID

logger = logging.getLogger(__name__)


def assign_range_type(env):
    fy_type = env['date.range.type'].search([
        ('fiscal_year', '=', True)], limit=1)
    query = """
        update date_range set date_range_type_id = %s
    """ % fy_type
    openupgrade.logged_query(env.cr, query)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    assign_range_type(env)
