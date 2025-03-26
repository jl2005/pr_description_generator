# PR Description Generator

一个独立的工具，用于生成Pull Request的描述信息。

## 使用方法

### 通过命令行运行

您可以通过命令行直接运行 `main` 函数来生成PR描述。以下是示例命令：

```bash
python generator.py /path/to/repo \
         source-branch target-branch \
         https://api.openai.com/v1/chat/completions \
         your-openai-api-key
```

### 参数说明

- **/path/to/repo**: 您的本地Git仓库的路径。
- **source-branch**: 您想要比较的源分支名称。
- **target-branch**: 您想要比较的目标分支名称。
- **https://api.openai.com/v1/chat/completions**: OpenAI API的基础URL。
- **your-openai-api-key**: 您的OpenAI API密钥。

### 输出

运行上述命令后，程序将输出生成的PR描述信息，包括PR标题、类型、描述和变更说明。例如：

```plaintext
PR Title: Add new feature to improve performance
PR Type: feature
PR Description: This pull request introduces a new feature that significantly improves the performance of the application by optimizing the data processing algorithm.
PR Changes: 
- Refactored the data processing module
- Improved algorithm efficiency
- Updated unit tests to cover new changes
```

## 输入参数

- **repo_path**: git仓库的本地路径
- **source_branch**: 源代码分支名称
- **target_branch**: 目标代码分支名称
- **openai_base_url**: OpenAI API的基础URL
- **openai_api_key**: OpenAI API密钥

## 依赖

在使用此工具之前，请确保安装以下Python包：

```bash
pip install -r requirements.txt
```

## 功能说明

- **自动生成PR描述**: 根据代码差异自动生成PR的标题、类型、描述和变更说明。
- **支持多种编程语言**: 通过识别文件扩展名来支持多种编程语言的代码文件。
- **与OpenAI集成**: 使用OpenAI的API来生成自然语言描述。

## 注意事项

- 确保提供的分支名称在本地仓库中存在。
- 确保OpenAI API密钥有效，并且有足够的调用配额。
- 该工具假设仓库处于干净状态，没有未提交的更改。

## 示例

以下是一个完整的示例，展示如何使用该工具生成PR描述：

```python
from pr_description_generator import PRDescriptionGenerator

# 初始化生成器
generator = PRDescriptionGenerator(
    repo_path="/path/to/your/repo",
    source_branch="feature-branch",
    target_branch="main",
    openai_base_url="https://api.openai.com/v1",
    openai_api_key="your-openai-api-key"
)

# 生成PR描述
description = generator.generate()

# 打印生成的描述
print("PR Title:", description["title"])
print("PR Type:", description["type"])
print("PR Description:", description["description"])
print("PR Changes:", description["changes"])
```

通过以上步骤，您可以轻松地在本地环境中生成PR描述，并将其应用于您的开发工作流中。
