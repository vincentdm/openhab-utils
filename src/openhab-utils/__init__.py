
from sqlalchemy import Table, Column, MetaData, Integer, String
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy.sql.sqltypes import String


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
            
            
class GraphGenerator():
    def __init__(self, database):
        self._db = database;
        
    def Generate(self, items, period = "day", start = None, stop = None, interval = None):
        pass
    
    
if __name__ == "__main__":
    db = Database("mysql://root:4mandsb3rG@localhost/openhab");
    db.get_items()
    print "Table for Living_Temp2 = {}".format(db.get_table_for_item("Living_Temp2"))
    print "connected"
        