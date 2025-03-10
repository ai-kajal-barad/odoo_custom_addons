#-*- coding: utf-8 -*-

{
    'name': 'Library Management ',
    'version': '18.0.1.0.0',
    'summary': 'library management system borrow book',
    #'sequence': 10,
    'description': """
Its Basic Library management system""",
    'author':'Kajal Barad',
    'category': 'Sales/Sales',
    'website': 'https://www.aktivsoftware.com',
    'depends': ['web','product','sale_management','contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_form_view.xml',
        'views/res_partner_views.xml',
        'views/bulk_book_views.xml',
        'views/borrow_transaction_history.xml',
        'wizard/borrow_transaction_history_wizard_views.xml',
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
