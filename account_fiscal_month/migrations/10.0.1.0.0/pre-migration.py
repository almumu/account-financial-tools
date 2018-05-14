# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


def copy_from_account_period(env):
    env.cr.execute("""
        select name, date_start, date_stop
        from account_period
        where special = false
    """)
    for (name, date_start, date_stop) in env.cr.fetchall():
        env.cr.execute("select id from date_range where name = '%s'" % name)
        if not env.cr.fetchone():
            env.cr.execute("""
            INSERT into date_range (id, name, date_start, date_end, type_id, active, company_id, state)
            VALUES ((SELECT MAX(id) FROM date_range)+1, '%s', '%s', '%s', 2, true, 1, 'draft')        
            """ % (name,  date_start, date_stop))


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    copy_from_account_period(env)
