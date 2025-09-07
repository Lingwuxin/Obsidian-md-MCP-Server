# Obsidian Markdown MCP Server

一个用于管理SCP基金会文档的MCP (Model Context Protocol) 服务器，提供文档读取、链接管理和双向链接生成功能。

## 🚀 功能特性

### � SCP文档管理
- **文档读取**: 根据SCP编号读取完整文档内容
- **分行读取**: 支持按行号范围读取文档片段
- **智能目录**: 自动根据SCP编号分配到对应子目录
- **链接提取**: 识别现有的Obsidian和Markdown格式链接

### 🛠️ 提供的工具

#### 1. `get_scp_document`
根据SCP编号获取对应的文档内容。

**参数:**
- `scp_id` (str): SCP编号，如scp-001、scp-5001

**返回值:**
- 完整的文档内容字符串

#### 2. `get_scp_document_lines`
根据SCP编号获取对应文档内容的指定行范围。

**参数:**
- `scp_id` (str): SCP编号，如scp-001、scp-5001
- `start` (int): 起始行号
- `end` (int): 结束行号

**返回值:**
- 指定行范围的文档内容

#### 3. `put_links`
保存文档中找到的潜在链接目标列表。

**参数:**
- `scp_id` (str): SCP编号，如scp-001、scp-5001
- `links` (List[str]): 文档中找到的潜在链接目标列表

**返回值:**
- 布尔值，表示是否成功保存链接数据

#### 4. `extract_existing_links`
提取文档中已存在的链接。

**参数:**
- `text` (str): Markdown文档的文本内容

**返回值:**
- 现有链接列表

## 📥 安装和运行

### 环境要求
- Python 3.11+
- MCP 1.13.1+
- uv (推荐的Python包管理工具)

### 安装依赖
```bash
# 使用 uv 安装依赖
uv install
```

### 环境配置
在项目根目录创建 `.env` 文件：
```env
SCP_MD_LINKING_OUTPUT_DIR=./SCP-Linking
SCP_MD_UNLINK_OUTPUT_DIR=./SCP-Unlink
TRANSPORT=sse
PORT=8088
```

### 运行服务器
```bash
# 使用 uv 运行
uv run main.py
```

## 🎯 使用示例

### 基本用法
```python
# 获取SCP文档
document = get_scp_document("scp-173")

# 获取文档的指定行
lines = get_scp_document_lines("scp-173", 10, 20)

# 保存链接数据
success = put_links("scp-173", ["SCP-096", "基金会", "收容"])

# 提取现有链接
existing_links = extract_existing_links(document)
```

### 目录结构说明
- `SCP-Unlink/`: 存储原始SCP文档的目录
- `SCP-Linking/`: 存储链接分析结果的目录

文档按编号范围自动分组：
- `001-1000/`: SCP-001 到 SCP-1000
- `1001-2000/`: SCP-1001 到 SCP-2000
- 以此类推...

## 🔧 技术架构

### 核心组件
- **FastMCP Server**: 基于MCP协议的服务器框架
- **File Management**: 智能文件路径管理和目录分组
- **Link Processing**: 链接提取和数据持久化

### 传输协议支持
- **stdio**: 标准输入输出
- **sse**: Server-Sent Events (默认)
- **streamable-http**: HTTP流式传输

### 目录分组算法
自动根据SCP编号计算对应的子目录：
```python
# 示例：scp-1234 -> "1001-2000" 目录
# 示例：scp-173 -> "001-1000" 目录
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目。


### 项目结构
```
Obsidian-md-MCP-Server/
├── main.py                    # 程序入口
├── pyproject.toml             # 项目配置
├── src/obsidian_md_mcp/       
│   ├── server.py              # MCP服务器实现
│   └── filepath_tool.py       # 文件路径工具
└── test/                      # 测试文件
```

## 🔗 相关项目

- [SCP-Obsidian](https://github.com/Lingwuxin/SCP-Obsidian) - 主项目
- [SCP-Obsidian-Markdown](https://github.com/Lingwuxin/SCP-Obsidian-Markdown) - 应用项目  
- [MCP](https://modelcontextprotocol.io/) - Model Context Protocol