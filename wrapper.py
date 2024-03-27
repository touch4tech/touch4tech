import argparse
from dotenv import load_dotenv
import pkg_resources
from os.path import abspath, isdir, join,pardir
from os import mkdir, walk
from os import getenv
import pathlib
from shutil import copytree, rmtree
import sys
import subprocess
import yaml

from Notion2Pelican.Notion2Pelican import readDatabase, page_tree_ids
from Notion2Pelican.Notion2Pelican import get_notion_headers, pageid_2_md


gist_folder = abspath(join(__file__,pardir,"content","gist"))
www_folder = abspath(join(__file__,pardir,"www_folder"))
dp_theme = abspath(join(__file__,pardir,"static"))
dp_tmp = abspath(join(__file__,pardir,"tmp"))
# pathlib.Path(dp_tmp).mkdir(parents=True, exist_ok=True) 

sys.path.insert(1, gist_folder)

def check_venv(test_requirements=True):
    if test_requirements:

        installed_packages = pkg_resources.working_set
        installed_versionned_packages_list = sorted(["%s==%s" % (i.key, i.version)
           for i in installed_packages])
        installed_packages_list = sorted([i.key for i in installed_packages])
        # print(installed_packages_list)   
        # print(installed_versionned_packages_list)

        
        for needed in ["pelican","jinja2","markdown","pelican-sitemap"]:
            if needed not in installed_packages_list:
                print(f"missing {needed}")
                run_pelican=False
def list_drafts(dp_content,theme,dp_www):
    from urllib.parse import quote
    drafts = {"articles":[]}
    for root, folders, files in walk(dp_content):
        for f in files:
            if f.find(".md") >=0:
                try:
                    fp = abspath(join(root, f))
                    with open(fp, encoding="utf-8") as fi:
                        fc = fi.read()
                    yaml_header = fc.split("---")[1]
                    yaml_header = yaml.safe_load(yaml_header)
                except Exception as ex:
                    log_msg = f"{str(ex)} for fp: {fp}"
                    print(log_msg)
                    raise
                if "status" in yaml_header:
                    if yaml_header["status"]=="draft":
                        url = "drafts/" + quote(yaml_header["title"].replace(" ","-")) + ".html"
                        drafts["articles"].append({"title": yaml_header["title"],
                                                    "date": yaml_header["date"],
                                                    "url": url}
                                                  )
    dp_j2templates = abspath(join(dp_theme, theme, "templates")) #, 'draft_index.j2'))
    print(53,"**********", dp_j2templates)
    # conf = {"articles":[{"title":"test1","date":"2023-01-01","title":"test title"}]}
    from jinja2 import Environment, FileSystemLoader, Template
    env = Environment(loader=FileSystemLoader(dp_j2templates))
    template = env.get_template("draft_index.j2")
    full_html = template.render(drafts)
    fp = abspath(join(dp_www,"draft_index.html"))
    print(50,fp)
    with open(fp, 'w') as fo:
        fo.write(full_html)

def pull_notion():
    load_dotenv()
    MY_NOTION_SECRET = getenv("NOTIONKEY")
    FT_dbid = getenv("FT_dbid")
    headers = get_notion_headers(MY_NOTION_SECRET)
    # notion_db_id = MY_NOTION_DB_ID
    res = readDatabase(databaseId=FT_dbid, notion_header=headers)
    site_tree = page_tree_ids(res, headers)
    draft_folder = ""
    content_folder = dp_tmp
    page_folder = ""
    for page in site_tree:
        print(103, page["title"])
        if page["title"]=="Published":
            dpo = content_folder
            status= "published"
        elif page["title"]=="Draft":
            dpo = abspath(join(content_folder, "_drafts"))
            status = "draft"
        else:
            print("WARNING folder unknow:", page["title"])
            continue
        if page["children"]:
            folder = page["title"]
            for child in page["children"]:
                child_id = child["id"]
                child_title = child["title"]
                print(111, child_title)

                res_t = readDatabase(databaseId=child_id,
                                     notion_header=headers,
                                     print_res=False)
                front_matter = {"title": child_title,
                                "page_id": child_id,
                                "status": status
                                }
                md = pageid_2_md(front_matter, res_t)
                fp = abspath(join(dpo, f"{child_id}.md"))
                # fn = replace_invalid_characters(f"{folder}_{child_id}.md")
                print("writting fp", fp)
                with open(fp, 'w', encoding="utf-8") as fo:
                    fo.write(md)

def pre_pelican(dp_content,theme,dp_www,
                rebuild_tmp=True,
                rebuild_notion=False):
    """ pelican wrapper, to be included here :
    1. check python dependancies
    2. generate index page for all draft pages
    2. TBD
    """
    check_venv()
    if not isdir(dp_www):
        mkdir(dp_www)
    list_drafts(dp_content,theme,dp_www)

    # 1. clean the tmp folder
    if rebuild_tmp:
        if pathlib.Path(dp_tmp).exists():
            rmtree(dp_tmp)
    # 1. copy the content folder into the tmp folder
    
    dp_src = abspath(join(__file__,pardir,"content"))
    if rebuild_tmp:
        copytree(dp_src, dp_tmp)

    # 2. add the notion pages
    if rebuild_notion:
        pull_notion()
    else:
        print("NOTION **NOT** updated")


    return dp_tmp
    
def post_pelican(dp_content,theme,dp_www, pelican_results, delete_tmp=False):
    """ pelican wrapper, to be included here :
    1. hidden page which has logs of last generated static site
    2. TBD
    """
    print("post pelican **************")
    print(pelican_results.stdout)
    print(pelican_results.stderr)
    if delete_tmp:
        if pathlib.Path(dp_tmp).exists():
            rmtree(dp_tmp)

def pelican_wrapper(dp_content, theme, dp_www, test_requirements=False):
    """ add here code around pelican:
    a. check for required packages
    b. run specific actions (like own pelican extensions not available in 
        pelican repository...)
    """
    run_pelican=True
    
    if test_requirements:

        installed_packages = pkg_resources.working_set
        installed_versionned_packages_list = sorted(["%s==%s" % (i.key, i.version)
           for i in installed_packages])
        installed_packages_list = sorted([i.key for i in installed_packages])
        # print(installed_packages_list)   
        # print(installed_versionned_packages_list)

        
        for needed in ["pelican","jinja2","markdown","pelican-sitemap"]:
            if needed not in installed_packages_list:
                print(f"missing {needed}")
                run_pelican=False
        
    if run_pelican:
        result = subprocess.run(["pelican",dp_content,"-t","static/theme","-o",www_folder], capture_output=True, text=True)
    return result
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--staging",
                        help="build staging and deploy it",
                        action="store_true")    
    parser.add_argument("-l", "--local",
                        help="build site locally",
                        action="store_true")
    parser.add_argument("-n", "--notion",
                        help="update notion local cache",
                        action="store_true")
    args = parser.parse_args()
    print(args)
    if args.local or args.staging:
        pass
    else:
        print("SELECT AN OPTION !!!")
    if args.local:
        print("BUILD DEV LOCALLY")
        dp_content = "content"
        dp_www = www_folder
        theme = "theme"

    dp_content_tmp = pre_pelican(dp_content, theme, dp_www, rebuild_notion=args.notion)
    pelican_results = pelican_wrapper(dp_content_tmp, theme, dp_www, test_requirements=True)
    post_pelican(dp_content, theme, dp_www, pelican_results)