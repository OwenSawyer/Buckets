

from Buckets import *
from tkinter import *

class ObjectView:
    
    def __init__(self: 'Object', height: float, width: float, 
                 x_mid: float, y_mid: float,                 
                 onclick: (lambda Event: None), canvas: Canvas):
        self.canvas = canvas
        self.height = height
        self.width = width
        self.x_mid = x_mid
        self.y_mid = y_mid


        self.index = canvas.create_rectangle(0, 0, 0, 0)
        self.canvas.itemconfig(self.index)

        self.place(x_mid, y_mid)


        canvas.tag_bind(self.index,
                        '<ButtonRelease>',
                        lambda _: onclick(self))    
        
    def place(self: 'ObjectView', x_mid: float,
              y_mid: float):
        """
        Place rectangular image of this cheese/stool at (x_center, y_center)
        """
        # corners are half of size or thickness away
    
        self.canvas.coords(self.index,
                           (x_mid - self.width // 2),
                           (y_mid - self.height // 2),
                           (x_mid + self.width // 2),
                           (y_mid + self.height // 2))
        # record new center
        self.x_mid = x_mid
        self.y_mid = y_mid
        
        
class BucketView(Buckets, ObjectView):
    def __init__(self: 'BucketView',
                 size: int, height: float, width: float,
                 x_mid: float, y_mid: float,
                 onclick: (lambda Event: None), canvas: Canvas, bucket_no: float):
        self.bucket_no = bucket_no
        ObjectView.__init__(self, height, width, x_mid, y_mid,
                              onclick, canvas)
        #Buckets.__init__(self, size)

        self.size = size
        # Initially unhighlighted.
        self.highlight(False)

    def highlight(self: 'BucketView', highlighting: bool):


        self.canvas.itemconfigure(self.index,
                                  fill=('red' if highlighting else 'grey'))

        
class WidgetView(ObjectView):
    
    def __init__(self: 'WidgetView', height: float, width: float,
                 x_mid: float, y_mid: float, onclick: (lambda Event: None), 
                 canvas: Canvas, widget_type: float):
        self.widget_type = widget_type
        ObjectView.__init__(self, height, width, x_mid, y_mid,
                              onclick, canvas)
        if widget_type == 0: #water
            self.canvas.itemconfigure(self.index, fill='blue')        
        else: #pipe
            self.canvas.itemconfigure(self.index, fill='green')  
            
class WaterView:
    
    def __init__(self: 'WaterView', height: float, width: float, 
                 x_mid: float, y_mid: float,                 
                 onclick: (lambda Event: None), canvas: Canvas):

        self.canvas = canvas
        self.height = height
        self.width = width
        self.x_mid = x_mid
        self.y_mid = y_mid

        self.index = canvas.create_rectangle(0, 0, 0, 0)
        self.canvas.itemconfig(self.index)

        self.place(x_mid, y_mid)
        self.canvas.itemconfigure(self.index, fill='blue') 


        canvas.tag_bind(self.index,
                        '<ButtonRelease>',
                        lambda _: onclick(self))          
    
    def remove(self: 'WaterView'):
        self.canvas.delete(self.index)
    def place(self: 'ObjectView', x_mid: float,
              y_mid: float):
    
        self.canvas.coords(self.index,
                           (x_mid - self.width // 2),
                           (y_mid - self.height // 2),
                           (x_mid + self.width // 2),
                           (y_mid + self.height // 2))
        # record new center
        self.x_mid = x_mid
        self.y_mid = y_mid