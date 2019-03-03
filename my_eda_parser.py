# -*- coding: utf-8 -*-
from my_parser import Parser
import pandas as pd
import json
import re

class my_eda_parser:
    url = 'https://eda.ru/'
    path_list = ['recepty/vypechka-deserty/yaponskaya-kuhnya',
                'recepty/tayskaya-kuhnya/vypechka-deserty']

    def get_ingredient(self,obj):
        p = []
        for p_tag in obj.find_all('p'):
            p.append([
                p_tag.find_all('span')[1].text.strip(),
                p_tag.find_all('span')[2].text
            ])
        return json.dumps(
            {l[0]: l[1:] for l in p},
            ensure_ascii=False
        )

    def get_steps(self,obj):
        """
        Get recept steps from tag.
        :param obj: tag
        :return:    list of rules
        """
        steps = []
        for step in obj.find_all('span','instruction__description'):
            num = step.find('span').text.strip()        # number of step
            text = step.text.strip()                    # step rule
            steps.append(re.sub(num,'',text).strip())   # delete number from rule text and append to list of rules
        return steps

    tags = [
        {
            'name': 'name',
            'tags': [('h3', 'horizontal-tile__item-title'), ('span', '')],
            'function':Parser.get_text_from_bs_object
        },
        {
            'name': 'link',
            'tags': [('h3', 'horizontal-tile__item-title'), ('a', '')],
            'function':Parser.get_href_from_a_tag
        },
        {
            'name': 'prep_time',
            'tags': [('span', 'prep-time')],
            'function': Parser.get_text_from_bs_object
        },
        {
            'name': 'author',
            'tags': [('div', 'horizontal-tile__author'), ('span', 'horizontal-tile__author-link')],
            'function': Parser.get_text_from_bs_object
        },
    ]

    tags2 = [
        {
            'name': 'nutrition',
            'tags': [('ul', 'nutrition__list')],
            'function': Parser.get_list_from_ul_li,
        },
        {
            'name': 'ingredients',
            'tags': [('div', 'ingredients-list__content')],
            'function': get_ingredient
        },
        {
            'name': 'recept_name',
            'tags': [('h1','recipe__name g-h1')],
            'function': Parser.get_text_from_bs_object,
        },
        {
            'name': 'like',
            'tags':[('span','likes__counter js-likes-like-counter')],
            'function': Parser.get_text_from_bs_object,
        },
        {
            'name': 'dislike',
            'tags': [('span', 'likes__counter js-likes-dislike-counter')],
            'function': Parser.get_text_from_bs_object,
        },
        {
            'name': 'bookmark',
            'tags': [('span', 'counter js-bookmark__counter')],
            'function': Parser.get_text_from_bs_object,
        },
        {
            'name': 'steps',
            'tags': [('ul', 'recipe__steps')],
            'function': get_steps,
        }
    ]

    def __init__(self, url=None, path_list=None):
        if path_list:
            self.path_list = path_list        # possibility to change url list
        if url:
            self.url = url


    def parse_url_list(self):
        """
        :return: self.elements_dict - dict of elements got via Parser and some my_eda_parser's methods
        """
        P = Parser(self.url)
        for path in self.path_list:
            page = 1
            print('load ', path)
            while True:             # while pagination list contains data
                print('Get page: ',page)

                P.load_page(path=path + '?page=' + str(page))
                if not P.split_page_to_elements(tag='div',classs='clearfix'):
                    break           # if pagination page is empty
                page += 1

                # В этом месте можено сделать сохранение части полученных данных, а можно накапливать в списке
                # self.elements, а обработать потом

                self.elements_dict = P.parse_elements(self.tags)      # get data and clear self.elements
            #P.elements_dict = []                                     # can be accumulated, but we clean it
        self.get_recepts()                                            # get additional data
        del P

    def get_elements_dict(self):
        return self.elements_dict



    def get_recepts(self):
        """
        Get recept of every element in self.elements_dict
        """
        dict_count = len(self.elements_dict)
        for i,e in enumerate(self.elements_dict):
            print('\t\tGet recept:\t', str(i+1), '/', dict_count,'\t',e['name'])
            R = Parser(self.url)                                      # new Parser object to parse inner information
            R.load_page(e['link'])
            R.split_page_to_elements(tag='section',classs='recipe')

            additional_elements = R.parse_elements(self.tags2)[0]
            for t in self.tags2:
                e[t['name']] = additional_elements.get(t['name'])     # append additional info to self.get_recepts
            del R






    #





