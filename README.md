# AI驱动的交互式故事冒险游戏

这是一个基于Ollama的交互式文字冒险游戏。游戏会使用AI实时生成故事情节和选项，让玩家通过选择来影响故事的发展方向，创造独特的游戏体验。

## 特点

- 使用Ollama本地AI模型生成故事
- 实时交互式故事生成
- 多重选择影响剧情发展
- 每次游戏都有不同的故事线
- 完全中文界面和故事内容

## 系统要求

- Python 3.6+
- Ollama（需要预先安装并运行）
- deepseek-r1 模型（需要在Ollama中预先下载）

## 安装步骤

1. 克隆仓库：
   ```bash
   git clone https://github.com/[你的用户名]/interactive-story-game.git
   cd interactive-story-game
   ```

2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

3. 确保Ollama已安装并运行：
   ```bash
   ollama run deepseek-r1
   ```

## 运行游戏

在终端中运行以下命令：
```bash
python interactive_story.py
```

## 游戏玩法

1. 游戏会生成一个故事场景和三个选项
2. 输入数字（1-3）来选择你想要的选项
3. 根据你的选择，故事会继续发展
4. 按Ctrl+C可以随时退出游戏

## 注意事项

- 确保在运行游戏之前，Ollama服务已经启动
- 游戏需要网络连接以与Ollama API通信
- 每个选择都会影响故事的发展方向
- 游戏生成的内容完全依赖于AI模型，每次体验都是独特的

## 贡献

欢迎提交Issue和Pull Request来改进游戏！

## 许可证

MIT License 