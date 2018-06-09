# -*- coding: utf-8 -*-
"""
-------------------------------------------------

@File    : base.py

Description : 基础类

@Author :       pchaos

date：          18-6-5
-------------------------------------------------
Change Activity:
               18-6-5:
@Contact : p19992003#gmail.com                   
-------------------------------------------------
"""
__author__ = 'pchaos'

from django.db import models
from django.db import transaction
import pandas as pd
import datetime


class StockBase(models.Model):
    """ StockBase为所有model的基类，提供共用的类函数

    """

    @classmethod
    def saveModel2File(cls, filename=None, dropPk=True):
        if not filename:
            # 文件名未赋值，则自动产生文件名
            filename = '{}_{}.pkl.gz'.format(cls.__name__, datetime.datetime.now().date())
        from django.forms import model_to_dict
        aobjs = [model_to_dict(aobj) for aobj in cls.objects.all()]
        df = pd.DataFrame(aobjs)
        cls.dropDataframePK(df, dropPk)
        df.to_pickle(filename)
        return filename

    @classmethod
    def loadModelFromFile(cls, filename=None, dropPk=True):
        if filename:
            df = pd.read_pickle(filename)
            cls.dropDataframePK(df, dropPk)
            cls.savedf(df)
        else:
            print('文件名为空，请传正确的文件名！')

    @classmethod
    def savedf(cls, df):
        entries = df.to_dict('records')
        with transaction.atomic():
            for v in entries:
                _, created = cls.objects.get_or_create(**v)
                # if  created:
                #     print('exists:{}'.format(v))

    @staticmethod
    def getRandomStr(types='letter', length=8):
        """ 随机产生length长度的字符串

        :param types: 随机字符串的类型
        types in ['letter', 'ascii'] 返回包含字母的字符串
        types in ['digit', 'num']: 返回包含数字的字符串
        其他：返回混合字母和数字的字符串

        :param length: 返回字符串的长度
        :return: 长度为length，类型为types的字符串
        """
        import random
        import string
        if types in ['letter', 'ascii']:
            return ''.join(random.sample(string.ascii_letters, length))
        if types in ['digit', 'num']:
            return ''.join(random.sample(string.digits, length))
        else:
            return ''.join(random.sample(string.ascii_letters + string.digits, length))

    @staticmethod
    def dropDataframePK(df, dropPk):
        """ 删除无明确意义的主键字段.
        如果是有业务逻辑意义的主键不能删除

        :param df:
        :param dropPk:
        :return:
        """
        if dropPk:
            pkname = 'id'
            if pkname in list(df.columns):
                #  主键在保存的dataFrame中
                df.drop(pkname, axis=1, inplace=True)

    @staticmethod
    def dfNotInAnotherdf(df1, df2):
        df = pd.merge(df1, df2, how='outer', indicator=True)
        rows_in_df1_not_in_df2 = df[df['_merge'] == 'left_only'][df1.columns]

        return rows_in_df1_not_in_df2

    @staticmethod
    def compareList(list1, list2):
        """ Check if two unordered lists are equal [duplicate]

        :param list1:
        :param list2:
        :return: list1 == list2 return True
        others return False
        """
        import collections
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        return compare(list1, list2)

    class Meta:
        abstract = True