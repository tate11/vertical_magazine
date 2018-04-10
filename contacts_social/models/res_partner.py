# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api

class ResPartner(models.Model):

    _inherit = 'res.partner'
    
    
    facebook = fields.Char('Facebook')
    facebook_page = fields.Char('Facebook Page')
    instagram = fields.Char('Instagram')
    twitter = fields.Char('Twitter')
    linkedin = fields.Char('LinkedIn')
    youtube = fields.Char('Youtube')
    google_plus = fields.Char('Google+')
    github = fields.Char('GitHub')
    blog1 = fields.Char('Blog 1')
    blog2 = fields.Char('Blog 2')
    