# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': "Dimabru Website Product",
    'version': '1.0',
    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",
    'website': 'https://www.odoo.com/app/inventory',
    'category': 'Website/Website',
    'depends': [
        # Odoo
        'website',
        
        # Custom
        'dim_product',
        'dim_stock',
    ],
    'category': 'Inventory/Inventory',
    'author': 'Jonathan Lituma',
    'sequence': 26,
    'demo': [],
    'data': [
        # Views
        'views/menu_website.xml',
        'views/product_template_views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,
    'pre_init_hook': False,
    'post_init_hook': False,
    'license': 'LGPL-3',
    'assets': {},
}
