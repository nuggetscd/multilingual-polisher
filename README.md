#  多语言文本润色工具
Multilingual Text Polisher · Outil de réécriture multilingue

## 项目简介
基于 FastAPI + DeepSeek API 构建的多语言文本润色工具，支持中/英/法三语输出，
提供正式、口语、小红书风格三种写作风格切换。

## 技术栈
- **后端**：Python · FastAPI · httpx（异步HTTP请求）
- **前端**：HTML · CSS · JavaScript（原生，前后端分离）
- **AI**：DeepSeek API · Prompt Engineering

## 功能
- 输入任意文本，一键润色改写
- 支持输出语言：中文 / English / Français
- 支持输出风格：正式 / 口语 / 小红书风

## 本地运行
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
浏览器打开 http://localhost:8000