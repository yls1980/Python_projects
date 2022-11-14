# -*- coding: utf-8 -*-
import peewee
from datetime import  datetime

db_proxy = peewee.Proxy()

class BaseTable(peewee.Model):  # TODO РЕР 8: поправьте стиль кода по всему модулю
    class Meta:
        database = db_proxy

class Wheather(BaseTable):
    dt = peewee.DateTimeField(unique=True)
    temp = peewee.CharField()
    icon = peewee.CharField()
    date_modify = peewee.DateTimeField()

class MethodsDb:

    def __init__(self):
        db = None
        # TODO проверьте наличие базы данных и нужных таблиц, если чего-то нет, то надо их создать вызвав
        #  соответствующие методы

    def create_db(self):
        try:
            self.db = peewee.SqliteDatabase("wheather.db")
            db_proxy.initialize(self.db)
        except Exception as e:
            print(str(e))

    def create_table(self):
        self.db.create_tables([Wheather])

    def ins_row(self,pdate,ptemp,picon):
        return (Wheather
                  .insert(dt=pdate, temp=ptemp, icon=picon, date_modify=datetime.now())
                  .on_conflict('replace')
                  .execute())


    def read_rows(self, dbegin, dend):
        return Wheather.select().where((((Wheather.dt >= dbegin)&(dbegin!=None))|(dbegin==None))&
                                       (((Wheather.dt <= dend)&(dend!=None))|(dend==None))).order_by(Wheather.dt)
