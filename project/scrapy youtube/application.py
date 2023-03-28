import scrapy
import re

class YoutubeSpider(scrapy.Spider):
    name = "PW-Foundation"
    allowed_domains = ["youtube.com"]
    
    def __init__(self, query=None, *args, **kwargs):
        super(YoutubeSpider, self).__init__(*args, **kwargs)
        self.start_urls = ["https://www.youtube.com/" + query + "/videos"]
    
    def parse(self, response):
        urls = []
        thumbnails_links = []
        titles = []
        views = []
        times = []
        
        allchannellist = response.css('a#video-title-link')
        urls = list(set(allchannellist.css('::attr(href)').extract()))

        urls = urls[:5]

        for url in urls:
            exp = "^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?))\??v?=?([^#&?]*).*"
            s = re.findall(exp,url)[0][-1]

            thumbnail_url = f"https://i.ytimg.com/vi/{s}/maxresdefault.jpg"
            thumbnails_links.append(thumbnail_url)

        all_titles = response.css('a#video-title-link')
        titles = all_titles.css('::attr(title)').extract()[:5]

        all_views_time = response.css('span.style-scope.ytd-video-meta-block::text').extract()
        views_time = all_views_time[0:14]
        views = [i for i in views_time if i.endswith("views")]
        times = [i for i in views_time if not i.endswith("views")]

        mydict = {"urls": urls, "thumbnails_links": thumbnails_links, 
                  "titles": titles, "views": views, "time": times}
        yield mydict
