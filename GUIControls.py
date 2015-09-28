
from GUIObjects import *
from Buckets import *
import tkinter as tk
from tkinter import messagebox
import time
import sys
from PIL import Image, ImageTk

class GUIControls:
    
    def __init__(self: 'GUIControls', height: float, width: float,
                 scale: float, wait: float):
        
        self.wait = wait
        self.prev_state = None
        self.model = Buckets()
        self.blinking = False
        self.moves = 0
        self.bucket_to_move = None
        self.scale = scale
        self.height = height
        self.width = width
        
        self.root = tk.Tk()
        self.canvas = tk.Canvas(self.root, background="white",
                           height=height, width=width)
        self.canvas.pack(expand=True, fill=tk.BOTH)     
        
        self.moves_label = tk.Label(self.root)  
        self.moves_label.pack()  
        
        #Bucket configuration
        size_m = self.model.m
        size_n = self.model.n
        #height = self.scale * self.height
        #width = self.scale * self.width
        #x_mid_m = (1/3)*width + (1/2)*(1/3)*width 
        #y_mid = height // 2
        #x_mid_n = (2/3)*width + (1/2)*(1/3)*width 
        height_m = 25+40*size_m
        height_n = 25+40*size_n
        width = 200
        x_mid_m = 550
        x_mid_n = 850
        y_mid = 250        
        
        self.bucket_m = BucketView(size_m, height_m, width, x_mid_m, y_mid,
                              lambda c: self.select(c), self.canvas, 0)       
        self.bucket_n = BucketView(size_n, height_n, width, x_mid_n, y_mid,
                              lambda c: self.select(c), self.canvas, 1)  
        
        self.bucket_config = [size_m,size_n,height_m,height_n,width,x_mid_m,x_mid_n,
                              y_mid]
        
        #Widget configuration   
        #FIX THIS
        #height = self.scale * self.height
        #width = self.scale * self.width
        #x_mid_m = (1/3)*width + (1/2)*(1/3)*width 
        #y_mid = height // 2
        #x_mid_n = (2/3)*width + (1/2)*(1/3)*width 
        height = 250
        width = 400
        x_mid = 200
        y_mid_water = 125
        y_mid_pipe = 375
        self.widget_water = WidgetView(height, width, x_mid, y_mid_water,
                               lambda c: self.select(c), self.canvas, 0,self.root) 
        
        self.widget_pipe = WidgetView(height, width, x_mid, y_mid_pipe,
                               lambda c: self.select(c), self.canvas, 1) 
     
        self.pipe_config = [height, width, x_mid, y_mid_water,y_mid_pipe]
        
        self.canvas.create_text( 200, 125, text='Water',
                                 font=("Purisa", 16), tag="water")         
        self.canvas.create_text( 200, 375, text='Empty',
                                 font=("Purisa", 16), tag="empty")     
        self.water_m = None
        self.water_n = None
        self.update_water_size(1)            
        self.update_bucket_size()  
        
        self.footer = self.canvas.create_rectangle(0, 520, 1100, 700,fill='grey')
    
        self.canvas.create_text( 75, 560, text='Goal:  '+str(self.model.k),
                                 font=("Purisa", 24), tag="goal")
        self.canvas.create_text( 275, 580, text='Minimum Moves:  '+
                                 str(self.model.optimal_moves),
                                 
                                 font=("Purisa", 16), tag="optimal")           
        self.again = ButtonView(50,150,890,560, lambda c: self.solution(),
                                self.canvas)         
        self.canvas.create_text( 890, 560, text='Solve', font=("Purisa", 16),
                                 tag="solve")
        
        self.canvas.create_text( 280, 550, text='Current Moves:  '+ 
                                 str(self.model.move_counter),
                                 font=("Purisa", 16), tag="move_count") 
        
        self.path = pathfix(self.model.path)
    
        self.show_number_of_moves()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  
        #self.root.mainloop()           
    def on_closing(self:'GUIControls'):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
        
    def solution(self:'GUIControls'): 
        self.model.state = (0,0)
        self.update_water_size(1)            
        self.update_bucket_size()    

        for state in reversed(self.path.stack):
            if state[1] == 0:
                self.moves +=1 
                self.model.move_counter+=1
                self.show_number_of_moves()                
            elif state[1] == 1:
                self.canvas.create_text( 550, 560, text='Fill First Bucket',
                                         font=("Purisa", 20), tag="instr")
                self.select(self.bucket_m)
                time.sleep(self.wait)               
                self.select(self.widget_water)
                time.sleep(self.wait)     
                self.canvas.delete("instr")
                time.sleep(self.wait)
            elif state[1] == 2:
                self.canvas.create_text( 550, 560, text='Fill Second Bucket',
                                         font=("Purisa", 20), tag="instr")
                
                self.select(self.bucket_n)
                time.sleep(self.wait)
                self.select(self.widget_water)
                time.sleep(self.wait)
                self.canvas.delete("instr")
                time.sleep(self.wait)
            elif state[1] == 3:
                self.canvas.create_text( 550, 560, text='Empty First Bucket',
                                         font=("Purisa", 20), tag="instr")
                
                self.select(self.bucket_m)
                time.sleep(self.wait)
                self.select(self.widget_pipe)
                time.sleep(self.wait)
                self.canvas.delete("instr")
                time.sleep(self.wait)
            elif state[1] == 4:
                self.canvas.create_text( 550, 560, text='Empty Second Bucket',
                                         font=("Purisa", 20), tag="instr")
                
                self.select(self.bucket_n)
                time.sleep(self.wait)
                self.select(self.widget_pipe)
                time.sleep(self.wait)
                self.canvas.delete("instr")
                time.sleep(self.wait)
            elif state[1] == 5:
                self.canvas.create_text( 550, 560, text="Second bucket -> First", font=("Purisa", 20), tag="instr")
                self.select(self.bucket_n)
                time.sleep(self.wait)
                self.select(self.bucket_m)
                time.sleep(self.wait)
                self.canvas.delete("instr")
                time.sleep(self.wait)
            else:
                self.canvas.create_text( 550, 560, text="First bucket -> Second", font=("Purisa", 20), tag="instr")
                self.select(self.bucket_m)
                time.sleep(self.wait)
                self.select(self.bucket_n)
                time.sleep(self.wait)     
                self.canvas.delete("instr")
                time.sleep(self.wait)
        
    def update_water_size(self:'GUIControls', init: bool): 
        self.model.re_frac()
        y_mid = self.bucket_config[7]
        width = self.bucket_config[4]
        height_m = self.bucket_config[2]
        height_n = self.bucket_config[3]
        x_mid_m = self.bucket_config[5]
        x_mid_n = self.bucket_config[6]        
        #if (init):            
            #width_w = width-40
            #y_mid_m = y_mid - 10 
            #y_mid_n = y_mid - 10 
            #height_w_m = 0
            #height_w_n = 0         
            
            #self.water_m = WaterView(height_w_m,width_w,x_mid_m,y_mid_m,
                                #lambda c: self.select(self.bucket_m), self.canvas)    
            #self.water_n = WaterView(height_w_n,width_w,x_mid_n,y_mid_n,
                                #lambda c: self.select(self.bucket_n), self.canvas)     
            
            #self.water_config = [height_w_m,height_w_n,width_w,x_mid_m,x_mid_n,y_mid_m,y_mid_n]
            #self.root.update()
        #else:
        #self.water_m.remove()
        #self.water_n.remove()
        if self.water_m:
            self.water_m.remove()   
        if self.water_n:
            self.water_n.remove()         
        if self.model.m_frac == 0 :
            y_mid_m = y_mid - 10 
            height_w_m = 0
        else:
            new = self.opp(self.model.state[0],self.model.m)
            y_mid_m = y_mid + (.5*height_m)*(new) - 10
            frac = self.model.state[0]/self.model.m
            height_w_m = (frac)*(height_m) - 20
        if self.model.n_frac == 0 :
            y_mid_n = y_mid - 10 
            height_w_n = 0
        else:
            new = self.opp(self.model.state[1],self.model.n)
            y_mid_n = y_mid + (.5*height_n)*(new) - 10
            frac = self.model.state[1]/self.model.n
            height_w_n = (frac)*(height_n) - 20  
        
        if self.model.state[0] >0:
            self.water_m = WaterView(height_w_m,width-40,x_mid_m,y_mid_m,
                            lambda c: self.select(self.bucket_m), self.canvas)
        if self.model.state[1] >0:           
            self.water_n = WaterView(height_w_n,width-40,x_mid_n,y_mid_n,
                            lambda c: self.select(self.bucket_n), self.canvas)
            
        self.water_config = [height_w_m,height_w_n,width,x_mid_m,x_mid_n,y_mid_m,y_mid_n]
        self.root.update()
        self.bucket_config = [self.model.m,self.model.n,height_m,height_n,width,x_mid_m,                      x_mid_n,y_mid]  
        self.update_bucket_size()
        self.win_check()    
        
    def opp(self,top,bot):
        new = bot - top
        return (new/bot)
    
    def win_check(self):
        if (self.model.state[0]==self.model.k) or (self.model.state[1]==self.
                                                   model.k):
            self.canvas.delete("goal")
            self.canvas.delete("move_count")
            self.canvas.create_rectangle(0,0, 1000, 1000, fill="grey")
            self.canvas.create_text( 700, 125, text='Ayy',
                                 tag="win")   
            self.again = ButtonView(75,150,300,300,
                                lambda c: self.restart(), self.canvas) 
            
    def restart(self: 'GuiControls'):
        self.root.destroy()
        gui = GUIControls(600,1000,1,.75)    
        tk.mainloop()        
        
    def update_bucket_size(self:'GUIControls'):
        
        bucket_m = str(self.model.state[0]) + "/" + str(self.model.m)
        bucket_n = str(self.model.state[1]) + "/" + str(self.model.n)
        self.canvas.delete("frac_m")
        self.canvas.delete("frac_n")
        self.canvas.create_text( 550, 250, text=bucket_m,tag="frac_m")
        self.canvas.create_text( 850, 250, text=bucket_n,tag="frac_n")
        
    def select(self: 'GUIControls', Object: 'ObjectView'):
        self.prev_state = self.model.state
        if not self.blinking:    
            #print(stool, stool_index, cheese)
            if self.bucket_to_move is None:    #First object to move
                if type(Object) is WidgetView:
                    self.root.update()
                elif type(Object) is WaterView:
                    self.root.update()
                else: #BucketView
                    self.bucket_to_move = Object
                    self.bucket_to_move.highlight(True)
                    self.root.update()
            elif type(self.bucket_to_move) is BucketView: 
                #A Bucket already selected
                #FIX THIS
                if type(Object) is WidgetView:  #Bucket -> clicked widget
                    if Object.widget_type == 0: #Water
                        if self.bucket_to_move.bucket_no == 0: #first bucket
                            self.model.state = (self.model.m,self.model.state[1])
                        else:
                            self.model.state = (self.model.state[0],self.model.n)
                        self.bucket_to_move.highlight(False)
                        self.bucket_to_move = None  
                        self.update_bucket_size()
                        self.update_water_size(0)
                        self.root.update()
                    else: #Garbage
                        if self.bucket_to_move.bucket_no == 0: #first bucket
                            self.model.state = (0,self.model.state[1])
                        else:
                            self.model.state = (self.model.state[0],0)
                        self.bucket_to_move.highlight(False)
                        self.bucket_to_move = None
                        self.update_bucket_size()
                        self.update_water_size(0)                        
                        self.root.update()  
                else:   #Bucket -> other bucket  #FIX THISASDASDS
                    if self.bucket_to_move.bucket_no == 0: #first bucket
                        self.model.state = (max(self.model.state[0]+self.model.state[1] - 
                            self.model.n,0), 
                         min(self.model.state[0]+self.model.state[1], 
                             self.model.n))

                    else:
                        self.model.state = (min(self.model.state[0]+self.model.state[1], 
                             self.model.m), 
                         max(self.model.state[0]+self.model.state[1] -
                             self.model.m, 0))
                    self.model.re_frac()
                    self.bucket_to_move.highlight(False)
                    self.bucket_to_move = None
                    self.update_bucket_size()
                    self.update_water_size(0)                        
                    self.root.update()
                
                if self.prev_state != self.model.state:    
                    self.moves +=1 
                    self.model.move_counter+=1
                    self.show_number_of_moves()
            else:
                self.root.update()
        else:
            self.blinking = False
                
    def show_number_of_moves(self: 'GUIView'):
        """Show the number of moves so far."""
        
        self.canvas.delete("move_count")
        self.canvas.create_text( 280, 550, text='Current Moves:  '+ 
                                 str(self.model.move_counter),
                                 font=("Purisa", 16), tag="move_count") 

    def show_goal(self: 'GUIView'):
        """Show the number of moves so far."""
        self.moves_label.config(text='Goal: ' +
                                str(self.model.k))        
if __name__ == '__main__':
    gui = GUIControls(600,1000,1,.75)    
    tk.mainloop()
