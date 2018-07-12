from random import randint

def test():
	total = 5
	processed = 0
	for i in range(total):
		yield randint(100,200), processed/total
		processed += 1

for a, b in test():
	print(a, b)