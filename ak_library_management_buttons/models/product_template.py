#-*- coding: utf-8 -*-
from odoo import models, fields


class ProductTemplate(models.Model):
    """inherit product.template for books """

    _inherit = 'product.template'

    is_library_book=fields.Boolean(string='Is Library Book')
    author=fields.Char(string='Author Name')
    publisher=fields.Char(string='Publisher')
    edition=fields.Char(string='Edition')
    published_date=fields.Date(string='Date of Publication')
    pages=fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string="ISBN Number")
    state=fields.Selection([('available','Available'),('borrowed','Borrowed'),
                            ('reserved','Reserved')],string='Status',
                           tracking=True,default="available")

    def action_state_borrowed(self):
        """ This method for change
    	state to borrowed"""
        self.write({'state': 'borrowed'})

    def action_state_available(self):
        """This method for change
    	state to available"""
        self.write({'state':'available'})

    def action_state_reserved(self):
        """This method for change
        state to reserved"""
        self.write({'state':'reserved'})
