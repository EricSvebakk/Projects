
size = int(input())

nodes = []
for i in range(size):
	nodes.append(0)
	
	row = input().split()
	for j in range(len(row)):
		row[j] = int(row[j])
	
	
	for j in range(size):
		nodes[i] += row[j]

print(nodes)

nodes.sort()

weak = []
for i in range(len(nodes)):
	if (nodes[i] < 3):
		weak.append(nodes(i))
		
print()

# def findNeighbours(xC: int, yC: int, grid: list) -> list:

# 	neighbours = 0

# 	# iterates over the cells "above" and
# 	# "below" of a specified cell-position
# 	for yi in range(-1, 2):
# 		yi += yC

# 		# y-positions which are too small
# 		# or too large are skipped
# 		if yi < 0 or yi > size-1:
# 			continue

# 		# iterates over the cells "left" and
# 		# "right" of a specified cell-position
# 		for xi in range(-1, 2):
# 			xi += xC

# 			# x-positions which are too small
# 			# or too large are skipped
# 			if xi < 0 or xi > size-1:
# 				continue

# 			# The cell specified for findNeighbours() is
# 			# not included among the list of neighbours
# 			if yi == yC and xi == xC:
# 				continue
			
# 			if (abs(yi-yC) == abs(xi-xC)):
# 				continue				

# 			# The remainder of positions (which are all valid positions)
# 			# are added to the list of neighbours
			
# 			neighbours += grid[yi][xi]

# 	return neighbours


# grid = []

# for i in range(size):
# 	temp = input().split(" ")
# 	row = []
	
# 	for j in range(len(temp)):
# 		row.append(int(temp[j]))
		
# 	grid.append(row)


# strength = []
# for i in range(len(grid)):
# 	row = []
	
# 	for j in range(len(grid[i])):
# 		row.append(findNeighbours(i, j, grid))
		
# 	strength.append(row)
			

# print(strength)

# for i in range(len(strength)):
	
# 	for j in range(len(strength[i])):
		
# 		print(f"{strength[i][j]} ",end="")
# 	print()



# weakest = []
# for i in range(len(strength)):
# 	for j in range(len(strength[i])):
# 		if (strength[i][j] < 2):
# 			weakest.append(strength[i][j])

# weakest.sort()

# print(weakest)