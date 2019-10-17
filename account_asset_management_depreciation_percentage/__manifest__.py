# Copyright 2015 AvanzOSC - Ainara Galdona
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2012-2019 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Asset Management Depreciation Percentage",
    "version": "11.0.1.0.1",
    "depends": [
        "account_asset_management",
    ],
    "conflicts": ['l10n_es_account_asset'],
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://odoo-community.org/",
    "category": "Accounting & Finance",
    "data": [
        "views/account_asset_profile_views.xml",
        "views/account_asset_views.xml",
    ],
    "installable": True,
    "development_status": "Production/Stable",
    "maintainers": ["pedrobaeza"],
}
