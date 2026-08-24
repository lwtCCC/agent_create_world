'''
提示词
'''

from 智能体项目.utils.config_handler import prompts_config
from 智能体项目.utils.logger_handler import logger
from 智能体项目.utils.path_tools import get_abs_path


def load_system_prompts():
    try:
        system_prompt_path = get_abs_path(prompts_config['main_prompt_path'])
    except KeyError as e:
        logger.error(f'[读取系统提示词]在配置文件中没有main_prompt_path配置项')
        raise e

    try:
        return open(system_prompt_path,'r',encoding='utf-8').read()
    except FileNotFoundError as e:
        logger.error(f'[读取系统提示词]解析系统提示词出错，错误：{str(e)}')
        raise e

def load_rag_prompts():
    try:
        rag_prompt_path = get_abs_path(prompts_config['rag_summarize_prompt_path'])
    except KeyError as e:
        logger.error(f'[读取系统提示词]在配置文件中没有rag_summarize_prompt_path配置项')
        raise e

    try:
        return open(rag_prompt_path,'r',encoding='utf-8').read()
    except FileNotFoundError as e:
        logger.error(f'[读取系统提示词]解析RAG提示词出错，错误：{str(e)}')
        raise e

def load_report_prompts():
    try:
        report_prompt_path = get_abs_path(prompts_config['report_prompt_path'])
    except KeyError as e:
        logger.error(f'[读取系统提示词]在配置文件中没有report_prompt_path配置项')
        raise e

    try:
        return open(report_prompt_path,'r',encoding='utf-8').read()
    except FileNotFoundError as e:
        logger.error(f'[读取系统提示词]解析报告提示词出错，错误：{str(e)}')
        raise e

if __name__ == '__main__':
    print(load_system_prompts())
    print(load_rag_prompts())