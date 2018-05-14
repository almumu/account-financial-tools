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


def restore_table(cr):
    cr.execute(
        """
        SELECT table_name FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        AND table_name = 'account_fiscalyear'
        """
    )
    if not cr.fetchone():
        cr.execute("""
            select * into account_fiscalyear from legacy_account_fiscalyear;
        """)


def date_range_primary_key(cr):
    cr.execute("""
    SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
    FROM   pg_index i
    JOIN   pg_attribute a ON a.attrelid = i.indrelid
                         AND a.attnum = ANY(i.indkey)
    WHERE  i.indrelid = 'date_range'::regclass
    AND    i.indisprimary;
    """)
    if not cr.fetchone():
        cr.execute("""
            ALTER TABLE date_range drop constraint date_range_pkey cascade;
            ALTER TABLE date_range ADD PRIMARY KEY (id);
            CREATE SEQUENCE date_range_id_seq;
            SELECT setval('date_range_id_seq', (SELECT MAX(id) FROM date_range))              
        """)


@openupgrade.migrate(use_env=True)
def migrate(env, version):
    drop_date_range(env.cr)
    restore_table(env.cr)
    add_columns(env.cr)
    openupgrade.rename_columns(env.cr, column_renames)
    openupgrade.rename_tables(env.cr, table_renames)
    date_range_primary_key(env.cr)
