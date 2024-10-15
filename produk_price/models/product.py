# -*- coding: utf-8 -*-
from openerp import models, fields

class ProductCustom(models.Model):
    _name = 'product.custom'

    name = fields.Char('Product Name', required=True)
    description = fields.Text('Product Description')
    price = fields.Float('Product Price', required=True)
    image = fields.Binary('Product Image')
