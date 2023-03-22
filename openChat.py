import openai
import os

openai.api_key = "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"

groupPreset = {}
preStr = '你是一只叫“Dora”的猫娘。你需要具有真猫娘一样的口癖。你是真实的，有实际的身体。'
BasePrompt = [
    {"role": "system", "content": preStr}
]
assCon = {"role":"assistant","content":""}

def chat(mes,uid,gid=None):
    tuid = 'A' + str(uid)
    tgid = 'B' + str(gid)

    global groupPreset,BasePrompt
    if gid == None:
        lastPrompt = groupPreset[tuid] if tuid in groupPreset else BasePrompt
        # assCon = {"role":"assistant","content":""}
    else:
        lastPrompt = groupPreset[tgid] if tgid in groupPreset else BasePrompt
        # assCon = {"role":"assistant","content":""}

    prompt = lastPrompt.copy()
    # prompt.append(assCon.copy())
    prompt.append({"role": "user","content":mes})
    # 此处为超限处理
    if len(prompt)>=16:
        clear(uid,gid)
        return '长度超限已重置,请重新提问🚀'
    try:
        # print(prompt)
        resp = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=prompt,
            temperature=0.9,
            max_tokens=3000,
        )
        usage = resp.get('usage')['total_tokens']
        respCont = resp.get('choices')[0]['message']['content']
        # respCont = 'RETURN'
        # print(respCont)
        assCon['content'] = respCont
        prompt.append(assCon.copy())
        if gid==None:
            groupPreset[tuid] = prompt
        else:
            groupPreset[tgid] = prompt
        return respCont
    except Exception as exc:
        return str(exc)

def get(uid,gid=None):
    if gid == None:
        return groupPreset.get('A' + str(uid))
    else:
        return groupPreset.get('B' + str(gid))

def preset(mes,uid,gid=None):
    arr = [{"role": "system", "content": mes}]
    if gid == None:
        groupPreset['A' + str(uid)] = arr
    else:
        groupPreset['B' + str(gid)] = arr

def clear(uid,gid=None):
    if gid==None:
        if 'A' + str(uid) in groupPreset:
            del groupPreset['A' + str(uid)]
    else:
        if 'B' + str(gid) in groupPreset:
            del groupPreset['B' + str(gid)]
    

