'''
获取统一的绝对路径
'''

import os

def get_project_root()->str:
    '''
    获取项目所在根目录
    :return: 字符串根目录
    '''
    current_file = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file)
    root_path = os.path.dirname(current_dir)
    return root_path

def get_abs_path(path:str)->str:
    '''
    传递相对路径，返回绝对路径
    :param path:
    :return:
    '''

    project_root = get_project_root()
    return os.path.join(project_root, path)

if __name__ == '__main__':
    print(get_abs_path('config/config.txt'))
