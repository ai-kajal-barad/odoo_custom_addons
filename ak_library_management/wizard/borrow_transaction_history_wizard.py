# -*- coding: utf-8 -*-

from odoo import models, fields


class BorrowTransactionHistory(models.TransientModel):
    """
    This is Transient model and redirect when confirm button is clicked.
    """
    _name = 'borrow.transaction.history.wizard'
    _description = 'borrow transaction history wizard'

    message = fields.Text(string='Error:')

    def action_cancel(self):
        """
        when click cancel button then current record is deleted.
        """
        rec_id = self.env.context.get('active_id')
        self.env["borrow.transaction.history"].browse(rec_id).unlink()
