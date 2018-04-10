# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website" 
    
    @api.multi
    def _get_search_blog(self):
        search_blog_id = self.env['blog.blog'].search([('active','=', True)])[0].id
        return search_blog_id
    
    logo = fields.Binary(string="Website logo",  help="This field holds the logo for this website, showed in header. Recommended size is 180x50")
    search_blog_id = fields.Many2one('blog.blog', string='Blog to Search', default=_get_search_blog)
    
