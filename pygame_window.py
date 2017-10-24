# -*- coding: utf-8 -*-
# Use 4 spaces as a tab
import pygame
import os
from pygame.locals import HWSURFACE, DOUBLEBUF, RESIZABLE, VIDEORESIZE, NOFRAME
from win32api import GetSystemMetrics

# For on top function
from ctypes import Structure, c_long, byref, windll
# 
import io
from PIL import Image


class Rectangle(Structure):
	_fields_ = [
		('left',    c_long),
		('top',     c_long),
		('right',   c_long),
		('bottom',  c_long),
	]
	def width(self):
		return self.right  - self.left
	def height(self):
		return self.bottom - self.top

class PyGameWindow(object):
	"""docstring for PyGameWindow"""
	def __init__(self, window_size, maxfps):
		super(PyGameWindow, self).__init__()
		# Init pygame, create clock, set up display to be resizeable and use hardware acc
		pygame.init()
		self.pygame = pygame
		self.clock = pygame.time.Clock()
		# User's variables
		self.window_size = window_size
		try:
			x = GetSystemMetrics(0) - 350 - window_size[0]
			y = GetSystemMetrics(1) - window_size[1]
			os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)
		except:
			pass
		self.background = (0,0,0)
		self.font = "./georgia.ttf"
		self.font_colour = (255,255,255)
		# Meh, colours are not matched nicely
		self.research_bar_colour = (0x88,0xbb,0xbb)
		self.research_bar_colour_background = (0x88, 0x88, 0x88)
		self.font_size = 12
		self.maxfps = maxfps
		self.fps = 0
		self.noframe = NOFRAME

		# Set screen size, write
		self.screen = self.set_screen(window_size)
		self.pygame.display.set_caption("AoE II - Bartender") 
		self.pygame.display.set_icon(pygame.image.load("icon.png"))	
		self.on_top()

		self.dataset = "Expansions"

	def on_top(self):	
		# Sets the window to be always on the top
		window = self.pygame.display.get_wm_info()['window']
		rc = Rectangle()
		windll.user32.GetWindowRect(window, byref(rc))
		windll.user32.SetWindowPos(window, -1, rc.left, rc.top, 0, 0, 0x0001)

	def change_dataset(self):
		if self.dataset == "Expansions":
			self.dataset = "Original"
		elif self.dataset == "Original":
			self.dataset = "Expansions"


	def set_screen(self, window_size):
		return self.pygame.display.set_mode(window_size,HWSURFACE|DOUBLEBUF|RESIZABLE|self.noframe)
	
	def resize(self, event):
		self.window_size = event.dict['size']
		self.set_screen(self.window_size)
		self.on_top()

	def clear(self):
		self.screen.fill(self.background)

	def message(self, string, coords=None, left=10, top=10):
		if coords is None: 
			coords = (left, top)
		font = self.pygame.font.Font(self.font, self.font_size)
		#font = self.pygame.font.SysFont(None, 20)
		format = lambda x: font.render(x, False, self.font_colour)
		text = format(string)
		self.screen.blit(text, coords)

	def quit(self):
		self.clear()
		# Print hearthfull message. 
		self.message("Thank you for using this addon. ^_^")
		self.update()
		self.pygame.time.wait(500)
		# Quit
		self.pygame.quit()

	# Updates the window, check for events
	def update(self):
		# Get new events
		self.pygame.event.pump()
		# Parse events
		for event in self.pygame.event.get():
			if event.type == self.pygame.QUIT:
				self.quit()
				return False
			if event.type == VIDEORESIZE:
				self.resize(event)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_HOME:
					self.noframe = 0 if self.noframe else NOFRAME
					self.set_screen(self.window_size)
					self.on_top()
				if event.key == pygame.K_ESCAPE:
					self.quit()
					return False
				if event.key == pygame.K_END:
					self.change_dataset()


	
		# Update the display
		self.pygame.display.flip()
		# Dont run faster than MAX_FPS
		self.clock.tick(self.maxfps)
		return True



	
	def display_resources(self, gathered_resources, spent_resources, time):
		"""
		Prints informations about gathered and spent resources.
		+------------------------------------------------+
		| Wood:  xxx/xxx  ' Gold: xxx/xxx  '             |
		| Food:  xxx/xxx  ' Stone: xxx/xxx '             |
		| Time:  xxxx     ' FPS: xx        '             |
		+------------------------------------------------+
		xxx/xxx == gathered_resources/spent_resources
		"""
		# Make the strings of gathered_resources/spent_resources
		balance = tuple(map(lambda x: str(x[0]) + " /" + str(x[1]), 
		                    zip(gathered_resources, spent_resources)))
		# Unpack the tuple
		wood, food, gold, stone = balance
		# Set the length in pixels
		PADDING = 5
		SECOND_COLUMN = 120
		new_line = self.font_size + PADDING

		self.clear()
		self.message("Wood: " + str(wood), (PADDING, PADDING))
		self.message("Food: " + str(food), (PADDING, new_line + PADDING))
		self.message("Gold: " + str(gold), (SECOND_COLUMN, PADDING))
		self.message("Stone: " + str(stone), (SECOND_COLUMN, new_line + PADDING))
		self.message("Time: " + str(time), (PADDING, new_line*2 + PADDING))
		self.message("FPS: " + str('%.2f' % self.get_fps()), (SECOND_COLUMN, new_line*2 + PADDING))
		# Set where the research starts
		self.research_starts = (self.font_size + PADDING)*3 

	def display_researches(self, queue):
		"""
		Print bars and info about the technologies which are currentelly researched. 
		  Padding
		    +----------------------------------- ...
		    |     5px     3px horizontal gap
		    |   #########  1 px vertical gap
		    |5px# ICON1 #  ########### -.
		    |   # 23x23 #  #XXXXXX   #   > 20 px height of the frame
		    |   #       #  ########### -'  18 px height of the researchbar
		    |   #########  2 px vertical gap
		    |      1 px
		    .   #########
		    .   # ICON2 #
		"""
		PADDING = 5
		starts = self.research_starts + PADDING

		new_line = 24
		icon_size = 23
		horizontal_gap = 3
		vertical_gap = 1
		frame_height = 20
		frame_border = 1

		frame_left = PADDING + icon_size + horizontal_gap
		frame_width = self.window_size[0] - frame_left - PADDING
		bar_left = PADDING + icon_size + horizontal_gap + frame_border
		bar_height = frame_height - frame_border*2
		bar_width = frame_width - frame_border*2
		
		for idx, metadata in enumerate(queue):
			# Unpack values
			completed = queue[metadata][0]
			expires = queue[metadata][1] 
			icon = queue[metadata][2] 
			name, time = queue.techs[metadata]
			# Get the time
			research_time_remaining = expires - completed
			# Icon
			icon_top = idx*new_line + starts
			self.show_img(icon, rgb=True, u_size=(icon_size, icon_size), left=PADDING, top=icon_top)
			# Frame calculations
			frame_top = starts + new_line*idx + vertical_gap
			bar_top = frame_top + frame_border
			width = int(bar_width*completed/expires)
			# Frame
			self.pygame.draw.rect(self.screen, self.research_bar_colour_background ,(frame_left, frame_top, frame_width, frame_height))
			# Bar
			self.pygame.draw.rect(self.screen, self.research_bar_colour , (bar_left, bar_top, width, bar_height))
			# Name
			bar_name = name +" " + str(research_time_remaining)+"s"
			self.message(bar_name, (bar_left+PADDING, bar_top+3))


		"""
		Also prints last 10 researched technologies
		"""
		left_start = 240
		top_start = 5
		for idx, research in enumerate(queue.researched[:-11:-1]): # Last ten researches.
			metadata, time, icon = research
			self.show_img(icon, rgb=True, u_size=(icon_size-1, icon_size-1), left=left_start + icon_size*(idx%5), top=top_start + icon_size*(idx//5))
			#if idx >= 10: break # BAD IDEA

			

	
	def error(self, string):
		self.clear()
		self.message(string, top=10)
		self.message("Dataset: " + self.dataset, top=10+self.font_size+5)
		self.message("Click on this window and ", top=10+(self.font_size+5)*2)
		self.message(" - press [End] to change dataset", top=10+(self.font_size+5)*3)
		self.message(" - press [Home] to show/hide the window frame", top=10+(self.font_size+5)*4 )
		self.message(" - press [Esc] to exit", top=10+(self.font_size+5)*5)
		
		
	

	def show_img(self, im, rgb=False, scale=1, left=0, top=0, u_size=None, alpha=True):
		size = (len(im[1]), len(im))
		if rgb:
			# RGB printing
			im = Image.frombuffer('RGB', size, im.tobytes(), 'raw', 'BGRX', 0, 1)
		else:
			# Greyscale printing
			im = Image.frombuffer("L", size, im.tobytes(), "raw", "L", 0, 1)
		if not alpha:
			im = Image.frombuffer("RGB", size, im.tobytes(), "raw", "RGB", 0, 1)
			print("ffs")
		tmp = io.BytesIO()
		if u_size is None:
			im = im.resize((size[0]*scale, size[1]*scale))
		else:
			im = im.resize(u_size)
		im.save(tmp, "bmp")
		tmp.seek(0)
		self.screen.blit(self.pygame.image.load(tmp),(left, top))

	def get_fps(self):
		return self.clock.get_fps()
		


