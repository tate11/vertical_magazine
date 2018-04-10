# -*- coding: utf-8 -*-
# License MIT #

from odoo import api, fields, models

class WebsiteUnitegalleryRestart(models.TransientModel):
    _name = 'website.unitegallery.restart'
    _description = 'Restart Unite Gallery'
    
    
    @api.multi
    def restart_unite_gallery(self):
        ug = self.env['website.unitegallery'].browse(self.env.context.get('active_ids'))
        ug.set_defaults()
        return  {'type': 'ir.actions.act_window_close'}
