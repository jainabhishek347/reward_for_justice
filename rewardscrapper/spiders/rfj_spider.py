import json
import scrapy
from scrapy import Selector
from scrapy import Item, Field


class RewardItem(Item):
    title = Field()
    page_url = Field()
    reward = Field()
    ass_org = Field()
    ass_loc = Field()
    about = Field()
    img_urls = Field()
    category = Field()
    dob = Field()


class RFJ_Spider(scrapy.Spider):
    name = 'rfj_spider'
    allowed_domains = ['rewardsforjustice.net']

    def start_requests(self):
        url = 'https://rewardsforjustice.net/index/?jsf=jet-engine%3Arewards-grid&tax=crime-category%3A1070%2C1071%2C1073%2C1072%2C1074&nocache=1660557920'
        form_data = {'action': 'jet_engine_ajax',
            'handler': 'get_listing',
            'page_settings[post_id]' : '22076',
            'page_settings[queried_id]': '22076|WP_Post',
            'page_settings[element_id]': 'ddd7ae9',
            'page_settings[page]' : '1',
            'listing_type' : 'elementor',
            'isEditMode' : 'false',
            'addedPostCSS[]' : '22078'
        }
        return [scrapy.FormRequest(url,
                                   formdata=form_data,
                                   callback=self.logged_in)]

    def new_parsing_method(self, response):
        reward = RewardItem()
        reward['page_url'] = response.url

        try: reward['title'] = response.xpath('//*[@id="hero-col"]/div/div[1]/div/h2/text()')[0].get()
        except: reward['title'] = 'null'

        try: reward['reward'] = response.xpath('//*[@id="reward-box"]/div/div[2]/div/h2/text()')[0].get()
        except: reward['reward'] = 'null'

        try: reward['ass_org'] = response.xpath('string(//*[@id="Rewards-Organizations-Links"]/div)').get().split(':')[1]
        except : reward['ass_org'] = 'null'
        if reward['ass_org']:
            reward['ass_org'] = reward['ass_org'].replace('\n', '').replace('\t', '')

        try: reward['ass_loc'] = response.xpath('//*[@id="reward-fields"]/div/div[5]/div/div/span/text()')[0].get()
        except: reward['ass_loc'] = 'null'

        reward['about'] = response.xpath('string(//*[@id="reward-about"]/div/div[2]/div)').get()
        reward['img_urls'] = response.xpath('//*[@id="gallery-1"]/figure/div/img/@src').extract()
        if not reward['img_urls']:
            reward['img_urls'] = response.xpath('//*[@id="gallery-1"]/figure/div/picture/img/@src').extract()

        reward['category'] = self.category

        reward['dob'] = response.xpath('//div[@class = "elementor-element elementor-element-9a896ea dc-has-condition dc-condition-empty elementor-widget elementor-widget-text-editor"]/div/text()').get()
        if reward['dob'] :
            reward['dob'] = reward['dob'].replace('\n', '').replace('\t', '')

        return reward

    def logged_in(self, response):
        print('**'*30)
        print('Fetching data for url: ', response.url)
        # here you would extract links to follow and return Requests for
        # each of them, with another callback
        dict_response = json.loads(response.text)
        res_html = dict_response['data']['html']
        max_num_pages = dict_response['data']['filters_data']['props']['rewards-grid']['max_num_pages']
        page = dict_response['data']['filters_data']['props']['rewards-grid']['page']
        found_posts = dict_response['data']['filters_data']['props']['rewards-grid']['found_posts']
        selector_elm = Selector(text=res_html)
        self.category = selector_elm.xpath('.//h2[@class="elementor-heading-title elementor-size-default"]/text()').get()
        for url in selector_elm.xpath('.//a[@class="jet-engine-listing-overlay-link"]/@href'):
            yield scrapy.Request(response.urljoin(url.get()), callback=self.new_parsing_method)

        if page < max_num_pages:
            url = 'https://rewardsforjustice.net/index/?jsf=jet-engine%3Arewards-grid&tax=crime-category%3A1070%2C1071%2C1073%2C1072%2C1074&nocache=1660557920'
            url = url + '&pagenum=' + str(page+1)
            form_data = {'action': 'jet_engine_ajax',
                'handler': 'get_listing',
                'page_settings[post_id]' : '22076',
                'page_settings[queried_id]': '22076|WP_Post',
                'page_settings[element_id]': 'ddd7ae9',
                'page_settings[page]' : '1',
                'listing_type' : 'elementor',
                'isEditMode' : 'false',
                'addedPostCSS[]' : '22078'
            }

            yield scrapy.FormRequest(url,
                                       formdata=form_data,
                                       callback=self.logged_in)