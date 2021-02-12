f = open("useless.txt", "r")
l = [line.strip() for line in f]
s = set(l)
f.close()
f = open("useless_words.txt", "w")
for i in s:
    f.write(i + "\n")
print("ok")
f.close()
