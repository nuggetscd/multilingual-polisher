from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# DeepSeek API配置（从.env读取，不要直接写key！）
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-chat"

# 挂载静态文件目录（前端页面放这里）
app.mount("/static", StaticFiles(directory="static"), name="static")


class PolishRequest(BaseModel):
    text: str
    target_language: str  # "中文", "English", "Français"
    style: str            # "正式", "口语", "小红书风"


@app.get("/")
def read_root():
    return FileResponse("static/index.html")


@app.post("/polish")
async def polish_text(request: PolishRequest):
    # 根据风格构建prompt
    style_prompts = {
        "正式": "使用正式、专业的语言风格，适合商务或学术场合",
        "口语": "使用自然、轻松的口语风格，像朋友之间的对话",
        "小红书风": "使用小红书博主风格：活泼、有感染力，适当使用emoji，标题要吸引眼球，内容要有干货感"
    }

    language_prompts = {
        "中文": "请用中文输出",
        "English": "Please output in English",
        "Français": "Veuillez répondre en français"
    }

    style_desc = style_prompts.get(request.style, "自然流畅的语言风格")
    lang_desc = language_prompts.get(request.target_language, "请用中文输出")

    prompt = f"""你是一个专业的多语言文本润色助手。
请对以下文本进行润色改写：
- 风格要求：{style_desc}
- 语言要求：{lang_desc}
- 只输出润色后的文本，不要加解释或前缀

原文：
{request.text}"""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(DEEPSEEK_API_URL, json=payload, headers=headers)
        result = response.json()

    polished_text = result["choices"][0]["message"]["content"]
    return {"result": polished_text}
