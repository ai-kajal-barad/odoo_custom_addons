#-*- coding: utf-8 -*-

from odoo import models, fields, api


class BulkBook(models.TransientModel):
    """This class creates multiple records for
    product.template model."""
    _name = 'bulk.book'
    _description = "This is the books class for managing the books"
    _rec_name='book_name'

    book_name=fields.Text(string='Book Title', help="Comma-separated book names")
    partner_id=fields.Many2one(string='Author Name', comodel_name='res.partner')
    product_ids=fields.Many2many(comodel_name='product.template')
    count_product=fields.Integer(string='Count Book',compute='_compute_book_count')

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
        """This method use to delete existing records
        from product.template"""
        if self.product_ids:
            product_un=self.env['product.template'].search([('id','in',self.product_ids.ids)])
            if product_un:
                product_un.unlink()

    @api.depends('product_ids')
    def _compute_book_count(self):
        """count records that created by bulk.book """
        for rec in self:
            rec.count_product=self.env['product.template'].search_count([('is_bulk_book','=',True)])

    def action_view_bulk_book(self):
        """method for smart button  that display
        single record  in form view and multiple in list-form"""
        if self.product_ids:
            if len(self.product_ids) == 1:
                return {
                    'name':'Bulk Book',
                    'type':'ir.actions.act_window',
                    'res_model':'product.template',
                    'view_mode':'form',
                    'domain':[('is_bulk_book','=', True)],
                }
            else:
                return {
                    'name': 'Bulk Book',
                    'type': 'ir.actions.act_window',
                    'res_model': 'product.template',
                    'view_mode': 'list,form',
                    'view_types':'list,form',
                    'domain': [('is_bulk_book', '=', True)],
                }
