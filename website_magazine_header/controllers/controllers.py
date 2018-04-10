# -*- coding: utf-8 -*-
from odoo import http

# class WebsiteBrandHeader(http.Controller):
#     @http.route('/website_magazine_header/website_magazine_header/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/website_magazine_header/website_magazine_header/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('website_magazine_header.listing', {
#             'root': '/website_magazine_header/website_magazine_header',
#             'objects': http.request.env['website_magazine_header.website_magazine_header'].search([]),
#         })

#     @http.route('/website_magazine_header/website_magazine_header/objects/<model("website_magazine_header.website_magazine_header"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('website_magazine_header.object', {
#             'object': obj
#         })