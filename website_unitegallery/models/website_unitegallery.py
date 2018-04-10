# -*- coding: utf-8 -*-
# License MIT #

from odoo import api, fields, models, tools
import logging
_logger = logging.getLogger(__name__)

UGJS1 = '<script type="text/javascript">jQuery(document).ready(function(){jQuery("#gallery").unitegallery('
UGJS2 = ');});</script>'
UGTILE = {"tile_background_color":"#F0F0F0", "tile_border_width":3,"tile_border_color":"#F0F0F0","tile_border_radius":0,"tile_outline_color":'#8B8B8B'}
UGSHADOW = {"tile_shadow_h":1,"tile_shadow_v":1,"tile_shadow_blur":3,"tile_shadow_spread":2,"tile_shadow_color":"#8B8B8B"}
UGIMAGE = {"tile_image_effect_type":"bw", "tile_image_effect_reverse":False, "tile_overlay_color":"#00000", "tile_overlay_opacity": 0.4}
UGTEXTPANEL = {"textpanel_bg_color":"#000000", "tile_textpanel_appear_type":"slide", "tile_textpanel_bg_opacity":0.4, "textpanel_title_color":"#F3F3F3","textpanel_desc_color":"#F3F3F3"}
UGLIGHTBOX = {'lightbox_overlay_color':'#000000', 'lightbox_overlay_opacity':1, 'lightbox_top_panel_opacity':0.4, 'lightbox_show_numbers':True, 'lightbox_numbers_color':'#E5E5E5'}
UG = {**UGTILE, **UGSHADOW, **UGIMAGE, **UGTEXTPANEL, **UGLIGHTBOX}

    

class WebsiteUnitegallery(models.Model):
    _name = 'website.unitegallery'
    _description = 'Unite Gallery'
    name = fields.Char('Gallery Name', required=True)
    tile_background_color = fields.Char('Background Color', default="#F0F0F0", help="Tile background color")
    tile_border_width = fields.Integer('Border Width', default=3)
    tile_border_color = fields.Char('Border Color', default="#F0F0F0")
    tile_border_radius = fields.Integer('Border Radius', default=0)
    tile_outline_color = fields.Char('Outline Color', default="#8B8B8B")
    tile_shadow_h = fields.Integer('Horizaontal', default=1)
    tile_shadow_v = fields.Integer('Vertical', default=1)
    tile_shadow_blur = fields.Integer('Blur', default=3)
    tile_shadow_spread = fields.Integer('Spread', default=2)
    tile_shadow_color = fields.Char('Shadow Color', default="#8B8B8B")   
    tile_overlay_opacity = fields.Float('Overlay Opacity', default=0.4)
    tile_overlay_color = fields.Char('Overlay Color', default="#00000")
    tile_image_effect_type = fields.Selection([
        ('bw', 'Black & White'),
        ('blur', 'Blur'),
        ('sepia', 'Sepia'),
    ], string='Image Efect', default='bw')
    tile_image_effect_reverse = fields.Boolean('On Mouseover', default=False)
    textpanel_bg_color = fields.Char('Background Color', default="#000000", help="Text panel background color")
    tile_textpanel_appear_type = fields.Selection([
        ('slide', 'Slide'),
        ('fade', 'Fade'),
    ], string='Appear Type', default='slide')
    tile_textpanel_bg_opacity = fields.Float('Background Opacity', default=0.4, help="Textpanel background opacity")
    textpanel_title_color = fields.Char('Title Color', default="#F3F3F3")
    textpanel_desc_color = fields.Char('Description Color', default="#F3F3F3")
    lightbox_overlay_color = fields.Char('Overlay Color', default="#00000", help="The color of the overlay.")
    lightbox_overlay_opacity = fields.Float('Overlay Opacity', default=1)
    lightbox_top_panel_opacity = fields.Float('Top Panel Opacity', default=0.4)
    lightbox_show_numbers = fields.Boolean('Show Numbers', default=True)
    lightbox_numbers_color = fields.Char('Numbers Color', default="#E5E5E5", help="The color of the numbers")
    carousel_ids = fields.One2many('website.unitegallery.carousel', 'gallery_id', string='Carousels')
    compact_ids = fields.One2many('website.unitegallery.compact', 'gallery_id', string='Compacts')
    default_ids = fields.One2many('website.unitegallery.default', 'gallery_id', string='Defaults')
    grid_ids = fields.One2many('website.unitegallery.grid', 'gallery_id', string='Grids')
    slider_ids = fields.One2many('website.unitegallery.slider', 'gallery_id', string='Sliders')
    tiles_ids = fields.One2many('website.unitegallery.tiles', 'gallery_id', string='Tiles')
    tilesgrid_ids = fields.One2many('website.unitegallery.tilesgrid', 'gallery_id', string='Tiles Grids')
    video_ids = fields.One2many('website.unitegallery.video', 'gallery_id', string='Videos')
    
    @api.one
    def set_defaults(self):
        self.write(UG)
        return True
    
    def get_carousel(self, ug_id, ug_name, tag):
        obj_carousel = self.env["website.unitegallery.carousel"]
        ug = self.search_read([('id', '=', ug_id)],[])[0]
        carousel = obj_carousel.search_read([('name', '=', ug_name)],[])[0]
        settings = {}
        for k, v in UG.items():
            if ug[k]!=v:
                settings[k]=ug[k]
        for k, v in CAROUSEL.items():
            if carousel[k]!=v:
                settings[k]=carousel[k]
        for k, v in settings.items():
            if type(v)==str:
                settings[k]= '"' + v + '"'
        if len(settings) > 0:
            js = UGJS1.replace('#gallery',tag) + str(settings).replace('False', 'false').replace('True','true') + UGJS2
        else:
            js = UGJS1.replace('#gallery',tag) + UGJS2  
        js = js.replace("'","")
        return js
    

    
CAROUSELGALLERY = {"theme_gallery_padding":0, "theme_carousel_align":"center", "theme_carousel_offset":0, "gallery_width":"100%", "tile_width":160, "tile_height":160, "carousel_vertical_scroll_ondrag":True, "carousel_space_between_tiles":20, "carousel_autoplay_timeout":3000, "carousel_autoplay_direction":"right"}
CAROUSELNAVIGATION = {"theme_enable_navigation":True, "theme_navigation_position":"bottom", "theme_navigation_enable_play":True, "theme_navigation_align":"center", "theme_navigation_offset_hor":0, "theme_navigation_margin":20, "theme_space_between_arrows":5}
CAROUSELTEXTPANEL = {"tile_enable_textpanel":False, "tile_textpanel_source":"title", "tile_textpanel_always_on":False, "tile_textpanel_position":"inside_bottom", "tile_textpanel_offset":0}
CAROUSELICONS = {"tile_enable_icons":True, "tile_show_link_icon":False, "tile_videoplay_icon_always_on":"never", "tile_space_between_icons":26}
CAROUSELAPPERANCE = {"tile_enable_background":True, "tile_enable_border":True, "tile_enable_outline":True, "tile_enable_shadow":False, "tile_enable_overlay":True, "tile_enable_image_effect":False}
CAROUSELACTIONS = {"tile_enable_action":True, "tile_as_link":False, "tile_link_newpage":True}
CAROUSEL = {**CAROUSELGALLERY, **CAROUSELNAVIGATION, **CAROUSELTEXTPANEL, **CAROUSELICONS, **CAROUSELACTIONS}

    
class WebsiteUnitegalleryCarousel(models.Model):
    _name = 'website.unitegallery.carousel'
    _description = 'Unite Gallery Carousel'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    theme_gallery_padding = fields.Integer('Padding', default=0, help="The padding of the gallery wrapper.")
    theme_carousel_align = fields.Selection([
        ('center', 'Center'),
        ('left', 'Left'),
        ('right', 'Right'),
    ], string='Position', default='center')
    theme_carousel_offset = fields.Integer('Carousel Offset', default=0, help="Tte offset of the carousel from the align sides.")
    gallery_width = fields.Char('Width', default="100%")
    carousel_vertical_scroll_ondrag = fields.Boolean('Vertical Scroll', default=True, help="Carousel vertical scroll on drag.")
    tile_width = fields.Integer('Tile Width', default=160)
    tile_height = fields.Integer('Tile Height', default=160)
    carousel_space_between_tiles = fields.Integer('Space', default=20, help="Space between tiles")
    carousel_autoplay_timeout = fields.Integer('Timeoout', default=3000, help="Autoplay timeout in milliseconds.")
    carousel_autoplay_direction = fields.Selection([
        ('right', 'Right'),
        ('left', 'Left'),
    ], string='Direction', default='right', help="Autoplay direction.")
    theme_enable_navigation = fields.Boolean('Enable Navigation', default=True)
    theme_navigation_position = fields.Selection([
        ('top', 'Top'),
        ('bottom', 'Bottom')
    ], string='Vertical Position', default='bottom', help="The vertical position of the navigation reative to the carousel.")
    theme_navigation_enable_play = fields.Boolean('Enable Play Button', default=True, help="enable / disable the play button of the navigation.")
    theme_navigation_align = fields.Selection([
        ('center', 'Center'),
        ('left', 'Left'),
        ('right', 'Right'),
    ], string='Navigation Align', default='center')
    theme_navigation_offset_hor = fields.Integer('Horizontal Offset', default=0, help="Horizontal offset of the navigation.")
    theme_navigation_margin = fields.Integer('Navigation Margin', default=20, help="The space between the carousel and the navigation.")
    theme_space_between_arrows = fields.Integer('Space Between Arrows', default=5, help="The space between arrows in the navigation.")
    tile_enable_background = fields.Boolean('Enable Background', default=True, help="Enable backgruond of the tile")
    tile_enable_border = fields.Boolean('Enable Border', default=True, help="Enable border of the tile")
    tile_enable_outline = fields.Boolean('Enable Outline', default=True)
    tile_enable_shadow = fields.Boolean('Enable Shadow', default=False)
    tile_enable_overlay = fields.Boolean('Enable Overlay', default=True)
    tile_enable_image_effect = fields.Boolean('Enable Image Efects', default=False)
    tile_enable_textpanel = fields.Boolean('Enable Text Panel', default=False)
    tile_textpanel_source = fields.Selection([
        ('title', 'Title'),
        ('desc_title', 'Description or Title'),
        ('title_and_desc', 'Title and Description'),
    ], string='Text Source', default='title')
    tile_textpanel_always_on = fields.Boolean('Olways On', default=False)
    tile_textpanel_position = fields.Selection([
        ('inside_bottom', 'Inside Bottom'),
        ('inside_top', 'Inside Top'),
        ('inside_center', 'Inside Center'),
        ('top', 'Top'),
        ('bottom', 'Bottom'),
    ], string='Position', default='inside_bottom')
    tile_textpanel_offset = fields.Integer('Vertical Offset', default=0)
    tile_enable_icons = fields.Boolean('Enable Icons', default=True)
    tile_show_link_icon = fields.Boolean('Link Icon', default=False)
    tile_videoplay_icon_always_on = fields.Selection([
        ('always', 'Always'),
        ('never', 'Never'),
        ('mobile_only', 'Mobile Only'),
        ('desktop_only', 'Desktop Only'),
    ], string='Video Play Icon', default='never')
    tile_space_between_icons = fields.Integer('Space Between Icons', default=26)
    tile_enable_action = fields.Boolean('Enable Action', default=True)
    tile_as_link = fields.Boolean('Tile as Link', default=False)
    tile_link_newpage = fields.Boolean('Link in New Page', default=True)
    
    @api.one
    def set_defaults(self):
        self.write(CAROUSEL)
        return True
    
    
    
class WebsiteUnitegalleryCompact(models.Model):
    _name = 'website.unitegallery.compact'
    _description = 'Unite Gallery Compact'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegalleryDefault(models.Model):
    _name = 'website.unitegallery.default'
    _description = 'Unite Gallery Default'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegalleryGrid(models.Model):
    _name = 'website.unitegallery.grid'
    _description = 'Unite Gallery Grid'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegallerySlider(models.Model):
    _name = 'website.unitegallery.slider'
    _description = 'Unite Gallery Slider'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegalleryTiles(models.Model):
    _name = 'website.unitegallery.tiles'
    _description = 'Unite Gallery Tiles'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegalleryTilesgrid(models.Model):
    _name = 'website.unitegallery.tilesgrid'
    _description = 'Unite Gallery Tiles Grid'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
class WebsiteUnitegalleryVideo(models.Model):
    _name = 'website.unitegallery.video'
    _description = 'Unite Gallery Tiles Video'
    name = fields.Char('Name', required=True)
    gallery_id = fields.Many2one('website.unitegallery', string="Set", required=True)
    
    
    
    
    
    
    