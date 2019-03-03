# -*- coding: utf-8 -*-

from my_eda_parser import my_eda_parser


def GetData(type=None):
    P = my_eda_parser(type)
    P.parse_url_list()
    return P.get_elements_dict()

def SaveData():
    pass

def main():
    Japanese = ['recepty/vypechka-deserty/yaponskaya-kuhnya']
    Tay = ['recepty/tayskaya-kuhnya/vypechka-deserty']
    data = GetData()

if __name__ == '__main__':
    main()


