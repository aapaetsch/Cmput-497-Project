from itertools import combinations_with_replacement as cwr 
from itertools import permutations
def calc(arr, toplay):
	address = 0 
	for i in range(len(arr)):
		x = arr[i]
		if toplay == 1:
			address += arr[i]*4**i
		else:
			address += (1 + 2 - arr[i]) * 4 ** i
	return address

def iterations(arr, length):
	possible = []
	combs = list(cwr(arr, length))
	
	for c in combs:
		
		perms = list(permutations(c,length))
		for p in perms:
			if p not in possible:
				possible.append(p)
	return possible, len(possible)


def main():
	arr1 = [0,1,2]
	a, a1 = iterations(arr1, 4)
	b, b1 = iterations(arr1, 5)
	c, c1 = iterations(arr1, 6)
	d, d1 = iterations(arr1, 7)
	
	print('A: {}, B: {}, C: {}, D: {}, Total: {}'.format())

if __name__ == '__main__':
	main()