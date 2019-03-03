# -*- coding: utf-8 -*-

from my_eda_parser import my_eda_parser


def GetData():
    Japanese = ['recepty/vypechka-deserty/yaponskaya-kuhnya']
    Tay = ['recepty/tayskaya-kuhnya/vypechka-deserty']

    P = my_eda_parser()
    P.parse_url_list()
    return P.get_elements_dict()

def SaveData():
    pass

def main():
    data = GetData()

if __name__ == '__main__':
    main()


