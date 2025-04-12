# -*- coding: utf-8 -*-
{
    'name': "late_hr_attendance_s_and_s_venture_ltd",

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
    'depends': ['base','hr_attendance'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/daily_attendance_download.xml',
        'views/daily_report_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/hr_attendance_view_inherit.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

