# -*- coding: utf-8 -*-
{
    'name': "Movimientos de los usuarios",
    'summary': """
       saldo app""",
    'description': """
        Creacion de movimientos de los diferentes usuarios
    """,
    'author': "jonathan lituma",
    'website': "jonathanpaulbby@gmail.com",
    'category': 'Tools',
    'version': '0.1',
    # any module necessary for this one to work correctly
    'depends': ['base','mail'],
    # always loaded
    'data': [

        'security/res_groups.xml',
        'security/ir_rule.xml',
'security/ir.model.access.csv',
        'views/views.xml',
        'report/report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'license': 'OPL-1',
}
