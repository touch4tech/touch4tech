import pkg_resources
from os.path import abspath, isdir, join,pardir
from os import mkdir, walk
import sys
import subprocess
import yaml


gist_folder = abspath(join(__file__,pardir,"content","gist"))
www_folder = abspath(join(__file__,pardir,"www_folder"))
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
                fp = abspath(join(root, f))
                with open(fp, encoding="utf-8") as fi:
                    fc = fi.read()
                yaml_header = fc.split("---")[1]
                yaml_header = yaml.safe_load(yaml_header)
                if "status" in yaml_header:
                    if yaml_header["status"]=="draft":
                        url = "drafts/" + quote(yaml_header["title"].replace(" ","-")) + ".html"
                        drafts["articles"].append({"title": yaml_header["title"],
                                                    "date": yaml_header["date"],
                                                    "url": url}
                                                  )
    dp_j2templates = abspath(join(theme, "templates")) #, 'draft_index.j2'))
    # conf = {"articles":[{"title":"test1","date":"2023-01-01","title":"test title"}]}
    from jinja2 import Environment, FileSystemLoader, Template
    env = Environment(loader=FileSystemLoader(dp_j2templates))
    template = env.get_template("draft_index.j2")
    full_html = template.render(drafts)
    fp = abspath(join(dp_www,"draft_index.html"))
    print(50,fp)
    with open(fp, 'w') as fo:
        fo.write(full_html)

def pre_pelican(dp_content,theme,dp_www):
    """ pelican wrapper, to be included here :
    1. check python dependancies
    2. generate index page for all draft pages
    2. TBD
    """
    check_venv()
    if not isdir(dp_www):
        mkdir(dp_www)
    list_drafts(dp_content,theme,dp_www)
    
def post_pelican(dp_content,theme,dp_www, pelican_results):
    """ pelican wrapper, to be included here :
    1. hidden page which has logs of last generated static site
    2. TBD
    """
    print("post pelican **************")
    print(pelican_results.stdout)
    print(pelican_results.stderr)

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
        result = subprocess.run(["pelican","content","-t","theme","-o",www_folder], capture_output=True, text=True)
    return result
    
if __name__=="__main__":
    dp_content = "content"
    dp_www = www_folder
    theme = "theme"
    pre_pelican(dp_content, theme, dp_www)
    pelican_results = pelican_wrapper(dp_content, theme, dp_www, test_requirements=True)
    post_pelican(dp_content, theme, dp_www, pelican_results)