from openerp import api, models, fields
from openerp.exceptions import except_orm

class ProductCustom(models.Model):
    _name = 'product.custom'

    name = fields.Char('Product Name', required=True)
    description = fields.Text('Product Description')
    price = fields.Float('Product Price', required=True)
    image = fields.Binary('Product Image')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status Product', default='draft')

    @api.multi
    def action_confirm(self):
        if not self.env.user.has_group('produk_price.group_junior_product_manager'):
            raise AccessError("You do not have permission to confirm.")
        self.write({'state': 'confirmed'})

    @api.multi
    def action_approve(self):
        if not self.env.user.has_group('produk_price.group_senior_product_manager'):
            raise AccessError("You do not have permission to approve.")
        self.write({'state': 'approved'})

    @api.multi
    def action_reject(self):
        if not self.env.user.has_group('produk_price.group_senior_product_manager'):
            raise AccessError("You do not have permission to reject.")
        self.write({'state': 'rejected'})

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
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ], string='Status Product', default='draft')

    confirmed_by = fields.Many2one('res.users', string='Confirmed By', readonly=True)
    approved_by = fields.Many2one('res.users', string='Approved By', readonly=True)
    rejected_by = fields.Many2one('res.users', string='Rejected By', readonly=True)
    viewed_by = fields.Many2many('res.users', string='Viewed By', readonly=True)

    @api.depends('product_id', 'quantity_amount')
    def _compute_total_price(self):
        for record in self:
            record.total_price = record.product_id.price * record.quantity_amount if record.product_id and record.quantity_amount else 0.0

    @api.depends('buyer_amount', 'total_price')
    def _compute_change(self):
        for record in self:
            record.change = record.buyer_amount - record.total_price if record.buyer_amount and record.total_price else 0.0

    @api.multi
    def action_confirm(self):
        if not self.env.user.has_group('produk_price.group_can_confirm'):
            raise except_orm("Permission Denied", "You do not have permission to confirm.")
        self.write({
            'state': 'confirmed',
            'confirmed_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]
        })

    @api.multi
    def action_approved(self):
        if not self.env.user.has_group('produk_price.group_can_confirm'):
            raise except_orm("Permission Denied", "You do not have permission to mark as done.")
        self.write({
            'state': 'approved',
            'approved_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]
        })

    @api.multi
    def action_reject(self):
        if not self.env.user.has_group('produk_price.group_can_reject'):
            raise except_orm("Permission Denied", "You do not have permission to reject.")
        self.write({
            'state': 'rejected',
            'rejected_by': self.env.user.id,
            'viewed_by': [(4, self.env.user.id)]
        })
