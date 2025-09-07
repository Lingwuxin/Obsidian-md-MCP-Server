import re
import json
from typing import List, Dict, Any, Literal, Tuple, Optional, cast
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Settings
from mcp.types import Tool, TextContent
import dotenv
import os
from src.obsidian_md_mcp.filepath_tool import scp_num_generator, get_scp_subdirectory
# 加载环境变量
dotenv.load_dotenv()
SCP_MD_LINKING_OUTPUT_DIR = os.getenv(
    "SCP_MD_LINKING_OUTPUT_DIR", "./SCP-Linking")
SCP_MD_UNLINK_OUTPUT_DIR = os.getenv(
    "SCP_MD_UNLINK_OUTPUT_DIR", "./SCP-Unlink")
TRANSPORT = os.getenv("TRANSPORT", "sse")  # stdio\sse\streamable-http
PORT = int(os.getenv("PORT", 8088))
# 创建 FastMCP 服务器实例
mcp = FastMCP("Obsidian Markdown MCP Server", port=PORT)



@mcp.tool(name="extract_existing_links")
def extract_existing_links(self, text: str) -> List[str]:
    """提取文档中已存在的链接"""
    obsidian_links = re.findall(self.existing_link_pattern, text)
    markdown_links = re.findall(self.markdown_link_pattern, text)
    return obsidian_links + markdown_links

@mcp.tool(name="get_scp_document")
def get_scp_document(self, scp_id: str) -> str:
    """
    根据SCP编号获取对应的文档内容
    Args:
        scp_id: SCP编号,如scp-001,scp-5001
    Returns:
        str: 文档内容
    """
    file_path = os.path.join(SCP_MD_UNLINK_OUTPUT_DIR,get_scp_subdirectory(scp_id), f"{scp_id}.md")
    
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    else:
        return ""
# 逐行读取

@mcp.tool(name="get_scp_document_lines")
def get_scp_document_lines(self, scp_id: str, start: int, end: int) -> str:
    """
    根据SCP编号获取对应的文档内容的指定行
    Args:
        scp_id: SCP编号,如scp-001,scp-5001
        start: 起始行号
        end: 结束行号
    Returns:
        str: 指定行的文档内容
    """
    file_path = os.path.join(SCP_MD_UNLINK_OUTPUT_DIR,get_scp_subdirectory(scp_id), f"{scp_id}.md")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            return ''.join(lines[start:end])
    else:
        return ""

@mcp.tool(name="put_links")
def put_links(self, scp_id: str, links: list[str]) -> bool:
    """
    推送双向链接目标对象列表到存储
    Args:
        scp_id: SCP编号,如scp-001,scp-5001
        links: 文档中找到的需要添加双向链接的内容
    Returns:
        bool: 是否成功保存链接数据
    """
    output_path = os.path.join(
        SCP_MD_LINKING_OUTPUT_DIR, get_scp_subdirectory(scp_id), f"{scp_id}.json")
    if not os.path.exists(os.path.dirname(output_path)):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
    # 以json格式保存链接数据
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"scp_id": scp_id, "links": links},
                    f, ensure_ascii=False, indent=4)
    return True


def run():
    """运行MCP服务器"""
    def get_transport() -> Literal['stdio', 'sse', 'streamable-http']:
        # 进行类型检查
        if TRANSPORT in ['stdio', 'sse', 'streamable-http']:
            return cast(Literal['stdio', 'sse', 'streamable-http'], TRANSPORT)
        else:
            raise ValueError(f"Invalid transport: {TRANSPORT}")

    mcp.run(transport=get_transport())



if __name__ == "__main__":
    # 运行服务器
    run()
