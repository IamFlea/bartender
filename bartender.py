# -*- coding: utf-8 -*-
from screenshooter import ScreenShooter
from pygame_window import PyGameWindow
from screen_parser import *
from technologies import Technologies
from research_queue import ResearchQueue
from operator import sub


###
# User defined fancy stuff 
WINDOW_SIZE = (360, 160) # Width and height (or vice versa)
BACKGROUND_COLOUR = (244, 214, 172) # RGB 
FONT_SIZE = 12
FONT_COLOUR = (0x00, 0x00, 0x00) # RGB

MAX_FPS = 40

###

# Creates the window
window = PyGameWindow(WINDOW_SIZE, MAX_FPS)

# Set our fancy stuff
window.background = BACKGROUND_COLOUR 
window.font_size = FONT_SIZE
window.font_colour = FONT_COLOUR

# Init the stuff here.
window.on_top()
screen = ScreenShooter()

# Filter functions for gathered resources (10, -50, 10)
positive_sum = lambda x: sum(filter(lambda x: x > 0, x)) # Sum of positive values
negative_sum = lambda x: -sum(filter(lambda x: x < 0, x)) # Sum of negative

time = None
civ = None
# Lets not end this program now
while window.update():
	# Get screen shot
	try:
		img = screen.shot()
	except win32ui.error:
		window.error("Couldn't take screenshot!")
		window.update()
		window.pygame.time.wait(500)
		exit(42)
	# Save old time
	prev_time = time
	# Get new time
	time = get_time(img)
	# Check if we parsed time.
	if prev_time is None and time is None: 
		window.error("Can't parse time. Press F11 in game!")
		continue
	# Initate values. 
	if prev_time is None and (civ is None or time < 60): # We haven't already parsed civ
		# Get Civ
		try:
			civ = get_civ(img)
		except KeyError:
			time = None # The civ is crucial 
			window.error("Can't parse civ.")
			continue
		# Get technologies with bonuses
		techs = Technologies(civ, window.dataset)
		window.techs = techs 
		# Get the empty queue for the technology trees.
		queue = ResearchQueue(techs)
		# Parse resources
		prev_resources = get_resources(img)
		if None in prev_resources: # The resources are crucial
			time = None
			window.error("Can't parse resources")
			continue
		# Saved values of resources from the previous minute
		saved_values = [[(0,0,0,0)] for _ in range(60)]
		continue
	if prev_time is None: # We have initiated values
		continue
	# Gather Resources info and then calculate the difference between the actual resources and previous resources
	resources = get_resources(img)
	# Get Research
	queue.add(* get_research(img, civ))
	try:
		difference = tuple(map(sub, resources, prev_resources))
	except TypeError: 
		# Tuple `resources` contains None 
		# The error happens, if resources are hidden behind the window
		window.error("Can't parse resources")
		continue
	if any(difference):
		saved_values[time % 60] += [difference] 
		prev_resources = resources

	if (time - 1) > prev_time: # Time ticked more than once ((more than one second passed))
		for time_value in range(prev_time, (time - 2)): # Skiping 'time - 1'
			saved_values[time % 60] = [(0,0,0,0)]
	# Gather Research information. 
	if (time - 1) == prev_time:  # Time just ticked in game ((a second has passed))
		# Did ingame time changed?
		# Update the time in queue
		queue.update(time)
		# Calculate the resource per minute
		# Merge collected data [[(),()], [()]]  ->  [(), (), ()]
		merged_list = [values for sublist in saved_values for values in sublist]
		# Transpose the sublists zip(*l) -> from the list l=[(a,b,c), (a,b,c)] creates sublist -> [(a,a), (b,b), (c,c)]
		# Filter the resources in each sublist.
		gathered_resources = map(positive_sum, zip(*merged_list))
		spent_resources = map(negative_sum, zip(*merged_list))
		# Clear the sublist
		saved_values[time % 60] = [(0,0,0,0)]
		window.display_resources(gathered_resources, spent_resources, time)
		window.display_researches(queue)
		#print(fps)
# End while 
print("GG")