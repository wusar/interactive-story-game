import requests
import json
import sys
import time

class StoryGame:
    def __init__(self):
        self.base_url = "http://localhost:11434/api/generate"
        self.context = "你是一个奇幻故事的讲述者。游戏刚开始。"
        self.history = []

    def generate_story_segment(self, prompt):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "model": "llama3.2",
            "prompt": f"""作为一个中文交互式故事生成器，请按照以下固定格式生成内容：

故事：[故事内容]
选项1：[选项内容]
选项2：[选项内容]
选项3：[选项内容]

要求：
1. 故事内容必须是100-200字的引人入胜的情节
2. 每个选项必须是15-30字的独特选择
3. 所有内容必须使用纯中文，不要使用任何英文单词
4. 三个选项必须完全不同，引向不同的发展方向
5. 避免重复之前的情节或上一段的内容
6. 在故事中加入悬念和谜题元素
7. 确保选项之间没有相似的内容
8. 每个新的故事段落都应该是新的发展，而不是重复之前的内容

当前故事发展：{self.context}
历史：{self.history}
玩家选择：{prompt}

注意：请确保生成的内容完全符合上述格式，不要添加任何额外的内容或标记。故事和选项都必须是完整的中文句子。""",
            "stream": False
        }

        try:
            response = requests.post(self.base_url, json=data, headers=headers)
            response.raise_for_status()
            result = response.json()
            return result['response']
        except Exception as e:
            print(f"错误：无法连接到Ollama服务器。请确保Ollama正在运行。\n详细错误：{e}")
            sys.exit(1)

    def display_story_and_options(self, story_text):
        parts = story_text.split('\n')
        story = ""
        options = []
        
        # 更健壮的解析逻辑
        for part in parts:
            part = part.strip()
            if part.startswith('故事：'):
                story = part[3:].strip()
            elif part.startswith('选项') and '：' in part:
                option = part.split('：', 1)[1].strip()
                if option and option != '[生成第一个选项，15-30字]' and option != '[生成第二个选项，15-30字]' and option != '[生成第三个选项，15-30字]':
                    options.append(option)

        # 验证内容的完整性
        if not story or len(options) != 3:
            print("警告：AI返回的内容格式不正确，重新生成...")
            return None, None

        print("\n" + "="*50)
        print("\n📖 " + story + "\n")
        print("你的选择：")
        for i, option in enumerate(options, 1):
            print(f"{i}. {option}")
        print("\n" + "="*50)
        
        return story, options

    def get_user_choice(self, options):
        while True:
            try:
                choice = input("\n请选择你的行动 (输入数字1-3): ")
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num, options[choice_num-1]
                else:
                    print("请输入有效的选项数字！")
            except ValueError:
                print("请输入有效的数字！")

    def play(self):
        print("\n欢迎来到交互式故事冒险！")
        print("正在启动游戏...\n")
        time.sleep(1)

        current_prompt = "开始一个奇幻冒险故事，设定一个有趣的开场。"

        while True:
            # 生成故事段落和选项
            while True:
                story_text = self.generate_story_segment(current_prompt)
                story, options = self.display_story_and_options(story_text)
                if story is not None and options is not None:
                    break
                time.sleep(1)
            
            # 更新上下文和历史
            self.context = story
            self.history.append(story)

            # 获取用户选择
            choice_num, chosen_option = self.get_user_choice(options)
            
            # 准备下一轮的提示
            current_prompt = f"基于用户选择了：{chosen_option}，继续故事。请确保新的故事情节与选择相呼应，并带来有趣的发展。"

            print("\n正在生成故事的下一个段落...\n")
            time.sleep(1)

if __name__ == "__main__":
    print("正在初始化游戏...")
    game = StoryGame()
    try:
        game.play()
    except KeyboardInterrupt:
        print("\n\n感谢你体验这个故事冒险！再见！") 