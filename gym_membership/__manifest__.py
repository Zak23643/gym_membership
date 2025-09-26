# -*- coding: utf-8 -*-
{
    'name': "Gym Membership Management",

    'summary': """
        Manage gym memberships, plans, and member subscriptions.""",

    'description': """
        This module provides a comprehensive system to manage a fitness center or gym. 
        It allows for the creation of membership plans, enrollment of members, 
        and tracking of their membership status.
    """,

    'author': "Zahir",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Services/Fitness',
    # 'version': '16.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/cron_data.xml',
        'views/membership_plan_views.xml',
        'views/member_membership_views.xml',
        'views/menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}
