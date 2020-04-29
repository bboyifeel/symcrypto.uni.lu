import hashlib

filename 	= "task_3.py"
name 		= "igor"

def hash(tohash):
	return hashlib.sha256((tohash).encode()).hexdigest()[:4]

def meaningful_second_preimage(d):
	hash_txt = "Given hash function is an unsecure hash function build upon sha256"
	while hash(hash_txt) != d:
		hash_txt += ' '
	print("d", d)
	print("hash(hash_txt) ", hash(hash_txt))
	print("[begin] new text")
	print(hash_txt)
	print("[end] new text")

	file = open(filename, "r")
	src = file.read()
	file.close()

	hashname = hash(name)
	while hash(src) != hashname:
		src += ' '

	print("hash(name) ", hashname)
	print("hash(src)" , hash(src))
	print("[begin] updated src")
	print(src)
	print("[end] updated src")


if __name__ == '__main__':
	d = hash("text")
	meaningful_second_preimage(d)