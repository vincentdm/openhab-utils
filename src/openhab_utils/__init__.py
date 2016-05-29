
from sqlalchemy import Table, Column, MetaData, Integer, String
import sqlalchemy
from sqlalchemy.engine import create_engine


import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sqlalchemy.sql.elements import between

__updated__ = "";


class Database:    
    def __init__(self, connection):
        self._connection = connection
        self._engine = create_engine(self._connection)
        self._meta = MetaData(self._engine) 
        
        self._items_table = Table('Items', self._meta, autoload = True)
    
    
    def get_items(self):
        with self._engine.connect() as con:
            
            
            stm = sqlalchemy.select([self._items_table])
            rs = con.execute(stm)
            for row in rs:
                print row
        
    
    
    def get_table_for_item(self, item_name, con = None):    
        itemId = self._get_item_id_for_item(item_name)
        table_name = "Item{}".format(itemId)
        table = Table(table_name, self._meta, autoload = True)
        return table;
    
    def _get_item_id_for_item(self, item_name):
        with self._engine.connect() as con:
            stm = sqlalchemy.select([self._items_table.c.ItemId]).where(self._items_table.c.ItemName == item_name)
            rs =  con.execute(stm)
            return rs.first()[0]
    
    
    '''
        Retrieves the date for an 'Item' from the database.  
        The data can be limited between date_start and date_stop and aggregated 
        using interval_duration and the group_func 
        @param item: Item to retrieve the data from
        @param date_start: Only get the data since ...
        @param date_stop:  only get the data until
        @param interval_duration: Group the data using intervals of this length
        @param group_func: use this callable object to group the data 
    '''
    def get_data_for_item(self, item, date_start = None, date_stop = None, interval_duration = None, group_func = None):
        table = self.get_table_for_item(item)
        stm = sqlalchemy.select([table]).where(between(table.c.Time, date_start, date_stop))
        out = []
        with self._engine.connect() as con:
            rs = con.execute(stm)
            for e in rs:
                out.append((e[0], e[1]))
        return out
        
            
class GraphGenerator():
    def __init__(self, database):
        self._db = database;
        
    def Generate(self, items, date_start, date_end, out_file = None):
        for item in items:
            
            data = self._db.get_data_for_item(item, date_start, date_end)
            x = []
            y = []
            for line in data:
                x.append(line[0])
                y.append(line[1])
                
            plt.plot(x,y, label = item)
        
        plt.legend()
        if out_file is None:
            plt.show()
        else:
            plt.savefig(out_file)
    
    def GenerateLastWeek(self, items, out_file):
        date_end = datetime.now()
        date_start = date_end - timedelta(7)
        self.Generate(items, date_start, date_end, out_file=out_file)
        
        
    def GenerateLastMonth(self, items,out_file):
        date_end = datetime.now()
        date_start = date_end - timedelta(30)
        self.Generate(items, date_start, date_end, out_file=out_file)
        
    def GenerateLastYear(self, items,out_file):
        date_end = datetime.now()
        date_start = date_end - timedelta(365)
        self.Generate(items, date_start, date_end,out_file=out_file)
        
        
    
    
if __name__ == "__main__":
    db = Database("mysql://openhab:openhab@localhost/openhab");
    db.get_items()
    print "Table for Living_Temp2 = {}".format(db.get_table_for_item("Living_Temp2"))
    print "connected"
        