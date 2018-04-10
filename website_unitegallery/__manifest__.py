# -*- coding: utf-8 -*-
# License MIT #

{
    'name': "Website Unitegallery",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Antonio Fregoso, "
              "Max Valiano ",
    'website': "http://www.antoniofregoso.blog",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website','web_widget_color'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',        
        'wizard/ug_wizards.xml',
        'views/ug_views.xml',
        'views/ug_menus.xml',
        'views/ug_templates.xml',
        'views/ug_snippets.xml',
        'views/res_config_settings.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/ug_menus_demo.xml',
        'demo/ug_pages_demo.xml',
    ],
}