# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#


from odoo import models, fields



class ResPartner(models.Model):

    _inherit = 'res.partner'
    
    
    semblance = fields.Html('Semblance', translate=True, sanitize=False)