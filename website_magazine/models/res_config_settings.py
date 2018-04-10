# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    primary_ribbon = fields.Char('Ribbon 1', related='website_id.primary_ribbon')
    success_ribbon = fields.Char('Ribbon 2', related='website_id.success_ribbon')
    info_ribbon= fields.Char('Ribbon 3', related='website_id.info_ribbon')
    warning_ribbon = fields.Char('Ribbon 4', related='website_id.warning_ribbon')
    danger_ribbon = fields.Char('Ribbon 5', related='website_id.danger_ribbon')
    style = fields.Selection('Style', related='website_id.style')
    over_style = fields.Selection('Mouse Over Style', related='website_id.over_style')
    frosted_glass = fields.Boolean('Frosted Glass', related='website_id.frosted_glass')
    author = fields.Boolean('Author', related='website_id.author')
    ppg = fields.Integer("Posts per Page", related='website_id.ppg')
    ppr = fields.Selection("Posts per Page", related='website_id.ppr')
    pagination = fields.Boolean("Pagination", related='website_id.pagination')
    
    @api.onchange('ppr')
    def onchange_ppr(self):
        return self.env['blog.post'].create_cover_images()
        
    
