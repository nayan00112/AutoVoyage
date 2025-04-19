# -*- coding: utf-8 -*-
{
    'name': "autovoyage",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/autovoyage_service_sequence.xml',
        'views/autovoyage_services_view.xml',
        'views/res_users_view_inherit.xml',
        'views/autovoyage_vehicle_view.xml',
        # 'views/autovoyage_service_cron.xml',
        'views/autovoyage_service_provider_create.xml',
        'views/vehicle_custom_views.xml',
        'views/menu.xml',
    ],

    'installable':True,
    'application':True,
    
}

