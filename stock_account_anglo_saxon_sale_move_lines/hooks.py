# Copyright 2020 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.stock_account.models.product import ProductProduct
from odoo.addons.stock_account.models.account_invoice import AccountInvoice


def post_load_hook():
    def new_anglo_saxon_sale_move_lines(self, name, product, uom, qty, price_unit, currency=False, amount_currency=False, fiscal_position=False, account_analytic=False, analytic_tags=False, i_line=False):
        # FIRST HOOK STARTS
        if product._eligible_for_cogs(i_line):
            # FIRST HOOK ENDS
            accounts = product.product_tmpl_id.get_product_accounts(fiscal_pos=fiscal_position)
            # debit account dacc will be the output account
            dacc = accounts['stock_output'].id
            # credit account cacc will be the expense account
            cacc = accounts['expense'].id
            if dacc and cacc:
                # SECOND HOOK STARTS
                return product._prepare_product_anglo_saxon_sale_lines(name, product, uom, qty, price_unit, dacc, cacc, currency, amount_currency, fiscal_position, account_analytic, analytic_tags)
                # SECOND HOOK ENDS
        return []

    if not hasattr(
        ProductProduct, "anglo_saxon_sale_move_lines_original"
    ):
        ProductProduct.anglo_saxon_sale_move_lines_original = (
            ProductProduct._anglo_saxon_sale_move_lines
        )

    ProductProduct._anglo_saxon_sale_move_lines = (
        new_anglo_saxon_sale_move_lines
    )

    def new_account_invoice_anglo_saxon_sale_move_lines(self, i_line):
        inv = i_line.invoice_id
        company_currency = inv.company_id.currency_id
        price_unit = i_line._get_anglo_saxon_price_unit()
        if inv.currency_id != company_currency:
            currency = inv.currency_id
            amount_currency = i_line._get_price(company_currency, price_unit)
        else:
            currency = False
            amount_currency = False
        # THE HOOK
        return self.env['product.product']._anglo_saxon_sale_move_lines(i_line.name, i_line.product_id, i_line.uom_id, i_line.quantity, price_unit, currency=currency, amount_currency=amount_currency, fiscal_position=inv.fiscal_position_id, account_analytic=i_line.account_analytic_id, analytic_tags=i_line.analytic_tag_ids, i_line=i_line)

    if not hasattr(
        AccountInvoice, "anglo_saxon_sale_move_lines_original"
    ):
        AccountInvoice.anglo_saxon_sale_move_lines_original = (
            AccountInvoice._anglo_saxon_sale_move_lines
        )

    AccountInvoice._anglo_saxon_sale_move_lines = (
        new_account_invoice_anglo_saxon_sale_move_lines
    )
