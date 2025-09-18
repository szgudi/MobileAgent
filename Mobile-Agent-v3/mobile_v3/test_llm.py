
import os
from dotenv import load_dotenv, find_dotenv
from utils.call_mobile_agent_e import GUIOwlWrapper

def parse_response(response: str) -> dict:
    thought = response.split("### 思考")[-1].split("### 动作")[0].replace("\n", " ").replace("  ", " ").replace(
        "###", "").strip()
    action = response.split("### 动作")[-1].split("### 描述")[0].replace("\n", " ").replace("  ", " ").replace(
        "###", "").strip()
    description = response.split("### 描述")[-1].replace("\n", " ").replace("  ", " ").replace("###", "").strip()
    return {"thought": thought, "action": action, "description": description}

_ = load_dotenv(find_dotenv())
base_url = os.getenv("BASE_URL",'')
api_key = os.getenv("OPENAI_API_KEY",'')
model = os.getenv("MODEL",'')

vllm = GUIOwlWrapper(api_key, base_url, model)

prompt = '''
你是一个能够代表用户操作安卓手机的智能代理。你的目标是根据手机当前状态和用户的请求，决定应执行的操作。

### 用户请求 ###
打开系统设置页面

#### 原子操作 ###
原子操作函数以 action(arguments): 描述 的格式列出，如下所示：

click(coordinate): 点击屏幕上指定 (x, y) 坐标的点。使用示例：{"action": "click", "coordinate": [x, y]}

long_press(coordinate): 在屏幕上的位置 (x, y) 长按。使用示例：{"action": "long_press", "coordinate": [x, y]}

type(text): 向当前已激活的输入框或文本字段中输入文本。如果你已激活输入框，可以在屏幕底部看到“ADB Keyboard {on}”字样。如果没有，请再次点击输入框以确认。请确保在输入前已正确激活正确的输入框。使用示例：{"action": "type", "text": "你想输入的文本"}

system_button(button): 按下系统按钮，包括返回、主页和回车。使用示例：{"action": "system_button", "button": "Home"}

swipe(coordinate, coordinate2): 从具有坐标的位置滚动到具有 coordinate2 的位置。请确保滑动的起点和终点位于可滑动区域内，并远离键盘（y1 < 1400）。使用示例：{"action": "swipe", "coordinate": [x1, y1], "coordinate2": [x2, y2]}


重要提示：
coordinate的x和y值取图标中心位置的图标
请按以下格式提供你的输出，包含三个部分：

### 思考 ###
详细说明你为所选操作提供的理由。

### 动作 ###
从提供的选项中选择一个操作或快捷方式。
你必须使用有效的 JSON 格式提供你的决策，明确指定 action 及其参数。例如，如果你想输入一些文本，你应该写 {"action":"type", "text": "你想输入的文本"}。

### 描述 ###
对所选操作的简要描述。
给出识别到的图标的中心位置坐标的X和Y值。
给出整个图片的大小。
'''

image_home = './image/home.png'
image_apps = './image/apps_small.png'

output_action, message_manager, raw_response = vllm.predict_mm(prompt,[image_apps])

parsed_result_action = parse_response(output_action)
action_thought, action_object_str, action_description = parsed_result_action['thought'], parsed_result_action['action'], parsed_result_action['description']

print(action_object_str)


