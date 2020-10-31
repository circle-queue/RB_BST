import pdb

class Node():
	def __init__(self, key, val, parent, red=True):
		self.key = key
		self.val = val
		self.right = None
		self.left = None
		self.n = 1
		self.red = red
		self.parent = parent


class BstRB():
	''' 
	Supports 
		find(key)
		put(key, val)
		delete(key)
	'''
	def __init__(self):
		self.depth = 0
		self.root = None

	def isRed(self, node):
		return False if not node or not node.red else True

	def size(self, node):
		return False if not node else node.n
		
	def rotateR(self, h):
		x = h.left
		x.parent, h.parent = h.parent, x
		if x.right: x.right.parent = h
		h.left = x.right
		x.right = h
		self.fix(x, h)
		return x

	def rotateL(self, h):
		x = h.right
		x.parent, h.parent = h.parent, x
		if x.left: x.left.parent = h
		h.right = x.left
		x.left = h
		self.fix(x, h)
		return x

	def fix(self, x, h):
		x.red = h.red
		h.red = True
		x.n = h.n
		h.n = 1 + self.size(h.left) + self.size(h.right)
		if h == self.root: self.root = x # new root
		else:
			if h == x.parent.left: x.parent.left = x
			else:				   x.parent.right = x

	def find(self, key):
		''' Returns the node with the same key, if it exist, otherwise the parent of where it should be '''
		parent = self.root
		while True: # sink down PQ tree
			if		key < parent.key and parent.left:	parent = parent.left
			elif	key > parent.key and parent.right:	parent = parent.right
			else:	return parent # if key == parent.key, or reached bottom
		
	def put(self, key, val):
		# create root
		if not self.root:
			node = Node(key, val, None, red=False)
			self.root = node
			self.depth = 1
			return

		parent = self.find(key)
		if parent.key == key:
			parent.val = val
			return # value updated. No further updates required

		# parent is now parent of the new node
		child = Node(key, val, parent)
		if key < parent.key: parent.left = child
		if key > parent.key: parent.right = child
		parent.n += 1
		
		r = self.isRed
		s = self.size
		while parent:
			if r(parent.right)	and not r(parent.left): parent = self.rotateL(parent)
			if r(parent)		and		r(parent.left): parent = self.rotateR(parent.parent)
			parent.n = 1 + s(parent.left) + s(parent.right)
			
			if r(parent.left) and r(parent.right):
				self.flipColor(parent)
				if parent == self.root:
					parent.red = False
					break
			parent = parent.parent

			
	def flipColor(self, h):
		h.red = not h.red
		h.left.red = not h.left.red
		h.right.red = not h.right.red



	def delete(self, key, h=None):
		r = self.isRed
		if h is None: h = self.root
		while h:
			if key < h.key:
				if h.left and (not r(h.left) and not r(h.left.left)):
					h = self.moveRedLeft(h)
				h = h.left
			else:
				if r(h.left):
					h = self.rotateR(h)
				if key == h.key and h.right is None:
					if h.parent.left == h: 
						if r(h.parent.right): self.rotateL(h.parent)
						h.parent.left = None
					else: h.parent.right = None
					return
				if h.right and not r(h.right) and not r(h.right.left):
					h = self.moveRedRight(h)
				if key == h.key:
					x = self.min(h.right)
					h.key = x.key
					h.val = x.val
					self.delete(x.key, h=h.right)
				else: h = h.right
		return self.balance(h)
				
				
	def moveRedRight(self, h):
		self.flipColor(h)
		if self.isRed(h.left.left):
			h = self.rotateR(h)
			self.flipColor(h)
		return h

	def moveRedLeft(self, h):
		self.flipColor(h)
		if self.isRed(h.right.left):
			h.right = self.rotateR(h.right)
			h = self.rotateL(h)
			self.flipColor(h)
		return h
	
##	  def deleteMin(self, h = None):
##		  if h is None:
##			  h = self.root
##			  if not h: return
##			  if not h.left:
##				  if h.right: self.root = h.right
##				  else: self.root = None
##				  return
##		  
##		  r = self.isRed
##		  while h.left.left:
##			  if not r(h.left) and not r(h.left.left):
##				  h = moveRedLeft(h)
##			  h = h.left
##		  h.left = None
##		  return self.balance(h)

	def balance(self, h):
		r = self.isRed
		if not h: return
		if r(h.right): h = self.rotateL(h)
		if r(h) and r(h.left): h = self.rotateR(h.parent)
		h.n = 1 + s(h.left) + s(h.right)
			
		if r(h.left) and r(h.right):
			flipColor(h)
			if h == self.root:
				h.red = False
		return h

	
	def orderTraverse(self, verbose=True):
		visited = set([None])
		order = []
		stack = [self.root]
		leftn = 0 if not self.root.left else self.root.left.n
		rightn = 0 if not self.root.right else self.root.right.n
		print(1 + leftn + rightn, self.root.n)
		while stack:
			node = stack[-1]
			#print(node.key)
			#print([n.key for n in stack])
			if node in visited:
				stack.pop()
				continue
			if (node.left in visited):
				n = stack.pop()
				if verbose: print('node {:<6}, parent {:<6}, size {:<6}, red? {:<6}'.format(node.key, str(node.parent if not node.parent else node.parent.key), node.n, node.red))
				visited.add(node)
				order.append(node.key)
			else:
				stack.append(node.left)
				continue
			stack.append(node.right)
		return order

	def floor(self, key):
		''' Returns min value if no result '''
		parent = self.root
		floor = None
		while True:
			if not	parent: break
			if		key < parent.key:	parent = parent.left
			elif	key >= parent.key:
				if floor is None or parent.key > floor.key: floor = parent
				parent = parent.right
			else:	break
		return self.min() if floor is None else floor

	def min(self, root=None):
		if root is None: root = self.root
		while root.left: root = root.left
		return root
	
	def ceil(self, key):
		''' Returns max value if no result '''
		parent = self.root
		ceil = None
		while True:
			if not	parent: break
			if		key > parent.key: parent = parent.right
			elif	key <= parent.key:
				if ceil is None or parent.key < ceil.key: ceil = parent
				parent = parent.left
			else: break
		return self.max() if ceil is None else ceil
			
	def max(self, root=None):
		parent = self.root if root is None else root
		while parent.right: parent = parent.right
		return parent

	def interval(self, minKey, maxKey): # min max out of bounds?
		s = self.size
		n = 1 # Root counted

		subRoot = self.root
		while True:
			if	 subRoot.key > maxKey and subRoot.key > minKey and subRoot.left:  subRoot = subRoot.left #subroot is the smallest root containing min and max key
			elif subRoot.key < maxKey and subRoot.key < minKey and subRoot.right: subRoot = subRoot.right
			else: break
		
		h = self.ceil(minKey)
		parent = h.parent
		if h != subRoot:
			n += 1 + s(h.right)
			while parent != subRoot: # Walkts up tree, adding subtrees when they're larger than the min value
				if h == parent.left:
					n += s(parent.right) + 1
				h = parent
				parent = h.parent
		
		h = self.floor(maxKey)
		parent = h.parent
		if h != subRoot:
			n += 1 + s(h.left)
			while parent != subRoot: # Walkts up tree, adding subtrees when they're larger than the min value
				if h == parent.right:
					n += s(parent.left) + 1
				h = parent
				parent = h.parent
		return n
			

def main():
	st = BstRB()
	
	st.put(1, 'val')
	st.put(6, 'val')
	st.delete(1)
	st.put(3, 'val')
	st.put(0, 'val')
	st.delete(3)
	print(1)
	st.put(9, 'val')
	print(2)
	st.orderTraverse()
	# from random import randint
	# things = set()
	# size = 10
	# actions = []
	# try:
		# for num in range(size):
			# num = randint(0, 10)
			# actions.append("add " + str(num))
			# st.put(num, 'val')
			# things.add(num)
			# if randint(0,10) >= 7:
				# n = randint(0,10)
				# if n not in things:
					# actions.append("add " + str(n))
					# st.put(n, 'val')
					# things.add(n)
				# actions.append("remove " + str(num))
				# st.delete(n)
				# things.remove(n)
				
	# except AttributeError:
		# print(actions)
		# exit()
	
	
	# print(st.orderTraverse(False) == sorted(things))
	# if not st.orderTraverse(False) == sorted(things):
		# print(st.orderTraverse(), sorted(things))
		# print(actions)
	

if __name__ == "__main__":
	main()
