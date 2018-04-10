# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)

IMG_STYLES = [('ic_none', 'None'), 
              ('ic_bw', 'Black & Wite'), 
              ('ic_opacity', 'Opacity'), 
              ('ic_blur', 'Blur'), 
              ('ic_sepia', 'Sepia'), 
              ('ic_zoom', 'Zoom')]

IMG_OVER_STYLES = [('ic_hnone', 'None'), 
              ('ic_hbw', 'Black & Wite'), 
              ('ic_hopacity', 'Opacity'), 
              ('ic_hblur', 'Blur'), 
              ('ic_hsepia', 'Sepia'), 
              ('ic_hzoom', 'Zoom'),
              ('ic_hzoom_c', 'Zoom Clean')]



class Website(models.Model):
    _inherit = "website" 
    
    primary_ribbon = fields.Char('Ribbon 1', size=7, default="Primary")
    success_ribbon= fields.Char('Ribbon 2', size=7, default="Success")
    info_ribbon = fields.Char('Ribbon 3', size=7, default="Info")
    warning_ribbon = fields.Char('Ribbon 4', size=7, default="Warning")
    danger_ribbon = fields.Char('Ribbon 5', size=7, default="Danger")
    style = fields.Selection(IMG_STYLES, default="ic_none")
    over_style = fields.Selection(IMG_OVER_STYLES, default="ic_hnone")
    frosted_glass = fields.Boolean('Frosted Glass', default=True)
    author = fields.Boolean('Author', default=True)
    ppg = fields.Integer("Posts per Page", help="Post shown by page", default=20)
    ppr = fields.Selection([(2,'2'),(3,'3'),(4,'4')], help="Post shown by raw", default=4)
    pagination = fields.Boolean('Pagination', default=False)
    

    

            
        
    
    