# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
{
    'name': "Blog Advanced",

    'summary': 'Add new features to the blog',

    'description': """
Advanced management of post presentation in blogs.
======================================

Key Features
------------
* Right column.
* Most read posts with and without image.
* Post related with and without image.
* Customizing the lists of posts.
* Creative Commons.
""",

    'author': "Antonio Fregoso",
    'website': "http://www.antoniofregoso.blog",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base_automation', 'website_blog', 'web_widget_color','website_unitegallery'],

    # always loaded
    'data': [
        'views/website_blog_views.xml',
        'views/blog_category_view.xml',
        'views/res_partner_views.xml',
        'views/templates.xml',
        'data/blog_post.xml',
        'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
     'demo': [
        'demo/blog_category_demo.xml',
        'demo/blog_post_demo.xml',        
    ],
     'license': 'AGPL-3',
}