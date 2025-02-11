#-*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    is_library_book=fields.Boolean(string='Is Library Book')
    author=fields.Char(string='Author Name')
    publisher=fields.Char(string='Publisher')
    edition=fields.Char(string='Edition')
    published_date=fields.Date(string='Date of Publication')
    pages=fields.Integer(string='Pages')
    available = fields.Boolean(string='Available')
    isbn = fields.Char(string="ISBN Number")
    state=fields.Selection([('available','Available'),('borrowed','Borrowed'),('reserved','Reserved')],string='Status',tracking=True,default="available")
    @api.constrains('sale_ok','is_library_book')
    def _check_required_field(self):
        """Check for invalid fields based on sale_ok and
        is_library_book fields are true or not."""
        for rec in self:
            if rec.sale_ok and  rec.is_library_book:
                required_fields=['author','publisher','edition','published_date',
                                 'pages','available','isbn']
                missing_fields=[fields for fields in required_fields if not rec[fields] ]
                if missing_fields:
                    raise ValidationError(f"Invalid Fields:{missing_fields}")

    @api.onchange('barcode')
    def _onchange_barcode(self):
        """field isbn assign to barcode"""
        if self.sale_ok:
            self.barcode=self.isbn

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