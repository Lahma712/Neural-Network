import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image as Bg
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.textinput import TextInput
from kivy.core.image import Image as CoreImage
from kivy.clock import Clock
from Grid import Grid, Cells, drawCell, drawFrame
from kivy.graphics import Rectangle
import math
from kivy.uix.label import Label
from io import BytesIO
from PIL import Image, ImageDraw
import tensorflow as tf
import numpy as np
kivy.require("2.0.0")

class Drw(Widget):
	Height = 500
	Width = Height * 2
	Window.size = (Width, Height)
	BgColor = (0,0,0)
	GridColor = (20,20,20)
	CellColor = (255,0,0)
	CurrentCells = []
	Im = Image.new("RGB", (Height, Height), BgColor)
	byte_io = BytesIO()
	Im.save(byte_io, 'PNG')
	Net = tf.keras.models.load_model('network.model')

	def __init__(self,**kwargs):
		super(Drw, self).__init__(**kwargs)
		self.CellCount = 28 #initial number of columns

		with self.canvas:
			self.array = np.zeros((28,28))
			self.Im = Image.open(self.byte_io)
			self.draw = ImageDraw.Draw(self.Im)
			self.Grids = Grid(28, self.Height, self.Height, self.draw, self.GridColor)
			self.Cells = Cells(self.Grids[0], self.Grids[1]) #3D list of all the cell coordinates eg [ [[0,1,2,3], [5, 6, 7]....], [[0,1,2,3,4], [6,7,8,9]....] . 1st list holds x coordinate lists and 2nd list y coordinate lists
            
			self.byte_io = BytesIO()
			self.Im.save(self.byte_io, 'PNG')
			self.bg = Bg(texture = self.ImageByte(self, self.byte_io.getvalue()).texture, pos=(0, 0), size = (self.Height, self.Height)) #background

			self.clear = Button(text="clear", font_size=self.Height*0.05, size = (self.Width *0.25, self.Height*0.10), pos =(self.Height, self.Height * 0.90))
			self.clear.bind(on_press = self.Clear)
			self.add_widget(self.clear)
		

			self.ZeroRectangle = Rectangle(pos = (self.Width/2, self.Height*0.10), size = (self.Width/2*0.10, 0))
			self.OneRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.10, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.TwoRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.20, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.ThreeRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.30, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.FourRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.40, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.FiveRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.50, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.SixRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.60, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.SevenRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.70, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.EightRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.80, self.Height*0.10), size = (self.Width/2*0.05, 0))
			self.NineRectangle = Rectangle(pos = (self.Width/2 + (self.Width/2) * 0.90, self.Height*0.10), size = (self.Width/2*0.05, 0))

			self.ZeroLabel = Label(text = '  0', pos= (self.Width/2,self.Height*0.05), size=(10,10))
			self.OneLabel = Label(text = '  1', pos= (self.Width/2+ (self.Width/2) * 0.10,self.Height*0.05), size=(10,10))
			self.TwoLabel = Label(text = '  2', pos= (self.Width/2+ (self.Width/2) * 0.20,self.Height*0.05), size=(10,10))
			self.ThreeLabel = Label(text = '  3', pos= (self.Width/2+ (self.Width/2) * 0.30,self.Height*0.05), size=(10,10))
			self.FourLabel = Label(text = '  4', pos= (self.Width/2+ (self.Width/2) * 0.40,self.Height*0.05), size=(10,10))
			self.FiveLabel = Label(text = '  5', pos= (self.Width/2+ (self.Width/2) * 0.50,self.Height*0.05), size=(10,10))
			self.SixLabel = Label(text = '  6', pos= (self.Width/2+ (self.Width/2) * 0.60,self.Height*0.05), size=(10,10))
			self.SevenLabel = Label(text = '  7', pos= (self.Width/2+ (self.Width/2) * 0.70,self.Height*0.05), size=(10,10))
			self.EightLabel = Label(text = '  8', pos= (self.Width/2+ (self.Width/2) * 0.80,self.Height*0.05), size=(10,10))
			self.NineLabel = Label(text = '  9', pos= (self.Width/2+ (self.Width/2) * 0.90,self.Height*0.05), size=(10,10))


	def ImageByte(self, instance, ImageByte):
		self.Buffer = BytesIO(ImageByte)
		self.BgIm = CoreImage(self.Buffer, ext= 'png')
		return self.BgIm

	def save(self, instance):
		self.byte_io = BytesIO()
		self.Im.save(self.byte_io, 'PNG')
		with self.canvas:
			self.bg.texture = self.ImageByte(self, self.byte_io.getvalue()).texture

	def Clear(self, instance):

		drawFrame(self.draw, self.CurrentCells, self.Cells, self.BgColor)
		self.save(self)
		self.CurrentCells =[]
		self.array = np.zeros((28,28))

	def Draw(self, instance, X):
		self.XcellList = [x for x in self.Cells[0] if self.Xtouch+X in x][0] #finds the pixel X coordinates list containing the X coordinate you clicked with the mouse 
		self.YcellList = [x for x in self.Cells[1] if self.Ytouch+X in x][0]#finds the pixel Y coordinates list containing the Y coordinate you clicked with the mouse 
		self.cellIndexList = [self.Cells[0].index(self.XcellList), self.Cells[1].index(self.YcellList)] # produces a column/row list [column, row] of the cell you clicked with the mouse
		self.color = self.CellColor
		#if self.cellIndexList not in self.CurrentCells: #checks if the cell you clicked is already clicked, if not the [column, pair] gets added to CurrentCells and the cell gets colored
		self.CurrentCells.append([self.cellIndexList[0], self.cellIndexList[1]])
		self.CurrentCells.append([self.cellIndexList[0]+1, self.cellIndexList[1]])
		self.CurrentCells.append([self.cellIndexList[0]+1, self.cellIndexList[1]-1])
		self.CurrentCells.append([self.cellIndexList[0], self.cellIndexList[1]-1])
		


		#elif self.checkSingleClick == True and self.cellIndexList in self.CurrentCells: #if you only clicked once, and on a cell that is already clicked/activated, it gets erased again
			#self.CurrentCells.remove(self.cellIndexList)
			#self.color = self.BgColor



		drawCell(self.XcellList,self.YcellList, self.color, self.draw)
		drawCell(self.Cells[0][self.cellIndexList[0]+1], self.Cells[1][self.cellIndexList[1]], self.color, self.draw)
		drawCell(self.Cells[0][self.cellIndexList[0]+1], self.Cells[1][self.cellIndexList[1]-1], self.color, self.draw)
		drawCell(self.Cells[0][self.cellIndexList[0]], self.Cells[1][self.cellIndexList[1]-1], self.color, self.draw) #function that draws (or erases, based on the previous conditions) the cell you clicked
		
		self.save(self)
		
		self.array[self.cellIndexList[1], self.cellIndexList[0]+1] = 1.0
		self.array[self.cellIndexList[1]-1, self.cellIndexList[0]+1] = 1.0
		self.array[self.cellIndexList[1]-1, self.cellIndexList[0]] = 1.0
		self.array[self.cellIndexList[1], self.cellIndexList[0]] = 1.0

		self.PredImage = np.expand_dims(self.array,0)

		self.PredValue = self.Net.predict(self.PredImage)
		
		with self.canvas:

			self.ZeroRectangle.size = (self.Width/2*0.05, self.PredValue[0][0] * self.Height * 0.60)
			self.OneRectangle.size = (self.Width/2*0.05, self.PredValue[0][1] * self.Height * 0.60)
			self.TwoRectangle.size = (self.Width/2*0.05, self.PredValue[0][2] * self.Height * 0.60)
			self.ThreeRectangle.size = (self.Width/2*0.05, self.PredValue[0][3] * self.Height * 0.60)
			self.FourRectangle.size = (self.Width/2*0.05, self.PredValue[0][4] * self.Height * 0.60)
			self.FiveRectangle.size = (self.Width/2*0.05, self.PredValue[0][5] * self.Height * 0.60)
			self.SixRectangle.size = (self.Width/2*0.05, self.PredValue[0][6] * self.Height * 0.60)
			self.SevenRectangle.size = (self.Width/2*0.05, self.PredValue[0][7] * self.Height * 0.60)
			self.EightRectangle.size = (self.Width/2*0.05, self.PredValue[0][8] * self.Height * 0.60)
			self.NineRectangle.size = (self.Width/2*0.05, self.PredValue[0][9] * self.Height * 0.60)

		
		
		


	def onTouchFunctions(self, touch):
		self.touchpos = touch.pos #tuple that contains the X/Y coords of your mouse click
		self.Xtouch = math.floor(self.touchpos[0]) #rounds the coords down
		self.Ytouch = math.floor(abs(self.touchpos[1]-self.Height)) #inverts the Y coord. In kivy the origin (0,0) is bottom left, in PIL it is top left
		try: 
			self.Draw(self, 0) 
			super(Drw, self).on_touch_down(touch) 

		except(IndexError): #if you press exactly on a grid pixel (in between 2 cells), you would get an Index error. In that case, just move your mouseclick 1 pixel up and left
			try:
				self.Draw(self, -1)
				super(Drw, self).on_touch_down(touch) 
			except(IndexError): #if you press on a grid pixel at the border of the window, just do nothing
				super(Drw, self).on_touch_down(touch)

	def on_touch_down(self, touch): #function if you only click once
		self.checkSingleClick = True
		self.onTouchFunctions(touch)

	def on_touch_move(self, touch): #function if you click once and then start moving (with button still pressed). Is used for drawing lines 
		self.checkSingleClick = False
		self.onTouchFunctions(touch)



class Net(App):
	def build(self):
		return Drw()

if __name__ == "__main__":
	Net().run()