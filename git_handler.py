import os
from git import Repo
from typing import Optional

class GitHandler:
    def __init__(self, repo_path: str, source_branch: str, target_branch: str):
        """初始化Git处理器
        
        Args:
            repo_path: git仓库本地路径
            source_branch: 源代码分支
            target_branch: 目标代码分支
        """
        self.repo_path = repo_path
        self.source_branch = source_branch
        self.target_branch = target_branch
        self.repo = Repo(repo_path)
        
    def get_diff_info(self) -> str:
        """获取两个分支之间的代码差异信息"""
        # 确保分支存在
        if not self._branch_exists(self.source_branch) or \
           not self._branch_exists(self.target_branch):
            raise ValueError("Branch not found")
            
        # 获取差异
        diff = self.repo.git.diff(f"{self.target_branch}...{self.source_branch}")
        
        # 获取提交信息
        commits = list(self.repo.iter_commits(f"{self.target_branch}..{self.source_branch}"))
        commit_messages = "\n".join(c.message for c in commits)
        
        return f"""Diff:
{diff}

Commit Messages:
{commit_messages}
"""
    
    def _branch_exists(self, branch_name: str) -> bool:
        """检查分支是否存在"""
        try:
            self.repo.git.rev_parse("--verify", branch_name)
            return True
        except:
            return False
            
    def get_file_content(self, file_path: str, ref: str) -> Optional[str]:
        """获取指定版本的文件内容"""
        try:
            return self.repo.git.show(f"{ref}:{file_path}")
        except:
            return None