import os.path
import shutil

class FileBasedTable:
    def create_backup(self, orig_path):
        src_base_name = os.path.basename(orig_path)
        dest_base_name = "{}.bak{}".format(*os.path.splitext(src_base_name))
        dest_path = orig_path.replace(src_base_name, dest_base_name)
        shutil.copyfile(orig_path, dest_path)