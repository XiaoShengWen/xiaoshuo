# -*- coding: utf-8 -*-

import urllib
import urlparse

import tornado.web


class DeleteNote(tornado.web.UIModule):
    """docstring for LeftSidebarModule"""

    def render(self):
        return self.render_string("modules/deletenote.html")


class LeftSidebarModule(tornado.web.UIModule):
    """docstring for LeftSidebarModule"""

    def render(self, page_name, admin_role, admin_user_id = None):
        return self.render_string(
                "modules/leftsidebar.html",
                page_name=page_name,
                admin_role=admin_role,
                admin_user_id=admin_user_id
        )

class HeadJsModule(tornado.web.UIModule):
    """docstring for HeadJsModule"""

    def render(self):
        return self.render_string("modules/headjs.html")

class PagebarModule(tornado.web.UIModule):
    """docstring for PagebarModule"""

    def get_page_url(self, page):
        path = self.request.path
        query = self.request.query
        qdict = urlparse.parse_qs(query)
        for k, v in qdict.items():
            if isinstance(v, list):
                qdict[k] = v and v[0] or ''
        qdict['page'] = page
        return path + '?' + urllib.urlencode(qdict)

    def render(self, page, total, page_size=20, with_last_page=False):
        self.url_func = self.get_page_url
        self.page = 1 if int(page) < 1 else int(page)
        self.total = int(total)
        self.page_size = int(page_size)
        self.page_num = int(((self.total - 1) / self.page_size) + 1) if self.total > 0 else 0
        self.page_bars = {}
        self.data = ()

        for _page in range(1, self.page_num + 1):
            _index = int(_page / 10)
            if not self.page_bars.has_key(_index):
                self.page_bars[_index] = [_page]
            else:
                self.page_bars[_index].append(_page)

        current_start = self.page

        page_bar = self.page_bars.get(int(self.page / 10))

        page_bar_min = max(self.page - 4, 1)
        page_bar_max = min(self.page_num, self.page + 4)
        if page_bar_max - page_bar_min > 10:
            if page_bar_max - self.page >= 4:
                page_bar_max = self.page + 4

            if page_bar_min <= self.page - 4:
                page_bar_min = self.page - 4

        if page_bar_max <= page_bar_min + 9:
            page_bar_max = min(page_bar_min + 8, self.page_num)
            if page_bar_max == self.page_num:
                page_bar_min = max(page_bar_max - 8, 1)


        page_bar = range(page_bar_min, page_bar_max + 1)

        if page_bar is None:
            return ''

        _htmls = []
        _htmls.append('<ul class="pagination">')
        if current_start == 1:
            _htmls.append(u'\t<li class="disabled"><a href="">首页</a></li>')
            _htmls.append(u'\t<li class="disabled"><a href="">&larr; 上一页</a></li>')
        else:
            _htmls.append(u'\t<li><a href="%s">首页</a></li>' % self.url_func(1))
            _htmls.append(u'\t<li><a href="%s">&larr; 上一页</a></li>' % self.url_func(current_start - 1))
        for page in page_bar:
            _page_url = self.url_func(page)
            if page == self.page:
                _htmls.append('\t<li class="active"><a href="">%s</a></li>' % page)
            else:
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (_page_url, page))

        current_end = self.page
        if current_end == self.page_num:
            _htmls.append(u'\t<li class="disabled"><a href="#">下一页 &rarr;</a></li>')
            # if with_last_page:
            #     _htmls.append(u'\t<li class="disabled"><a href="#">尾页</a></li>')
        else:
            if with_last_page:
                _htmls.append('\t<li><a href="%s">%s</a></li>' % (self.url_func(self.page_num), self.page_num))
            _htmls.append(u'\t<li><a href="%s">下一页 &rarr;</a></li>' % self.url_func(current_end + 1))
            # if with_last_page:
            #     _htmls.append(u'\t<li><a href="%s">尾页</a></li>' % self.url_func(self.page_num))

        _htmls.append('</ul>')

        return '\r\n'.join(_htmls)


