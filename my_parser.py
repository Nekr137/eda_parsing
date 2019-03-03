# -*- coding: utf-8 -*-

from urllib.request import urlopen
import requests, re
from bs4 import BeautifulSoup
import json


class Parser:
    """
    (load page->split_page->parse_elements)
    """
    def __init__(self,url):
        self.page = ''              # new page to analyse
        self.url = url              #
        self.elements = []          # dirty elements
        self.elements_dict = []     # clean elements dict


    def load_page(self, path):
        self.path = path

        while True:
            try:
                self.page = requests.get(self.url + self.path).text
                break
            except:
                print('connection error')

    def split_page_to_elements(self,tag,classs):
        elements_found = [b for b in BeautifulSoup(self.page, "html.parser").find_all(tag, classs)]
        if len(elements_found):
            self.elements += elements_found
            return 1
        else:
            return 0



    def parse_elements(self,tags):
        """
        :param tags: dict list like [{'name':'...','tags':'...'} , {... }]
        :return:     self.elements_dict
        """
        elem_count = len(self.elements)
        for i,element in enumerate(self.elements):
            data = {}                                   # dictionary like {'name':'...',    'time':'...',   ...}
            for elem_tags in tags:                      # find data via tag list
                tmp = self.parse_element(element,elem_tags['tags'])

                if elem_tags.get('function') and tmp:   # eval some function if necessary
                    tmp = elem_tags['function'](self,tmp)
                else:
                    tmp = 0
                data[elem_tags['name']] = tmp           # write to "data" dict

            print('\tGet element info:\t',str(i+1),'/',elem_count)
            self.elements_dict.append(data)             # append data dict
        self.elements = []                              # clear dirty elements
        return self.elements_dict



    def get_href_from_a_tag(self,a_tag):
        return a_tag.get('href')


    def get_text_from_bs_object(self,obj):
        try:
            resp = re.sub(r'\xa0',' ',obj.text.strip())
        except:
            resp = ''
        return resp


    def parse_element(self,element,elem_tags):
        """
        :param element: element from self.elements
        :param elem_tags: list like [('h3','class name'),('span','')]
        :return: inner text
        """
        e = [element]
        for tag in elem_tags:
            e = [e[0].find(tag[0], tag[1])]
        return e[0]

    def get_list_from_ul_li(self,obj):
        """
        Create a dict (json) from ul tag
        :param obj:    ul tag
        :return:        list
        """
        li = []
        for li_tag in obj.find_all('li'):
            p = []
            for p_tag in li_tag.find_all('p'):
                p.append(p_tag.text)
            li.append(p)
        li = {l[0]: l[1:] for l in li}
        return json.dumps(li,ensure_ascii=False)
