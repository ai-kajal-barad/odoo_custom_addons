#-*- coding: utf-8 -*-

from odoo import models, fields, api,_


class ProductTemplate(models.Model):
    """Inherited class using for books"""

    _inherit = 'product.template'

    author=fields.Char(string='Author Name')
    publisher=fields.Char(string='Publisher')
    edition=fields.Char(string='Edition')
    published_date=fields.Date(string='Date of Publication')
    pages=fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string="ISBN Number")
    is_bulk_book=fields.Boolean(string='Is Bulk')
    default_code=fields.Char(string='Reference')

    @api.model_create_multi
    def create(self, vals_list):
        """create sequence for reference field in
        product.template model"""
        for vals in vals_list:
            if not vals.get('default_code') or vals['default_code'] == _('New'):
                vals['default_code'] = (self.env['ir.sequence'].next_by_code
                                        ('product.template') or _('New'))
        return super().create(vals_list)
