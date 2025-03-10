# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta
from odoo.exceptions import ValidationError, UserError


class BorrowTransactionHistory(models.TransientModel):
    """This class contains borrowed books
    transaction history."""
    _name = 'borrow.transaction.history'
    _description = ("This is class manage history "
                    "of borrowed books")
    _inherit = ['mail.activity.mixin']
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(string='Customer Name', comodel_name='res.partner')
    book_ids = fields.Many2many(comodel_name='product.template')

    borrow_start_date = fields.Datetime(string='Borrow Start Date',
                                        required=True, default=fields.Datetime.now)
    borrow_end_date = fields.Datetime(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean('res.partner', related='customer_id.is_member')
    not_trust_worthy = fields.Boolean('res.partner', related='customer_id.not_trust_worthy')

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def date_constrains(self):
        """books borrow end date must be lesser
        than borrow start date"""
        for rec in self:
            if self.borrow_end_date < self.borrow_start_date:
                raise ValidationError("Sorry, End Date Must be greater than Start Date... ")

    @api.onchange('customer_id')
    def _onchange_customer(self):
        """set default amount for customer
        is not member"""
        if self.customer_id and not self.customer_id.is_member:
            self.deposit_amount = 50.0
        else:
            self.deposit_amount = 0.0

    def action_check_trust_worthy(self):
        """check customer is trustworthy or not"""
        if not self.not_trust_worthy:
            raise UserError("Customer is not trustworthy. "
                            "Are you sure you want to continue?")

    def action_confirm(self):
        """check books stock"""
        out_of_stock_books = self.book_ids.filtered(lambda b: b.qty_available <= 0)
        if out_of_stock_books:
            raise UserError(f"The following books are out of stock: "
                            f"{', '.join(out_of_stock_books.mapped('name'))}")

    def total_borrow_book(self):
        """check total borrowed book by customers"""
        open_transactions = self.env['borrow.transaction.history'].search([
            ('customer_id', '=', self.customer_id.id),
            ('borrow_end_date', '>=', fields.Datetime.now()),
        ])
        total_borrowed_books = sum(len(t.book_ids) for t in open_transactions)
        if total_borrowed_books > 5:
            raise UserError(f"Customer already has 5 borrowed books."
                            f" Cannot exceed limit of 5.")
        self.env['borrow.transaction.history'].create({
            'customer_id': self.customer_id.id,
            'book_ids': [(6, 0, self.book_ids.ids)],
            'borrow_start_date': self.borrow_start_date,
            'borrow_end_date': self.borrow_end_date,
            'deposit_amount': self.deposit_amount if not self.customer_id.is_member else 0.0,
        })
        for book in self.book_ids:
            book.qty_available -= 1
        return {'type': 'ir.actions.act_window_close'}

    @api.constrains('book_ids')
    def _check_book_availability(self):
        """if book status is borrowed or unavailable than
        raise validationerror"""
        for record in self:
            unavailable_books = record.book_ids.filtered(
                lambda b: b.state in ['unavailable', 'borrowed'])
            if unavailable_books:
                raise ValidationError(
                    "The following books are unavailable or already borrowed: {}".format(
                        ", ".join(unavailable_books.mapped('name'))
                    )
                )
