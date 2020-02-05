import numpy as np 

board = np.zeros((6,7), dtype=int)

for i in range(6):
	board[i][3] = 1
for i in range(7):
	if i % 2 == 0:
		board[3][i] = 2
board[4][4] = 3 
for row in board:
	print(row)

print('vertical',board[:,3])
print('horizontal', board[3])
print('diagonal', board.diagonal())
print(np.fliplr(board).diagonal())


for row in board:
	print(row)



