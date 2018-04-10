# -*- coding: utf-8 -*-
# License MIT #

from odoo import api, fields, models, tools

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    
    unitegallery_id = fields.Many2one(related="website_id.unitegallery_id")