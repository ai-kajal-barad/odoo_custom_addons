#-*- coding: utf-8 -*-
from odoo import models, fields, api,_
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    """Inherit sale order"""
    _inherit = 'sale.order'

    approval_needed = fields.Boolean(string="Approval Needed",
                                     compute="_compute_approval_needed", store=True)
    is_approved = fields.Boolean(string="Approved", default=False)

    @api.depends('order_line.product_id', 'order_line.product_uom_qty')
    def _compute_approval_needed(self):
        """compute value for approval needed field"""
        for order in self:
            low_stock_products = [line.product_id.name for line in order.order_line
                                  if line.product_id.qty_available < 5]
            order.approval_needed = bool(low_stock_products)

    def action_confirm(self):
        """override action confirm method"""
        self.ensure_one()
        if self.approval_needed and not self.is_approved:
            low_stock_products = [line.product_id.name for line in self.order_line
                                  if line.product_id.qty_available < 5]
            raise UserError(_("Approval needed! The following books have "
                              "low stock: %s" % ', '.join(low_stock_products)))
        return super().action_confirm()

    def action_approve(self):
        """method for confirmation"""
        if not self.env.user.is_manager:
            raise UserError(_("Only managers can approve orders."))
        self.is_approved = True

    def action_reject(self):
        """method for cancellation"""
        # if not self.env.user.is_manager:
        #     raise UserError(_("Only managers can reject orders."))
        self.action_cancel()
