#-*- coding: utf-8 -*-
from odoo import models, fields, api


class Library(models.Model):
    """This class contain library related details."""
    _name = 'library.library'
    _description = "This is the library class."

    name=fields.Char(string='Book Title')
    location=fields.Char(string='Location')
    capacity=fields.Integer(string='Capacity')
    notes=fields.Text(string=' notes')
    product_ids = fields.Many2many(string='Products',comodel_name='product.template')
    member_id=fields.Many2one(comodel_name='library.member')
    borrow_book_count=fields.Integer( string="Book Count", compute='_compute_book_count')

    @api.depends('product_ids.state')
    def _compute_book_count(self):
        """compute method for count books"""
        for rec in self:
            rec.borrow_book_count=len(rec.product_ids.filtered(
                lambda p: p.state == 'borrowed'))

    def action_view_borrow_book(self):
        """method for smart button"""
        self.ensure_one()
        return {
            'name':'Borrowed Book',
            'type':'ir.actions.act_window',
            'res_model':'product.template',
            'view_mode':'list,form',
            'domain':[('state','=','borrowed')],
        }
