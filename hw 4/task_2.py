import hashlib

def hash(tohash):
	return hashlib.sha256((tohash).encode()).hexdigest()[:12]

def find_collision():
	initial_string = "text"
	name = "igor"

	hash1 = hash(initial_string + name)
	hash2 = hash(hash(initial_string + name) + name)

	print("Let's find the loop")
	while hash1 != hash2:
		hash1 = hash(hash1 + name)
		hash2 = hash(hash(hash2 + name) + name)

	print(hash1)

	print("Let's find the collision")

	m1 = initial_string + name
	m2 = hash1 + name
	hash1 = hash(m1)
	hash2 = hash(m2)

	while hash1 != hash2:
		m1 = hash1 + name
		m2 = hash2 + name
		hash1 = hash(m1)
		hash2 = hash(m2)

	print("m1: ", m1)
	print("m2: ", m2)
	print("hash1: ", hash1)
	print("hash2: ", hash2)


if __name__ == '__main__':
	find_collision()