import pkg_resources
from os.path import abspath,join,pardir
import sys
import subprocess

gist_folder = abspath(join(__file__,pardir,"content","gist"))
www_folder = abspath(join(__file__,pardir,"www_folder"))
sys.path.insert(1, gist_folder)

def pelican_wrapper(test_installed_package=False):
    """ add here code around pelican:
    a. check for required packages
    b. run specific actions (like own pelican extensions not available in 
        pelican repository...)
    """
    run_pelican=True
    
    if test_installed_package:

        installed_packages = pkg_resources.working_set
        installed_versionned_packages_list = sorted(["%s==%s" % (i.key, i.version)
           for i in installed_packages])
        installed_packages_list = sorted([i.key for i in installed_packages])
        print(installed_packages_list)   
        print(installed_versionned_packages_list)

        
        for needed in ["pelican","jinja2","markdown","pelican-sitemap"]:
            if needed not in installed_packages_list:
                print(f"missing {needed}")
                run_pelican=False
        
    if run_pelican:
        subprocess.run(["pelican","content","-t","theme","-o",www_folder])
    
if __name__=="__main__":
    pelican_wrapper()