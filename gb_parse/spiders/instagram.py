import json
import scrapy


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    login_url = 'https://www.instagram.com/accounts/login/ajax/'
    allowed_domains = ['www.instagram.com']
    start_urls = ['https://www.instagram.com/']
    
    query_hash = {
        'tag_paginate': '9b498c08113f1e09617a1703c22b2f32'
    }
    {"tag_name": "python",
     "first": 2,
     "after": "QVFEeGhna1dpcnZuQUFfbDQ2eGV1SzZUVWtVMDBuTGc1UnZJVkw4WW1EakpvTF8xVXlJQWRYWXhWVHdBX0hqYWkzLXE3b3BDNVRnbTVpWEVnN0QzSDEtUA=="}
    def __init__(self, login, password, tag_list, *args, **kwargs):
        self.login = login
        self.password = password
        self.tag_list = tag_list
        super(InstagramSpider, self).__init__(*args, **kwargs)
    
    def parse(self, response):
        try:
            js_data = self.js_data_extract(response)
            yield scrapy.FormRequest(
                self.login_url,
                method='POST',
                callback=self.parse,
                formdata={
                    'username': self.login,
                    'enc_password': self.password,
                },
                headers={'X-CSRFToken': js_data['config']['csrf_token']}
            )
        except AttributeError:
            if response.json().get('authenticated'):
                for tag in self.tag_list:
                    yield response.follow(f'/explore/tags/{tag}', callback=self.tag_parse)
        print(1)
    
    def tag_parse(self, response):
        print(1)
    
    def js_data_extract(self, response):
        script = response.xpath('//script[contains(text(), "window._sharedData = ")]/text()').get()
        return json.loads(script.replace("window._sharedData = ", '')[:-1])
