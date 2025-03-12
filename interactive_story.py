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
            "model": "deepseek-r1",
            "prompt": f"""你现在是一个交互式故事游戏的生成器。请严格按照以下格式生成内容：

故事：[生成一段100-200字的故事情节]
选项1：[生成第一个选项，15-30字]
选项2：[生成第二个选项，15-30字]
选项3：[生成第三个选项，15-30字]

注意：
1. 必须严格按照上述格式返回，每个部分都必须存在
2. 不要添加任何其他内容
3. 确保选项之间有明显的区别
4. 每个选项都应该能带来不同的故事发展

当前上下文：{self.context}
历史记录：{self.history}
当前提示：{prompt}""",
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