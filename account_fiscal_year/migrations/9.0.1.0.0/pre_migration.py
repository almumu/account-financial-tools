# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)
from openupgradelib import openupgrade


_table_renames = [
    ('account_fiscalyear', 'date_range'),
]

column_renames = {
    'crm_claim': [('description', 'comment'),
                  ('date', 'date_rma'),
                  ],
    'account_fiscalyear': [
        ('date_stop', 'date_end'),
    ]}


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    openupgrade.rename_columns(env.cr, column_renames)
    openupgrade.rename_tables(env.cr, _table_renames)
