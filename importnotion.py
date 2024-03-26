import subprocess
import shutil
# from os import environ
from os import name as os_name
from os import getenv
from os.path import abspath, exists, join, pardir
from dotenv import load_dotenv

import pathlib

def get_gist():
    gist = "28939ddb1fd4ea4721475cf2edf474e8"
    gist_url = f"https://gist.github.com/{gist}.git"
    output = subprocess.call(["git", "clone", gist_url])
    if not output==0:
      print(f"gist error code: {output}")
    print(17, os_name)
    if os_name == "nt":
        fpi = abspath(join(__file__, pardir, gist, "notion2md.py"))
        fpo = abspath(join(__file__, pardir, "notion2md.py"))
        print(fpi)
        print(fpo)
        
        output = shutil.move(fpi, fpo)
    else:
        output = subprocess.call(["mv",f"{gist}/notion2md.py","./notion2md.py"])
    if not output==0:
      print(f"mv error code: {output}")

def __old__():
    # notion db id for frenchtouch.dev is:
    # FT_dbid = 'af9dd2942ef74d7c9faf32e694055a7e'
    FT_dbid = os.getenv("FT_dbid")
    # get the GitHub secret which has the Notion Key
    my_secret = os.getenv("NOTIONKEY")
    headers = get_notion_headers(my_secret)
    print("headers",headers)
    res = readDatabase(databaseId=FT_dbid, notion_headers=headers)
    res2 = process_page_results(res, headers)

    res_t = readDatabase(databaseId=res2["page_children_ids"][1], notion_headers=headers)
    md = pageid_2_md(res_t, headers)
    print(md)
    with open("test.md",'w') as fo:
      fo.write(md)

def new(notion_db_id, notion_secret):
    headers = get_notion_headers(notion_secret)
    # notion_db_id = MY_NOTION_DB_ID
    res = readDatabase(databaseId=notion_db_id, notion_header=headers)
    site_tree = page_tree_ids(res, headers)
    for page in site_tree:
        if page["children"]:
            folder = page["title"]
            for child in page["children"]:
                child_id = child["id"]
                child_title = child["title"]

                res_t = readDatabase(databaseId=child_id,
                                     notion_header=headers,
                                     print_res=False)
                front_matter = {"title": child_title,
                                "page_id": child_id
                                }
                md = pageid_2_md(front_matter, res_t)
                fp = abspath(join(__file__, pardir, "www_folder",
                                  "notion", folder, f"{child_id}.md"))
                # fn = replace_invalid_characters(f"{folder}_{child_id}.md")
                print("writting fp", fp)
                with open(fp, 'w') as fo:
                    fo.write(md)

if __name__ == "__main__":
    load_dotenv()
    notion2mdpy = abspath(join(__file__, pardir, "notion2md.py"))
    if not exists(notion2mdpy):
        get_gist()

    dpo_cached = abspath(join(__file__, pardir, "www_folder",
                             "notion", "Cached"))
    path = pathlib.Path(dpo_cached)
    path.mkdir(parents=True, exist_ok=True)
    dpo_draft = abspath(join(__file__, pardir, "www_folder",
                             "notion", "Draft"))
    path = pathlib.Path(dpo_draft)
    path.mkdir(parents=True, exist_ok=True)
    dpo_published = abspath(join(__file__, pardir, "www_folder",
                             "notion", "Published"))
    path = pathlib.Path(dpo_published)
    path.mkdir(parents=True, exist_ok=True)
        
    from notion2md import readDatabase, page_tree_ids, replace_invalid_characters
    from notion2md import get_notion_headers, pageid_2_md

    # from notion2md import readDatabase, process_page_results
    # from notion2md import get_notion_headers, pageid_2_md
    MY_NOTION_SECRET = getenv("NOTIONKEY")
    FT_dbid = getenv("FT_dbid")
    new(notion_db_id = FT_dbid, notion_secret = MY_NOTION_SECRET)