# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteMagazineFooter(http.Controller):
#     @http.route('/website_magazine_footer/website_magazine_footer/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_magazine_footer/website_magazine_footer/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_magazine_footer.listing', {
#             'root': '/website_magazine_footer/website_magazine_footer',
#             'objects': http.request.env['website_magazine_footer.website_magazine_footer'].search([]),
#         })

#     @http.route('/website_magazine_footer/website_magazine_footer/objects/<model("website_magazine_footer.website_magazine_footer"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_magazine_footer.object', {
#             'object': obj
#         })