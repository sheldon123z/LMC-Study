# Large-Model-Control-For-Power-System

# 电力系统决策控制项目

## 项目简介

本项目旨在利用**大语言模型**（Large Language Models, LLMs）实现电力系统的**决策控制**。通过集成 **PowerZoo** 模块，我们实现了电力系统的稳态控制，提升了系统的稳定性和效率。

## 主要功能

- **大语言模型驱动的决策支持**：利用先进的自然语言处理技术，辅助电力系统的实时决策。
- **稳态控制**：集成 **PowerZoo** 模块，实现电力系统的稳态控制，确保系统的稳定运行。
- **可视化工具**：提供直观的图形界面，展示电力系统的运行状态和决策过程。
- **模块化设计**：采用子模块管理，便于扩展和维护各个功能组件。

## 技术栈

- **编程语言**：Python
- **子模块**：[PowerZoo](https://github.com/XJTU-RL/PowerZoo)（已作为子模块集成）
- **依赖库**：
  - `numpy`
  - `pandas`
  - `matplotlib`
  - `torch`（用于大语言模型）
  - 其他相关库

## 安装指南

### 前提条件

- Git
- Python 3.7 及以上版本
- `pip` 包管理器

### 克隆仓库

使用 Git 克隆本仓库并初始化子模块：

```bash
git clone --recurse-submodules https://github.com/sheldon123z/Large-Model-Control.git
cd your-repository
```

如果你已经克隆了仓库但未初始化子模块，可以运行：

```bash
git submodule update --init --recursive
```

### 创建虚拟环境（可选）

建议使用虚拟环境管理项目依赖：

```bash
python -m venv venv
source venv/bin/activate  # 对于 Windows 用户使用 `venv\Scripts\activate`
```

### 安装依赖

使用 `pip` 安装项目所需的依赖：

```bash
pip install -r requirements.txt
```

**注意**：确保 `requirements.txt` 文件中列出了所有必要的依赖。如果没有，可以手动创建并添加依赖项。

### 配置环境变量

如果项目需要特定的环境变量，请在 `.env` 文件或其他配置文件中进行设置。

## 使用指南

### 运行主程序

在项目根目录下运行主程序：

```bash
python main.py
```

### 使用 PowerZoo 模块

**PowerZoo** 已作为子模块集成在 `libs/PowerZoo` 目录下。你可以直接在项目中引用和使用该模块的功能。

示例代码：

```python

```

## 贡献指南

欢迎任何形式的贡献！请按照以下步骤进行：

1. Fork 本仓库。
2. 创建新分支：`git checkout -b feature/新功能名称`。
3. 提交更改：`git commit -m "添加新功能"`。
4. 推送分支：`git push origin feature/新功能名称`。
5. 提交 Pull Request。

请确保所有提交都通过了测试，并且遵循项目的编码规范。

## 许可证

本项目采用 [MIT 许可证](LICENSE) 进行许可。详情请参阅 [LICENSE](LICENSE) 文件。

## 联系方式

如有任何问题或建议，请通过以下方式联系：

- **邮箱**：zxd_xjtu@stu.xjtu.edu.cn
- **GitHub**：[sheldon123z](https://github.com/sheldon123z)

## 致谢

感谢 [PowerZoo](https://github.com/XJTU-RL/PowerZoo) 项目团队提供的强大支持，帮助我们实现电力系统的稳态控制功能。

---

**注意事项**：

1. **更新链接和联系方式**：请将示例中的 `https://github.com/your-username/your-repository.git`、`your-email@example.com` 和 `your-username` 替换为你实际的仓库链接和联系方式。
2. **添加详细内容**：根据项目的实际情况，补充或修改各个部分的内容，例如详细的安装步骤、使用示例、更多的功能描述等。
3. **保持一致性**：确保项目结构、代码文件和 README 中的描述保持一致。
