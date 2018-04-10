# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
{
    'name': "Magazine",

    'summary': """Add a cover page for all blogs""",

    'description': """
        Home page to display the posts of all blogs.
======================================

This module allows the advanced management of the post presentation of all the blog's website

Key Features
------------
* Order chronologically the ost of all blogs.
* Allows you to modify the size of the post image.
* You can modify the unication of the posts in the grid.
* It has 5 ribbons with configurable text to superimpose on the image of the post.
    """,

    'author': "Antonio Fregoso",
    'website': "http://www.antoniofregoso.blog",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Website',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_blog_advanced',
                'website_magazine_footer', 
                'website_magazine_header', 
                'website_back_to_top', 
                'website_anchor_smooth_scroll', 
                'website_cookie_notice',
                'website_adv_image_optimization',
                'website_media_size',
                'website_snippet_preset',
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'security/ir.model.access.csv',
        'data/blog_data.xml',
        'views/res_config_settings.xml',
        'views/templates.xml',
        'views/snippets.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'license': 'AGPL-3',
}
