from os import environ
print("env var")
i = 0
for var in environ:
  i+=1
  if i>3:
    break
  print("var",var)
  for k in environ[var]:
    print("\t",k)
print("done notion2md v1")
