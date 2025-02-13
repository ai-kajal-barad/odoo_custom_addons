#-*- coding: utf-8 -*-

{
    'name': 'Library Management System',
    'version': '18.0.1.0.0',
    'summary': 'library management system',
    #'sequence': 10,
    'description': """
Its Basic Library management system""",
    'author':'Kajal Barad',
    'category': 'Sales/Sales',
    'website': 'https://www.aktivsoftware.com',
    'depends': ['sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_only_form_view.xml',
        'views/library_library_views.xml',
        'views/library_member_views.xml',
        'views/library_book_category_views.xml',
        'views/library_book_tag_views.xml',
        ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
