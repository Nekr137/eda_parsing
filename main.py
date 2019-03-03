# -*- coding: utf-8 -*-

from my_eda_parser import my_eda_parser
from my_db import my_db


def GetData(type=None):
    P = my_eda_parser(path_list=type)
    P.parse_url_list()
    return P.get_elements_dict()


def SaveData(data):
    username = 'postgres'
    psw = 'denekra'
    table1name = 't3'
    table2name = 't4'

    db = my_db(dbname='edadb2',username=username,password=psw,table1name=table1name,table2name=table2name)
    db.append_data(data)


def main():
    Japanese = ['recepty/vypechka-deserty/yaponskaya-kuhnya']
    Tay = ['recepty/tayskaya-kuhnya/vypechka-deserty']
    data = GetData()   # type = Japanese or Tay, empty == both
    SaveData(data)                  # write data to db


if __name__ == '__main__':
    main()
    print('OK!')


