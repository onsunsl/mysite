import logging
import os

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View


class ChatApiView(View):

    history = list()

    @property
    def url(self):
        base = os.environ.get("API_BASE")
        model = os.environ.get("API_MODEL")
        version = os.environ.get("API_VERSION")

        return f"{base}/{model}/chat/completions?api-version={version}"

    def chat(self, content: dict):
        text = content.get("question")
        import requests

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
            "Sec-Ch-Ua": '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
            "api-key": os.environ.get("API_KEY"),
            "Content-Type": "application/json",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "Windows",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        }

        system = {"role": "system", "content": "你是一个全能王助手"}
        user = {"role": "user", "content": "讲一个故事"}

        data = {
            "messages": [
            ],
            "temperature": 0.7,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0,
            "max_tokens": 4000,
            "stop": None,
            "stream": False
        }
        user["content"] = text
        msg = list()
        msg.append(system)
        if self.history:
            msg.extend(self.history)
        msg.append(user)

        data["messages"] = msg
        logging.info(f"You:{text} {self.url}")
        r = requests.post(self.url, headers=headers, json=data)
        answer = r.json().get("choices")[0].get("message").get("content")
        logging.info(f"AI:{answer}\n\n")
        self.history.append({"role": "user", "content": text})
        self.history.append({"role": "assistant", "content": answer})
        return JsonResponse(dict(code="0000", data=dict(answer=answer), msg="成功"))

    def get(self, request):
        return render(request, "chat.html")

    def post(self, request):
        try:
            data = request.POST
            return self.chat(data)
        except Exception as err:
            logging.error(f"Chat POST 异常:{err}", exc_info=True)
            return JsonResponse(dict(code="0001", data=dict(answer=f"{err}"), msg="失败"))

    def delete(self, request):
        self.history.clear()
        return JsonResponse(dict(code="0000", data=None, msg="成功"))

