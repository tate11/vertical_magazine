# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).#
from odoo import http, tools, _

from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website.controllers.main import QueryURL
import logging
_logger = logging.getLogger(__name__)



class TableCompute(object):

    def __init__(self):
        self.table = {}

    def _check_place(self, ppr, posx, posy, sizex, sizey):
        res = True
        for y in range(sizey):
            for x in range(sizex):
                if posx + x >= ppr:
                    res = False
                    break
                row = self.table.setdefault(posy + y, {})
                if row.setdefault(posx + x) is not None:
                    res = False
                    break
            for x in range(ppr):
                self.table[posy + y].setdefault(x, None)
        return res

    def process(self, posts, ppg, ppr):
        # Compute posts positions on the grid
        minpos = 0
        index = 0
        maxy = 0
        x = 0
        for p in posts:
            x = min(max(p.website_size_x, 1), ppr)
            y = min(max(p.website_size_y, 1), ppr)
            if index >= ppg:
                x = y = 1

            pos = minpos
            while not self._check_place(ppr, pos % ppr, pos // ppr, x, y):
                pos += 1
            # if 21st products (index 20) and the last line is full (PPR products in it), break
            # (pos + 1.0) / PPR is the line where the product would be inserted
            # maxy is the number of existing lines
            # + 1.0 is because pos begins at 0, thus pos 20 is actually the 21st block
            # and to force python to not round the division operation
            if index >= ppg and ((pos + 1.0) // ppr) > maxy:
                break

            if x == 1 and y == 1:   # simple heuristic for CPU optimization
                minpos = pos // ppr

            for y2 in range(y):
                for x2 in range(x):
                    self.table[(pos // ppr) + y2][(pos % ppr) + x2] = False
            self.table[pos // ppr][pos % ppr] = {
                'post': p, 'x': x, 'y': y,
                'class': " ".join(x.html_class for x in p.website_style_ids if x.html_class)
            }
            if index <= ppg:
                maxy = max(maxy, y + (pos // ppr))
            index += 1

        # Format table according to HTML needs
        rows = sorted(self.table.items())
        rows = [r[1] for r in rows]
        for col in range(len(rows)):
            cols = sorted(rows[col].items())
            x += len(cols)
            rows[col] = [r[1] for r in cols if r[1]]
        
        return rows


        
class Website(Website):
    
    
    def _get_search_domain(self, search):
        domain = [("website_published","=",True)]
        if search:
            for srch in search.split(" "):
                domain += [
                    '|', '|', '|', ('name', 'ilike', srch), ('subtitle', 'ilike', srch),
                    ('content', 'ilike', srch), ('tag_ids.name', 'ilike', srch)]
        return domain
        
    @http.route(['/', '/page/<int:page>'], type='http', auth="public", website=True)
    def index(self, page=0):
        portal = request.website
        homepage = portal.homepage_id
        if homepage and (homepage.sudo().is_visible or request.env.user.has_group('base.group_user')) and homepage.url != '/':
            return request.env['ir.http'].reroute(homepage.url)
        ppg = portal.ppg
        ppr = portal.ppr
        content = request.env['blog.post']
        domain = [('website_published','=',True)]
        post_count = content.sudo().search_count(domain)
        url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        pager = request.website.pager(url=url, total=post_count, page=page, step=ppg, scope=5)
        posts = content.sudo().search(domain,  offset=pager['offset'], limit=ppg, order='website_sequence desc, published_date desc')
        values = {
                'pager': pager,
                'posts': posts,
                'bins': TableCompute().process(posts, ppg, ppr),
                'rows': ppr,
                'style': portal.style,
                'over_style': portal.over_style
            }
        return http.request.render('website.homepage',values)
        

        

    
    @http.route(['/change_styles'], type='json', auth="public")
    def change_styles(self, id, style_id):
        blog_post = request.env['blog.post'].browse(id)
        remove = []
        active = False
        style_id = int(style_id)
        for style in blog_post.website_style_ids:
            if style.id == style_id:
                remove.append(style.id)
                active = True
                break
        style = request.env['blog.post.style'].browse(style_id)
        if remove:
            blog_post.write({'website_style_ids': [(3, rid) for rid in remove]})
        if not active:
            blog_post.write({'website_style_ids': [(4, style.id)]})
        return not active

    @http.route(['/change_sequence'], type='json', auth="public")
    def change_sequence(self, id, sequence):
        blog_post = request.env['blog.post'].browse(id)
        if sequence == "top":
            blog_post.set_sequence_top()
        elif sequence == "bottom":
            blog_post.set_sequence_bottom()
        elif sequence == "up":
            blog_post.set_sequence_up()
        elif sequence == "down":
            blog_post.set_sequence_down()
        elif sequence == "reset":
            blog_post.set_sequence_reset()

    @http.route(['/change_size'], type='json', auth="public")
    def change_size(self, id, x, y):
        blog_post = request.env['blog.post'].browse(id)
        return blog_post.write({'website_size_x': x, 'website_size_y': y})
    
    
    
