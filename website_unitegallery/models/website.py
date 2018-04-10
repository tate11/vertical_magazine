# -*- coding: utf-8 -*-
# License MIT #

from odoo import api, fields, models, tools

class Website(models.Model):
    _inherit = "website" 
    
    unitegallery_id = fields.Many2one('website.unitegallery', string="Unite Gallery Settings") 