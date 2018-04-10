# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    logo = fields.Binary(string="Website logo", related='website_id.logo')
    search_blog_id = fields.Many2one(string='Blog to Search', related='website_id.search_blog_id')