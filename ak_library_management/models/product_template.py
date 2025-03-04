# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date, timedelta


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
        """ This method for change
        state to borrowed"""
        self.write({'state': 'borrowed'})
        # self.message_post(body=f'{self.env.user.name} is Borrowed On {date.today()}')
        date_deadline = date.today() + timedelta(days=10)
        return super().activity_schedule(date_deadline=date_deadline,
                                         summary=f'Book borrowed by {self.env.user.name}'
                                                 f' and return date {date_deadline}')

    def action_state_available(self):
        """This method for change
        state to available"""
        self.write({'state': 'available'})

    def action_state_returned(self):
        """This method for change
        state to reserved"""
        self.write({'state': 'returned'})
        self.message_post(body=f'{self.env.user.name} is return book. Date: {date.today()}')

    def action_borrow_books(self):
        return {
            'name': 'Borrow Books',
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.transaction.history',
            'view_mode': 'form',
            'target': 'new',
        }

    @api.depends('name', 'author')
    def compute_display_name(self):
        for rec in self:
            rec.display_name = f"{rec.name}-{rec.author}" if rec.name else rec.author

    @api.constrains('state')
    def _check_book_state(self):
        """notify when book status changed"""
        self.env['bus.bus']._sendone(self.env.user.partner_id, 'simple_notification', {
            'title': 'Book Status',
            'type': 'warning',
            'message': f"Book Name:{self.name} Status: {self.state}",
        })
