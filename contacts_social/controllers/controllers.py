# -*- coding: utf-8 -*-
from odoo import http

# class ContactsSocial(http.Controller):
#     @http.route('/contacts_social/contacts_social/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/contacts_social/contacts_social/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('contacts_social.listing', {
#             'root': '/contacts_social/contacts_social',
#             'objects': http.request.env['contacts_social.contacts_social'].search([]),
#         })

#     @http.route('/contacts_social/contacts_social/objects/<model("contacts_social.contacts_social"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('contacts_social.object', {
#             'object': obj
#         })