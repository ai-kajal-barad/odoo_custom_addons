# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    """Inherited class using for books"""
    _inherit = 'product.template'

    author = fields.Char(string='Author Name', required=True)
    publisher = fields.Char(string='Publisher')
    edition = fields.Char(string='Edition')
    published_date = fields.Date(string='Date of Publication')
    pages = fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string='ISBN Number')
    is_bulk_book = fields.Boolean(string='Is Bulk')
    display_name = fields.Char(string='Display Name', compute='compute_display_name')

    @api.depends('name', 'author')
    def compute_display_name(self):
        """
        using compute display name method change book name format to
        [author_name]book_name.
        param: none
        """
        for rec in self:
            rec.display_name = f"[{rec.author}]{rec.name}" if rec.name else rec.author

    @api.model
    @api.readonly
    def name_search(self, name='', args=None, operator='ilike', limit=None):
        """
        override name_search method to search book by author name.
        param: name, args, operator, limit
        """
        args = list(args or [])
        if name:
            args += [('author', operator, name)]
        return super().name_search(args=args, limit=limit)

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
