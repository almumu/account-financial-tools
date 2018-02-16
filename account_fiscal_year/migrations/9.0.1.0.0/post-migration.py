# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


def insert_fy(env):
    fy_type = env['date.range.type'].search([
        ('fiscal_year', '=', True)], limit=1)
    env.cr.execute("""
    select name, date_start, date_stop
    from account_fiscal_year
    """)
    for (name, date_start, date_end) in env.cr.fetchall():
        env.cr.execute("""        
          INSERT INTO date_range 
            (name, date_start, date_end, date_range_type_id)
            VALUES ('%s', '%s', '%s', %s)
        """ % (name, date_start, date_end, fy_type.id))


def drop_obsolete(cr):
    cr.execute("drop table account_fiscal_year")


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    insert_fy(env)
    drop_obsolete(env.cr)
    print("This is all folks")
