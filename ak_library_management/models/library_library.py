# -*- coding: utf-8 -*-
from odoo import models, fields, api


class Library(models.Model):
    """This class contain library related details."""
    _name = 'library.library'
    _description = "This is the library class."
    _inherit = ['mail.thread']

    name = fields.Char(string='Library')
    location = fields.Char(string='Location')
    capacity = fields.Integer(string='Capacity')
    notes = fields.Text(string='notes')
    product_ids = fields.Many2many(string='Products', comodel_name='product.template')
    librarian_id = fields.Many2one(string="Librarian", comodel_name='res.users',
                                   tracking=True)

    """sql constrains for library name"""
    _sql_constraints = [('name_unique', 'unique(name)', 'Library Name is Unique.')]

    @api.constrains('product_ids')
    def _check_book_ids(self):
        """
        send notification to librarian if books is
         add or delete in many2many field.
        """
        for book in self.product_ids:
            self.env['bus.bus']._sendone(self.librarian_id.partner_id, 'simple_notification', {
                'type': 'success',
                'message': f"In library[{book.name}] book list are updated.",
            })
