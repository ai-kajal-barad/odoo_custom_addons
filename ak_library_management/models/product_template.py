# -*- coding: utf-8 -*-

from datetime import date, timedelta
from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Inherited class using for books"""
    _inherit = 'product.template'

    author = fields.Char(string='Author Name')
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Date of Publication')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string='ISBN Number')
    is_bulk_book = fields.Boolean(string='Is Bulk')
    display_name = fields.Char(string='Display Name', compute='compute_display_name')
    state = fields.Selection([('available', 'Available'),
                              ('unavailable', 'Unavailable'),
                              ('borrowed', 'Borrowed'),
                              ('returned', 'Returned')], string='Status',
                             tracking=True)

    def action_state_borrowed(self):
        """
        when this method call its change book status to borrowed and
        also schedule activity for the borrower.
        param: none
        """
        self.write({'state': 'borrowed'})
        # self.message_post(body=f'{self.env.user.name} is Borrowed On {date.today()}')
        date_deadline = date.today() + timedelta(days=10)
        return super().activity_schedule(date_deadline=date_deadline,
                                         summary=f'Book borrowed by {self.env.user.name}'
                                                 f' and return date {date_deadline}')

    def action_state_available(self):
        """
        when this method call its change book status to available.
        param: none
        """
        self.write({'state': 'available'})

    def action_state_returned(self):
        """
        Change Book State to return and pass log note in chatter.
        param: none
        """
        self.write({'state': 'returned'})
        self.message_post(body=f'The Book Returned by {self.env.user.name} on  {date.today()}')

    def action_borrow_books(self):
        """
        when we click borrow books button then redirect wizard action
        param: none
        """
        return {
            'name': 'Borrow Books',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.depends('name', 'author')
    def compute_display_name(self):
        """
        override compute display name and change book name format to [author_name] book_name.
        param: none
        """
        for rec in self:
            rec.display_name = f"{rec.name}-{rec.author}" if rec.name else rec.author

    @api.constrains('state')
    def _check_book_state(self):
        """
        send notification to the current user to status is changed and
        if status is borrowed then also pass log note in chatter.
        param: none
        """
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'title': 'Book Status',
            'type': 'warning',
            'message': f"Book Name:{self.name} Status: {self.state}",
        })
        if self.state == 'borrowed':
            self.message_post(body=f"{self.env.user.name} is borrowed the book and "
                                   f"the borrow date is {date.today()}")
