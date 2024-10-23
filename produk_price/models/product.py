# -*- coding: utf-8 -*-
from openerp import api, models, fields, exceptions

class ProductCustom(models.Model):
    _name = 'product.custom'

    name = fields.Char('Product Name', required=True)
    description = fields.Text('Product Description')
    price = fields.Float('Product Price', required=True)
    image = fields.Binary('Product Image')


class ProductPurchase(models.Model):
    _name = 'product.purchase'

    product_id = fields.Many2one('product.custom', string='Product', required=True)
    buyer_amount = fields.Float('Buyer Amount', required=True)
    quantity_amount = fields.Integer('Total Quantity', required=True)
    total_price = fields.Float('Total Price', compute='_compute_total_price', store=True)
    change = fields.Float('Change', compute='_compute_change', store=True)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('rejected', 'Rejected')
    ], string='Approval State', default='draft')
    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    done_by = fields.Many2one('res.users', string='Done By', readonly=True)
    rejected_by = fields.Many2one('res.users', string='Rejected By', readonly=True)

    
    viewed_by = fields.Many2many('res.users', string='Viewed By', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.buyer_amount = self.product_id.price
            self.quantity_amount = 0
            self.total_price = 0.0

    @api.onchange('quantity_amount')
    def _onchange_quantity(self):
        if self.quantity_amount:
            self.total_price = self.product_id.price * self.quantity_amount

    @api.depends('product_id.price', 'quantity_amount')
    def _compute_total_price(self):
        for record in self:
            if record.quantity_amount and record.product_id:
                record.total_price = record.product_id.price * record.quantity_amount
            else:
                record.total_price = 0.0

    @api.depends('buyer_amount', 'total_price')
    def _compute_change(self):
        for record in self:
            if record.buyer_amount and record.total_price:
                record.change = record.buyer_amount - record.total_price
            else:
                record.change = 0.0


    @api.multi
    def action_confirm(self):
        if not self.env.user.has_group('produk_price.group_confirm_only'):
            raise exceptions.UserError("You do not have permission to confirm.")
        self.write({
            'state': 'confirmed',
            'confirmed_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]  # Adds the user who confirmed to viewed_by
        })

    # Modify action_done to log user who marked as done and allow other users to view
    @api.multi
    def action_done(self):
        if not self.env.user.has_group('produk_price.group_confirm_only'):
            raise exceptions.UserError("You do not have permission to mark as done.")
        self.write({
            'state': 'done',
            'done_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]  # Adds the user who marked as done to viewed_by
        })

    # Modify action_reject to log user who rejected and allow other users to view
    @api.multi
    def action_reject(self):
        if not self.env.user.has_group('produk_price.group_reject_only'):
            raise exceptions.UserError("You do not have permission to reject.")
        self.write({
            'state': 'rejected',
            'rejected_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]  # Adds the user who rejected to viewed_by
        })
