# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#

from odoo import models, fields, api, _
from odoo.addons.http_routing.models.ir_http import slug
import  requests 
from datetime import datetime
import base64
from PIL import Image, ImageEnhance
from io import BytesIO
import os, sys
import logging
from werkzeug._internal import _log
from odoo.http import request
from requests.api import post
_logger = logging.getLogger(__name__)

class BlogPostStyle(models.Model):
    _name = "blog.post.style"

    name = fields.Char(string='Style Name', required=True)
    html_class = fields.Char(string='HTML Classes')

class BlogPost(models.Model):
    _inherit = 'blog.post'  
    
    website_size_x = fields.Integer('Size X', default=1)
    website_size_y = fields.Integer('Size Y', default=1)
    website_style_ids = fields.Many2many('blog.post.style', string='Styles')
    website_sequence = fields.Integer('Website Sequence', help="Determine the display order in the Website Cover",
                                      default=lambda self: self._default_website_sequence())
    

    def _default_website_sequence(self):
        #self._cr.execute("SELECT MIN(website_sequence) FROM %s" % self._table)
        #min_sequence = self._cr.fetchone()[0]
        #return min_sequence and min_sequence - 1 or 10
        return 50

    def set_sequence_top(self):
        self.website_sequence = self.sudo().search([], order='website_sequence desc', limit=1).website_sequence + 1

    def set_sequence_bottom(self):
        self.website_sequence = self.sudo().search([], order='website_sequence', limit=1).website_sequence - 1

    def set_sequence_up(self):
        previous_blog_post = self.sudo().search(
            [('website_sequence', '>', self.website_sequence), ('website_sequence', '=', self.website_sequence)],
            order='website_sequence', limit=1)
        if previous_blog_post:
            previous_blog_post.website_sequence, self.website_sequence = self.website_sequence, previous_blog_post.website_sequence
        else:
            self.set_sequence_top()

    def set_sequence_down(self):
        next_blog_post = self.search([('website_sequence', '<', self.website_sequence), ('website_sequence', '=', self.website_sequence)], order='website_sequence desc', limit=1)
        if next_blog_post:
            next_blog_post.website_sequence, self.website_sequence = self.website_sequence, next_blog_post.website_sequence
        else:
            return self.set_sequence_bottom()
        
    def set_sequence_reset(self):
        self.website_sequence = self._default_website_sequence() 
        
    def get_author(self):
        return self.sudo().author_id.name
    
    def get_author_slug(self):
        slug = self.sudo().author_id.name.strip().lower().replace(' ','-') + '-' + str(self.sudo().author_id.id)
        return slug
        
    @api.one
    def create_cover_image(self, blog_post_id, ppr, x, y):
        w=1368
        h=1200
        dx=w/ppr
        dy=h/4
        img_w = int(dx*x)
        img_h = int(dy*y)
        ratio = img_w/img_h
        img_url = eval(self.cover_properties)['background-image']
        if img_url != 'none':
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            img_name = str(blog_post_id)
            img_url = base_url + img_url.replace('url(', '').replace(')','')
            image_path = os.getcwd()  + '/addons/website_blog/static/src/img/'
            img_url = img_url.replace('web/image/website_blog.blog_post_cover_01','website_blog/static/src/img/demo/blog_post_cover_1.jpg')
            img_url = img_url.replace('web/image/website_blog.blog_post_cover_02','website_blog/static/src/img/demo/blog_post_cover_2.jpg')
            response = requests.get(img_url)
            if response.status_code ==200:
                blog_image = Image.open(BytesIO(response.content))
                origin_mode = blog_image.mode
                if blog_image.mode != 'RGBA':
                    blog_image = blog_image.convert('RGBA')
                size =blog_image.size
                ratio2 = size[0]/size[1]
                dx2 = size[1]*ratio
                dy2 = size[0]/ratio
                if ratio2>ratio:
                    spillover = int((size[0] - dx2)/2)
                    crop = (spillover,0,size[0]-spillover,size[1])
                    ar_image = blog_image.crop(crop).resize((img_w,img_h))
                elif ratio2<ratio:
                    spillover = int((size[1] - dy2)/2)
                    crop = (0,spillover,size[0],size[1]-spillover)
                    ar_image = blog_image.crop(crop).resize((img_w,img_h))
                else:
                    ar_image = blog_image.resize((img_w,img_h))                  
                sharpener = ImageEnhance.Sharpness(ar_image)
                resized_image = sharpener.enhance(2.0)
                if resized_image.mode != origin_mode:
                    resized_image = resized_image.convert(origin_mode)
                return resized_image.save(image_path +'cover_' + img_name + '.jpg', format="JPEG")
                
            else:
                return False
        
    @api.one
    def get_cover_url(self):
        img_url = '/website_blog/static/src/img/cover_' + str(self.id) + '.jpg'
        return  img_url
     
        
    def get_img_url(self):
        img_url = eval(self.cover_properties)['background-image']
        img_url = img_url.replace('url(', '').replace(')','')
        return img_url
    
    @api.model
    def create_cover_images(self):
        blog_post_obj = self.env['blog.post']
        posts = blog_post_obj.search_read([],['id','website_size_x','website_size_y','name'])
        _logger.warn('Creating cover images')        
        url_domain  = self.env['ir.config_parameter'].get_param('web.base.url').split('/')[2].split(':')[0]  
        ppr = self.env['website'].search([('domain','=',url_domain)]).ppr
        for post in posts:
            x = blog_post_obj.browse(post['id'])
            x.create_cover_image(post['id'], ppr, post['website_size_x'], post['website_size_y'])
            _logger.warn('Image from ' + post['name'] + ' post')
            