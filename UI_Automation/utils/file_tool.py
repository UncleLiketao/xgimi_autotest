import os

from utils.Logger import logger


def write_data(f, method='w+', data=""):
    """写入文件（文件存在记录异常）"""
    if not os.path.isfile(f):
        logger.warning('文件不存在，写入数据失败')
    else:
        with open(f, method, encoding="utf-8") as fs:
            fs.write(data + "\n")


def mkdir_file(f):
    """创建文件"""
    if not os.path.isfile(f):
        os.mknod(f)
        logger.info(f"创建文件{f}成功")
    else:
        logger.warning(f"{f}文件已经存在，创建失败")


def mkdir_directory(f):
    """创建文件夹"""
    if not os.path.isfile(f):
        os.mkdir(f)
        logger.info(f"创建文件夹{f}成功")
    else:
        logger.warning(f"{f}文件夹已经存在，创建失败")


def remove_file(f):
    """删除文件"""
    if os.path.isfile(f):
        os.remove(f)
    else:
        logger.warning(f"{f}文件不存在，无法删除")
