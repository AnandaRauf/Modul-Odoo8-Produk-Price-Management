# -*- coding: utf-8 -*-
{
    'name': 'Custom Product Module',
    'version': '1.0',
    'category': 'Product',
    'description': 'Module to manage products with image, name, description, and price.',
    'author': 'Ananda Rauf Maududi',
    'depends': ['base','sale'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/product.xml',
        'views/sale_order_inherit_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
