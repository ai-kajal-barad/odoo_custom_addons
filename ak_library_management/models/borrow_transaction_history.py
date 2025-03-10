# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
from odoo.exceptions import ValidationError


class BorrowTransactionHistory(models.TransientModel):
    """This class contains borrowed books
    transaction history."""
    _name = 'borrow.transaction.history'
    _description = ("This is class manage history "
                    "of borrowed books")
    _rec_name = 'customer_id'

    customer_id = fields.Many2one(string='Customer Name', comodel_name='res.partner')
    book_ids = fields.Many2many(comodel_name='product.template')
    borrow_start_date = fields.Datetime(string='Borrow Start Date',
                                        required=True, default=fields.Datetime.now)
    borrow_end_date = fields.Datetime(string="Borrow End Date", required=True)
    deposit_amount = fields.Float(string="Deposit Amount")
    is_member = fields.Boolean('res.partner', related='customer_id.is_member')
    not_trust_worthy = fields.Boolean('res.partner', related='customer_id.not_trust_worthy')

    @api.constrains('borrow_start_date', 'borrow_end_date')
    def date_constrains(self):
        """
        check end date is less than start date or not.
        param: none
        """
        for rec in self:
            if self.borrow_end_date < self.borrow_start_date:
                raise ValidationError("Sorry, End Date Must be greater than Start Date... ")

    def custom_wizard(self, message):
        """
        when we check any condition then return custom wizard.
        param: none
        """
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'borrow.transaction.history.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_message': message}
        }

    def action_confirm(self):
        """
        when we click confirm button then check conditions like customer is trustworthy or not,
        check product quantity,check books count
        param: none
        return: wizard
        """
        if self.customer_id.not_trust_worthy:
            message = "Customer is not trustworthy. Are you sure you want to continue?"
            return self.custom_wizard(message)

        product_list = [rec.name for rec in self.book_ids if rec.qty_available == 0]
        if product_list:
            message = (f"The following books are out of stock: {product_list}."
                       f" Are you sure you want to continue?")
            return self.custom_wizard(message)

        if len(self.book_ids) > 5:
            search_recd = self.search([('customer_id.id', "=", self.customer_id.id)],
                                      order='id desc', offset=1)
            books_name = []
            [books_name.append(book.name) for rec in search_recd
             for book in rec.book_ids if book.name not in books_name]

            if books_name:
                message = (f"Customer already has [{len(search_recd)}] open "
                           f"borrow transactions with {books_name} books. "
                           f"Are you sure you want to borrow more books?")
                return self.custom_wizard(message)

            message = ("Are you sure you want to allow "
                       "borrowing more than 5 books for this customer?")
            return self.custom_wizard(message)

        for rec in self.book_ids:
            if rec.qty_available:
                product_id = self.env['product.product'].search([('name', '=', rec.name),
                                                    ('default_code', '=', rec.default_code)])
                loc = self.env['stock.quant'].search([('product_id.name', '=', rec.name)], limit=1)
                self.env['stock.quant']._update_available_quantity(product_id, loc.location_id,
                                                                   quantity=-1)

    def reminder_borrow_book(self):
        """
        Borrow book remainder for customer if the borrow end date is within next 2 days and
        send the mail to the customer
        param: None
        return: None
        """
        all_recd = self.search([])
        for records in all_recd:
            date_deadline = records.borrow_start_date + timedelta(days=2)
            check_status = [rec.status == 'borrowed' for rec in records.book_ids]
            if (records.borrow_end_date == date_deadline and
                    any(check_status)):
                template = self.env.ref('ak_library_management.email_template_book_reminder')
                template.send_mail(records.id, force_send=True)

    def automated_action(self):
        """
        If customer has not return book before due date so that customer can't borrow
        more books.
        param: None
        return: Exception
        """
        search_rec = self.search([('customer_id.id', "=", self.customer_id.id)])
        for rec in search_rec[:-1]:
            for book in rec.book_ids:
                if rec.borrow_end_date < date.today() and book.status == "borrowed":
                    raise ValidationError(f"{rec.customer_id.name} with overdue books "
                                          f"cannot new ones until"
                                          f" you return the overdue items.")
