# 智能工作总结助手

智能工作总结助手是一款基于AI的工作周报生成工具，能够帮助用户快速、高效地生成工作周报。

## 功能特点

- 基于用户输入的工作内容要点，自动生成结构化的周报
- 支持自定义周报格式和内容
- 快速高效，减少手动撰写周报的时间

## 安装与运行

### 环境要求

- Python 3.8+

### 安装

```bash
# 克隆仓库
git clone https://github.com/yourusername/ai-work-summary-assistant.git
cd ai-work-summary-assistant

# 安装依赖
pip install -e .
```

### 运行

```bash
# 启动API服务
python run.py
```

服务启动后，可以访问 http://localhost:8000/docs 查看API文档。

## API接口

### 生成周报

**接口**: POST /api/v1/text-generation/generate_report

**请求体**:
```json
{
  "content": "周一：参加项目启动会议，讨论了新功能需求；周二：完成了登录模块的API设计；周三：实现了用户认证功能；周四：修复了3个bug；周五：完成代码审核并部署测试环境。"
}
```

**响应**:
```json
{
  "generated_text": "# 本周工作内容和成果\n\n1. 参加项目启动会议，讨论新功能需求\n2. 完成登录模块API设计\n3. 实现用户认证功能\n4. 修复3个bug\n5. 完成代码审核并部署测试环境\n\n# 下周工作计划\n\n1. 继续实现剩余API功能\n2. 进行单元测试编写\n3. 准备集成测试\n\n# 工作心得\n\n本周项目进展顺利，团队配合良好，需要继续保持高效的工作节奏。"
}
```
```

## 4. 确保目录结构

别忘了创建以下目录和文件（空文件）以确保项目结构完整：


