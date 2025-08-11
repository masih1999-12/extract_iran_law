# links = None

# with open('links.txt', 'r') as f:
#     links1 = set(f.readlines())

# with open('links2.txt', 'r') as f:
#     links2 = set(f.readlines())
    
# links3 = links1.union(links2)

# with open('links3.txt', 'w') as f:
#     f.writelines(links3)

links = None

with open('links3.txt', 'r') as f:
    links3 = set(f.readlines())

with open('links4.txt', 'r') as f:
    links4 = set(f.readlines())
    
links5 = links3.union(links4)

with open('links5.txt', 'w') as f:
    f.writelines(links5)
