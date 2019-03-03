# -*- coding: utf-8 -*-

from eda_parsing.my_eda_parser import my_eda_parser


def GetData():
    P = my_eda_parser()
    P.parse_url_list()
    return P.get_elements_dict()

def SaveData():
    pass

def main():
    data = GetData()



if __name__ == '__main__':
    main()


