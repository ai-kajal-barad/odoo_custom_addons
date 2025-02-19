#-*- coding: utf-8 -*-

{
    'name': 'Library Management',
    'version': '18.0.1.0.0',
    'summary': 'library management system',
    #'sequence': 10,
    'description': """
Its Basic Library management system""",
    'author':'Kajal Barad',
    'category': 'Sales/Sales',
    'website': 'https://www.aktivsoftware.com',
    'depends': ['web','sale_management','sale','stock'],
    'data': [
        'data/ir_sequence.xml',
        'security/ir.model.access.csv',
        'views/product_template_only_form_view.xml',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
        'views/library_library_views.xml',
        'views/library_member_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_tag_views.xml',
        'views/bulk_book_views.xml',
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
