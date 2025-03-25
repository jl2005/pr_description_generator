import yaml
import argparse
from .git_handler import GitHandler
from .openai_client import OpenAIClient

class PRDescriptionGenerator:
    def __init__(self, 
                 repo_path: str,
                 source_branch: str,
                 target_branch: str,
                 openai_base_url: str,
                 openai_api_key: str):
        """初始化PR描述生成器
        
        Args:
            repo_path: git仓库本地路径
            source_branch: 源代码分支
            target_branch: 目标代码分支
            openai_base_url: OpenAI API基础URL
            openai_api_key: OpenAI API密钥
        """
        self.git_handler = GitHandler(repo_path, source_branch, target_branch)
        self.ai_client = OpenAIClient(openai_base_url, openai_api_key)

    def generate(self) -> dict:
        """生成PR描述
        
        Returns:
            包含PR描述信息的字典,包括:
            - title: PR标题
            - type: PR类型
            - description: PR描述
            - changes: 代码变更说明
        """
        # 获取git差异信息
        diff_info = self.git_handler.get_diff_info()
        
        # 生成系统提示
        system_prompt = """你是一个代码审查助手。请根据提供的代码差异信息生成Pull Request描述。
        描述应该包含:
        1. PR标题
        2. PR类型(feature/bugfix/docs等)
        3. 变更概述
        4. 具体代码变更说明
        请以YAML格式返回结果。
        """
        
        # 生成用户提示
        user_prompt = f"""请根据以下代码差异生成PR描述:
        
        分支信息:
        - 源分支: {self.git_handler.source_branch}
        - 目标分支: {self.git_handler.target_branch}
        
        代码差异:
        {diff_info}
        """
        
        # 调用AI生成描述
        response = self.ai_client.chat_completion(
            system=system_prompt,
            user=user_prompt
        )
        
        # 解析并返回结果
        return self._parse_response(response)
        
    def _parse_response(self, response: str) -> dict:
        """解析AI响应,转换为结构化数据"""
        try:
            result = yaml.safe_load(response)
            return {
                "title": result.get("title", ""),
                "type": result.get("type", ""),
                "description": self._format_description(result.get("description", "")),
                "changes": self._format_changes(result.get("changes", ""))
            }
        except Exception as e:
            return {
                "title": "Failed to parse response",
                "type": "unknown",
                "description": response,
                "changes": ""
            }
    
    def _format_description(self, description: str) -> str:
        """格式化描述信息"""
        return description.strip()

    def _format_changes(self, changes: str) -> str:
        """格式化变更信息"""
        return changes.strip()

def main():
    parser = argparse.ArgumentParser(description="Generate a PR description using AI.")
    parser.add_argument("repo_path", type=str, help="Local path to the git repository")
    parser.add_argument("source_branch", type=str, help="Name of the source branch")
    parser.add_argument("target_branch", type=str, help="Name of the target branch")
    parser.add_argument("openai_base_url", type=str, help="Base URL for OpenAI API")
    parser.add_argument("openai_api_key", type=str, help="API key for OpenAI")

    args = parser.parse_args()

    generator = PRDescriptionGenerator(
        repo_path=args.repo_path,
        source_branch=args.source_branch,
        target_branch=args.target_branch,
        openai_base_url=args.openai_base_url,
        openai_api_key=args.openai_api_key
    )

    description = generator.generate()
    print("PR Title:", description["title"])
    print("PR Type:", description["type"])
    print("PR Description:", description["description"])
    print("PR Changes:", description["changes"])

if __name__ == "__main__":
    main() 