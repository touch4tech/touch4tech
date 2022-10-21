import subprocess
from notion2md import readDatabase, process_page_results
from notion2md import get_notion_headers, pageid_2_md

gist = "28939ddb1fd4ea4721475cf2edf474e8"
gist_url = f"https://gist.github.com/{gist}.git"
output = subprocess.call(["git", "clone", gist_url])
if not output==0:
  print(f"gist error code: {output}")
output = subprocess.call(["mv",f"{gist}/notion2md.py","./notion2md.py"])
if not output==0:
  print(f"mv error code: {output}")

# notion db id for frenchtouch.dev is:
FT_dbid = 'af9dd2942ef74d7c9faf32e694055a7e'
# get the GitHub secret which has the Notion Key
my_secret = environ.get("NOTIONKEY")
headers = get_notion_headers(my_secret)
print("headers",headers)
res = readDatabase(databaseId=FT_dbid, notion_headers=headers)
res2 = process_page_results(res, headers)

res_t = readDatabase(databaseId=res2["page_children_ids"][1], notion_headers=headers)
md = pageid_2_md(res_t, headers)
print(md)
with open("test.md",'w') as fo:
  fo.write(md)
