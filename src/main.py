import os
import shutil
from gencontent import generate_page,generate_pages_recursive
import sys
def main():
    def copy_files(static, public):
      
        if os.listdir(public) == os.listdir(static):
            return "completed"
        shutil.rmtree(public)
        if os.path.exists(public) == False:
            os.mkdir(public)
        static_files = os.listdir(static)
        for file in static_files:
            static_path = os.path.join(static,file)
            if os.path.isfile(static_path):
                shutil.copy(static_path, public)
            elif os.path.isdir(static_path):
               public_path = os.path.join(public, file)
               os.mkdir(public_path)
               copy_files(static_path, public_path)
    copy_files("/home/temme/workspace/static-generator/content" , "/home/temme/workspace/static-generator/docs")
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    generate_pages_recursive("/home/temme/workspace/static-generator/content", "/home/temme/workspace/static-generator/template.html", "/home/temme/workspace/static-generator/docs",basepath)

main()