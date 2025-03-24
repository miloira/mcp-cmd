import os
import shutil

from tools.utils import register_mcp_tools


def get_computer_username():
    """获取登录用户名"""
    return os.getlogin()


def list_directory(path):
    """列出目录下的文件"""
    return os.listdir(path)


def open_file(path):
    """打开文件"""
    os.startfile(path)
    return True


def view_file(path):
    """查看文件"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def create_file(path):
    """创建文件"""
    fd = os.open(path, os.O_CREAT | os.O_WRONLY)
    os.close(fd)
    return True


def edit_file(path, content):
    """编辑文件"""
    with open(path, "a", encoding="utf-8") as f:
        f.write(content)
    return True


def copy_file(src, dst):
    """复制文件"""
    shutil.copyfile(src, dst)
    return True


def rename_file(old_name, new_name):
    """重命名文件"""
    os.rename(old_name, new_name)
    return True


def delete_file(path):
    """删除文件"""
    os.remove(path)
    return True


def create_directory(path):
    """创建单个文件夹"""
    os.mkdir(path)
    return True


def create_directories(path, exist_ok=False):
    """创建多个文件夹"""
    os.makedirs(path, exist_ok=exist_ok)
    return True


def delete_directory(path):
    """删除文件夹"""
    shutil.rmtree(path)
    return True


register_mcp_tools([
    get_computer_username,
    list_directory,
    open_file,
    view_file,
    create_file,
    edit_file,
    copy_file,
    rename_file,
    delete_file,
    create_directory,
    create_directories,
    delete_directory
], tool_group_name="文件系统")
