# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api


class Website(models.Model):
    _inherit = "website" 
    
            
    @api.one
    def get_cc(self):
        o_blog = self.search_blog_id
        lc_url = "http://creativecommons.org/licenses/"
        lc_img = "https://i.creativecommons.org/l/"
        if o_blog.cc_commercial:
            if o_blog.cc_share=='by':
                lc_url += "by/4.0/" 
                lc_img += "by/4.0/"              
            elif o_blog.cc_share=='by-nd':
                lc_url += "by-nd/4.0/"
                lc_img += "by-nd/4.0/"        
            else:
                lc_url += "by-sa/4.0/"
                lc_img += "by-sa/4.0/"                             
        else:
            if o_blog.cc_share=='by':
                lc_url += "by-nc/4.0/" 
                lc_img += "by-nc/4.0/"                
            elif o_blog.cc_share=='by-nd':
                lc_url += "by-nc-nd/4.0/"
                lc_img += "by-nc-nd/4.0/"       
            else:
                lc_url += "by-nc-sa/4.0/" 
                lc_img += "by-nc-sa/4.0/"   
        if o_blog.cc_compact_icon: 
            lc_img += "80x15.png"
        else:
            lc_img += "88x31.png"     
        cc = {'lc_url':lc_url, 'lc_img':lc_img} 
        return  cc
    
        
         