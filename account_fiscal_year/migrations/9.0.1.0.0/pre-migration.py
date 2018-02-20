# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


column_renames = {
    'account_fiscalyear': [
        ('date_stop', 'date_end'),
    ]}

table_renames = [
    ('account_fiscalyear', 'date_range'),
]

def drop_date_range(cr):
    cr.execute("drop table date_range_generator cascade")
    cr.execute("drop table date_range_type cascade")
    cr.execute("drop table date_range cascade")

def add_columns(cr):
    cr.execute("""SELECT column_name
        FROM information_schema.columns
        WHERE table_name='account_fiscalyear' AND
        column_name='type_id'""")
    if not cr.fetchone():
        cr.execute(
            """
            ALTER TABLE account_fiscalyear
            ADD COLUMN type_id
            integer;
            """)
    cr.execute("""SELECT column_name
        FROM information_schema.columns
        WHERE table_name='account_fiscalyear' AND
        column_name='type_name'""")
    if not cr.fetchone():
        cr.execute(
            """
            ALTER TABLE account_fiscalyear
            ADD COLUMN type_name
            char;
            """)

@openupgrade.migrate(use_env=True)
def migrate(env, version):
    drop_date_range(env.cr)
    add_columns(env.cr)
    openupgrade.rename_columns(env.cr, column_renames)
    openupgrade.rename_tables(env.cr, table_renames)
