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
_logger = logging.getLogger(__name__)


class BlogPost(models.Model):

    _inherit = 'blog.post'

    website_category_id = fields.Many2one(
        string='Website Category',
        comodel_name='blog.category',
    )

    @api.model
    def search(self, domain, *args, **kwargs):
        if self.env.context.get('search_category_id'):
            category = self.env.context['search_category_id']
            domain += [
                ('website_category_id', 'child_of', category),
            ]
        _logger.debug(domain)
        return super(BlogPost, self).search(domain, *args, **kwargs)
    
        
    @api.one
    def get_cc(self):        
        o_blog = self.blog_id
        lc_text = ""
        lc_url = "http://creativecommons.org/licenses/"
        lc_img = "https://i.creativecommons.org/l/"
        if o_blog.cc_commercial:
            if o_blog.cc_share=='by':
                lc_text += _("Creative Commons Attribution 4.0 International License")
                lc_url += "by/4.0/" 
                lc_img += "by/4.0/"              
            elif o_blog.cc_share=='by-nd':
                lc_text += _("Creative Commons Attribution-WithoutDerive 4.0 International License")
                lc_url += "by-nd/4.0/"
                lc_img += "by-nd/4.0/"        
            else:
                lc_text += _("Creative Commons Attribution-ShareAlike 4.0 International License")
                lc_url += "by-sa/4.0/"
                lc_img += "by-sa/4.0/"                             
        else:
            if o_blog.cc_share=='by':
                lc_text += _("Creative Commons Attribution- NonCommercial 4.0 International License")
                lc_url += "by-nc/4.0/" 
                lc_img += "by-nc/4.0/"                
            elif o_blog.cc_share=='by-nd':
                lc_text += _("Creative Commons Attribution-NonCommercial-WithoutDerive 4.0 International License")
                lc_url += "by-nc-nd/4.0/"
                lc_img += "by-nc-nd/4.0/"       
            else:
                lc_text += _("Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License")
                lc_url += "by-nc-sa/4.0/" 
                lc_img += "by-nc-sa/4.0/"   
        if o_blog.cc_compact_icon: 
            lc_img += "80x15.png"
        else:
            lc_img += "88x31.png"     
        ccl = {'lc_text':lc_text,'lc_url':lc_url, 'lc_img':lc_img, 'lc_metadata_title':o_blog.cc_metadata_title, 'lc_metadata_attribution':o_blog.cc_metadata_attribution} 
        return  ccl
    
    @api.one
    def get_most_read(self, carousel=False):
        if carousel:
            max_posts=self.blog_id.most_read_c
        else:
            max_posts=self.blog_id.most_read
        posts = self.env['blog.post'].sudo().search([('blog_id','=',self.blog_id.id),('website_published','=',True)], order='ranking desc',limit=max_posts)
        if posts:
            post_most_read=[]
            for p in posts:
                if p.id!=self.id:
                    if len(p['subtitle'])>35:
                        subt = p['subtitle'][0:34] + '...'
                    else:
                        subt = p['subtitle'] 
                    published = datetime.strptime(p.published_date, '%Y-%m-%d %H:%M:%S').strftime('%B %Y')
                    published_long = datetime.strptime(p.published_date, '%Y-%m-%d %H:%M:%S').strftime('%B %d %Y %H:%M hrs.')
                    post_url = "/blog/%s/post/%s" % (slug(p.blog_id), slug(p))
                    img_path = '/website_blog/static/src/img/bp_'
                    author = p.author_id.name                    
                    cover = self.get_cover()
                    link={'url':post_url, 'name':p['name'], 'subtitle':subt, 'cover': cover, 'img':img_path + 'tn_' + str(p['id']) + '.jpg', 'img2':img_path + 'sld_' + str(p['id']) + '.jpg', 'author':author, 'published':published, 'published news':published_long, 'visits':p['visits']}
                    post_most_read.append(link)
            return   post_most_read
        else:
            return False
        
    @api.one
    def get_related_topics(self, carousel=False):
        if carousel:
            max_posts=self.blog_id.related_c
        else:
            max_posts=self.blog_id.related
        tags = []
        for tag in self.tag_ids:
            tags.append(tag.id)
        posts=self.env['blog.post'].sudo().search([('blog_id','=',self.blog_id.id),('website_published','=',True),('tag_ids','in',tags)], order='ranking desc',limit=max_posts)
        if posts:
            post_most_read=[]
            for p in posts:
                if p.id!=self.id:
                    if len(p['subtitle'])>35:
                        subt = p['subtitle'][0:34] + '...'
                    else:
                        subt = p['subtitle']                     
                    published = datetime.strptime(p.published_date, '%Y-%m-%d %H:%M:%S').strftime('%B %d %Y')
                    published_long = datetime.strptime(p.published_date, '%Y-%m-%d %H:%M:%S').strftime('%B %d %Y %H:%M')
                    post_url = "/blog/%s/post/%s" % (slug(p.blog_id), slug(p))
                    img_path = '/website_blog/static/src/img/bp_'
                    author = p.author_id.name
                    cover = self.get_cover()
                    link={'url':post_url, 'name':p['name'], 'subtitle':subt, 'cover': cover, 'img':img_path +'tn_' + str(p['id']) + '.jpg', 'img2':img_path + 'sld_' + str(p['id']) + '.jpg', 'author':author, 'published':published, 'published news':published_long, 'visits':p['visits']}
                    post_most_read.append(link)
                    
            return   post_most_read
        else:
            return False
        
    def get_cover(self):
        img_url = eval(self.cover_properties)['background-image']
        if img_url != 'none':   
            img_url = img_url.replace('url(', '').replace(')','')             
            img_url = img_url.replace('web/image/website_blog.blog_post_cover_01','website_blog/static/src/img/demo/blog_post_cover_1.jpg')
            img_url = img_url.replace('web/image/website_blog.blog_post_cover_02','website_blog/static/src/img/demo/blog_post_cover_2.jpg')
        else:
            img_url = None 
        return img_url
        
    @api.one
    def create_images(self):
        thumbnail = (70,70)
        slider = (268, 151)
        img_url = eval(self.cover_properties)['background-image']
        if img_url != 'none':
            base_url = self.env['ir.config_parameter'].get_param('web.base.url')
            img_name = str(self.id)
            img_url = base_url + self.get_cover()
            image_path = os.getcwd()  + '/addons/website_blog/static/src/img/'
            response = requests.get(img_url)   
            if response.status_code ==200: 
                blog_image = Image.open(BytesIO(response.content))
                origin_mode = blog_image.mode
                if blog_image.mode != 'RGBA':
                        blog_image = blog_image.convert('RGBA')
                size =blog_image.size 
                ar = float(slider[0])/slider[1]
                w2 = int(size[1]*ar)
                if w2 <= size[0]:
                    dw = (size[0]-w2)/2
                    crop = (0+dw,0,size[0]-dw,size[1])
                else:                
                    h2= int(size[0]/ar)
                    dh=(size[1]-h2)/2
                    crop = (0,dh,size[0],size[1]-dh)
                ar_image = blog_image.crop(crop).resize(slider)
                sharpener = ImageEnhance.Sharpness(ar_image)
                resized_image = sharpener.enhance(2.0)
                if resized_image.mode != origin_mode:
                    resized_image = resized_image.convert(origin_mode)
                resized_image.save(image_path +'bp_sld_' + img_name + '.jpg', format="JPEG")
                ar = float(thumbnail[0])/thumbnail[1]
                w2 = int(size[1]*ar)
                if w2 <= size[0]:
                    dw = (size[0]-w2)/2
                    crop = (0+dw,0,size[0]-dw,size[1])
                else:                
                    h2= int(size[0]/ar)
                    dh=(size[1]-h2)/2
                    crop = (0,dh,size[0],size[1]-dh)
                ar_image = blog_image.crop(crop).resize(thumbnail)
                sharpener = ImageEnhance.Sharpness(ar_image)
                resized_image = sharpener.enhance(2.0)
                if resized_image.mode != origin_mode:
                    resized_image = resized_image.convert(origin_mode)
                resized_image.save(image_path +'bp_tn_' + img_name + '.jpg', format="JPEG")              
                return True
            else:            
                return False
                
    @api.model
    def create_thumbnails(self):        
        blog_post_obj = self.env['blog.post']
        posts = blog_post_obj.search_read([],['id','name'])
        _logger.warn('Creating thumbnails')
        for post in posts:
            x = blog_post_obj.browse(post['id'])
            x.create_images()
            _logger.warn('Thumbnail from ' + post['name'] + ' post')
      
