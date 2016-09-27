'''
Created on 27-sep.-2016

@author: vincent
'''


import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from database import Database

class Generator():
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
    
    def GenerateLastDay(self, items, out_file):
        date_end = datetime.now()
        date_start = date_end - timedelta(1)
        self.Generate(items, date_start, date_end, out_file=out_file)
    
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
        
        