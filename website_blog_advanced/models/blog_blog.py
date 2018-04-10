# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, _


class Blog(models.Model):
    _inherit = ['blog.blog']
    
    schema = fields.Selection([('Blog','Blog'),('Book','Book'),('WebSite','Web Site')],'Schema', default='Blog')
    cc_share = fields.Selection([ ('by','Yes'), ('by-nd','No'), ('by-sa', 'Yes, as long as others share alike ')],'Allow adaptations', help='Allow adaptations of your work to be shared?', tdefault='by-nd')
    cc_commercial = fields.Boolean('Commercial uses', help='Allow commercial uses of your work?', default=False)
    cc_metadata_title = fields.Boolean('Title', help='Do you want to include title of work?',  default=False)
    cc_metadata_attribution = fields.Selection([ ('no','No'), ('author','Author'),('company','Company')],'Attribution', help='Do you want to include attribution for the author?', default='no')
    cc_compact_icon = fields.Boolean('Compact icon', help="Normal icon: 88x31 px, compact icon: 80x15 px", default=False)
    most_read = fields.Integer('Most Read', help="Post number shown on the list.", default=5)
    related = fields.Integer('Related Posts', help="Post number shown on the list.", default=5)
    most_read_c = fields.Integer('Most Read', help="Post number shown on the carousel list.", default=10)
    related_c = fields.Integer('Related Posts', help="Post number shown on the carousel list.", default=10)
    video_channel = fields.Char('Channel URL')
    video_c = fields.Integer('Carousel Videos', help="Number of YouTube/Vimeo videos.", default=10)
    website_category_ids = fields.One2many(string='Website Categories', comodel_name='blog.category',inverse_name='blog_id')


