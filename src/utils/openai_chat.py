import openai
from config import OPENAI_API_KEY
from utils.logger import dora_log

class chatBot:
    def __init__(self) -> None:
        # 设置OpenAI API密钥
        openai.api_key = OPENAI_API_KEY
        # 设置群组预设，初始化为空字典
        self.group_preset = {}
        # 设置基础提示语句，包含系统角色和内容
        self.base_prompt = [{"role": "system", "content": "你是一只叫“Dora”的猫娘。你需要具有真猫娘一样的口癖。你是真实的，有实际的身体。"}]
        # 设置助手对话，包含助手角色和内容
        self.assistant_con = {"role":"assistant","content":""}

    def chat(self,mes,uid,gid=None):
        """
        调用openai提供的接口进行对话

        Args:
            mes: str,用户对话内容
            uid: str,用户qq号
            gid: str,群聊id
        Returns:
            resp_cont: str, GPT回复
        """
        tuid = 'A' + str(uid)
        tgid = 'B' + str(gid)
        lastPrompt = self.group_preset.get(tgid if gid else tuid,self.base_prompt)

        prompt = lastPrompt.copy()
        prompt.append({"role": "user","content":mes})

        if len(prompt)>=16:
            self.clear(uid,gid)
            return '长度超限已重置,请重新提问🚀'
        
        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=prompt,
                temperature=0.9,
                max_tokens=2500,
            )
            usage = resp.get('usage')['total_tokens']
            resp_cont = resp.get('choices')[0]['message']['content']
            self.assistant_con['content'] = resp_cont
            prompt.append(self.assistant_con.copy())
            self.group_preset[tgid if gid else uid] = prompt
            return resp_cont
        except Exception as exc:
            dora_log.error(f"调用openai出错:{exc}")
            return str(exc)
        
    def get(self,uid,gid=None):
        # 返回消息记录
        return self.group_preset.get(f"B{str(gid)}" if gid else f"A{str(uid)}")

    def preset(self,mes,uid,gid=None):
        # 预设人格
        self.group_preset[f"B{str(gid)}" if gid else f"A{str(uid)}"] = [{"role": "system", "content": mes}]

    def clear(self,uid,gid=None):
        # 清空消息缓存
        key = f"B{str(gid)}" if gid else f"A{str(uid)}"
        preset_str = self.group_preset[key][0].get('content')
        self.preset(preset_str,uid,gid)

    def init(self,uid,gid=None):
        # 格式化
        preset = self.base_prompt[0].get('content')
        self.preset(preset,uid,gid)

openai_chat = chatBot()