from os import environ
print("env var")
i = 0
for var in environ:
  i+=1
  print(f"var {i}",var)
  for k in environ[var]:
    print("\t",k)
print("done notion2md v1")
