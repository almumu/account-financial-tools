# Copyright 2019 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)
from odoo import api, models, _
from odoo.exceptions import ValidationError, UserError


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'account.document.reversal']

    @api.multi
    def action_invoice_cancel(self):
        """ If cancel method is to reverse, use document reversal wizard """
        if all(j.is_cancel_reversal for j in self.mapped('journal_id')) and \
                all(st == 'open' for st in self.mapped('state')):
            return self.reverse_document_wizard()
        return super().action_invoice_cancel()

    @api.multi
    def action_document_reversal(self, date=None, journal_id=None):
        """ Reverse all moves related to this invoice + set state to cancel """
        # Check document state
        if 'cancel' in self.mapped('state'):
            raise ValidationError(
                _('You are trying to cancel the cancelled document'))
        MoveLine = self.env['account.move.line']
        move_lines = MoveLine.search([('invoice_id', 'in', self.ids)])
        moves = move_lines.mapped('move_id')
        # Set all moves to unreconciled
        move_lines.filtered(
            lambda x: x.account_id.reconcile).remove_move_reconcile()
        # Create reverse entries
        moves.reverse_moves(date, journal_id)
        # Set state cancelled
        self.write({'move_id': False, 'state': 'cancel'})
        return True
