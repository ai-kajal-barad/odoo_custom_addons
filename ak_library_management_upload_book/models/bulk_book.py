#-*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class BulkBook(models.TransientModel):
    """This class creates multiple records for
    product.template model."""
    _name = 'bulk.book'
    _description = ("This is the bulk book class for "
                    "generating multiple books at a once")
    _rec_name='book_name'

    book_name=fields.Text(string='Book Title', help="Comma-separated book names")
    partner_id=fields.Many2one(string='Author Name', comodel_name='res.partner')
    product_ids=fields.Many2many(comodel_name='product.template')
    count_created_book=fields.Integer(string='Count Book',compute='_compute_book_count')

    def create_books(self):
        """This method creates new record for
        product.template"""
        if self.book_name:
            book_list=[book.strip() for book in self.book_name.split(',') if book.strip()]
            product_model=self.env['product.template']
            created_products=[]
            for book_name in book_list:
                existing_book= product_model.search([('name','=',book_name)],limit=1)
                if not existing_book:
                    product=product_model.create({'name':book_name,'is_bulk_book':True,
                                                  'author':self.partner_id.name})
                    created_products.append(product.id)
            if created_products:
                self.product_ids=created_products

    def revert_changes(self):
        """
        When click on revert changes button than this method is call and
        delete all current bulk books from product menu.
        """
        book_list = self.book_name.split(',')
        self.env["product.template"].search([("name", "in", book_list),
                                             ('is_bulk_book','=',True)]).unlink()

    @api.depends('book_name')
    def _compute_book_count(self):
        """count records that created by bulk.book """
        self.count_created_book = 0
        for rec in self:
            if rec.book_name:
                book_list = rec.book_name.split(',')
                count_book = self.env["product.template"].search([("name", "in", book_list),
                                                                  ("is_bulk_book", "=", True)])
                rec.count_created_book = len(count_book)

    @api.constrains('book_name')
    def _check_book_name(self):
        """Additional task:raise validation error"""
        for name in self.book_name:
            if name == ' ':
                raise ValidationError('Please Enter Valid Book Name.')

    def action_view_bulk_book(self):
        """method for smart button  that display
        single record  in form view and multiple in list-form"""
        if self.count_created_book == 1:
            product_id = self.env['product.template'].search([('name','=',self.book_name),
                                                              ("is_bulk_book", "=", True)])
            return {
                    'name':'Bulk Book',
                    'type':'ir.actions.act_window',
                    'res_model':'product.template',
                    'view_mode':'form',
                    'res_id': product_id.id,
            }
        else:
            return {
                    'name': 'Bulk Book',
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.template',
                    'view_mode': 'list,form',
                    'domain': [('name', 'in', self.book_name.split(',')),('is_bulk_book','=',True)],

            }
