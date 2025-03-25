import os
from typing import List, Dict

def get_file_extension(filename: str) -> str:
    """获取文件扩展名"""
    return os.path.splitext(filename)[1].lstrip(".")
    
def is_code_file(filename: str) -> bool:
    """判断是否为代码文件"""
    code_extensions = {
        "py", "js", "ts", "java", "cpp", "c", "go", "rs",
        "php", "rb", "cs", "scala", "kt", "swift"
    }
    return get_file_extension(filename) in code_extensions

def truncate_text(text: str, max_length: int = 1000) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."