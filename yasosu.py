from curl_cffi import requests

class UploaderResponse:
    def __init__(self, code, message = None, link = None, response = None):
        self.code = code
        self.message = message
        self.link = link
        self.response = response

class PasteObject:
    def __init__(self, uploader, url, createdAt, content, contentType, textContentType):
        self.uploader = uploader
        self.url = url
        self.createdAt = createdAt
        self.content = content
        self.contentType = contentType
        self.textContentType = textContentType

    def delete(self):
        response = requests.delete(f"https://api.yaso.su/v1/records/{self.url}", cookies=self.uploader.cookies, headers=self.uploader.headers)
        if response.status_code == 200:
            return True
        return False


class YasoSuUploader:
    def __init__(self, yasosu_session: str = None, captcha: str = None):
        self.cookies = {
            "yasosu_session": yasosu_session
        }
        self.captcha = captcha
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
            "Content-Type": "application/json;charset=utf-8",
            "Referer": "https://yaso.su/",
            "Origin": "https://yaso.su",
            "DNT": "1",
            "Sec-GPC": "1",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "Connection": "keep-alive",
            "Idempotency-Key": "9420250686213929735"
        }
    
    def upload(self, text, url = None, expirein = -1):
        data = {
            'content': text,
            'captcha': self.captcha,
            'codeLanguage': 'auto',
            'expirationTime': expirein,
            'url': url or None
        }
        response = requests.post("https://api.yaso.su/v1/records", cookies=self.cookies, json=data, headers=self.headers)

        if response.status_code == 200:
            try:
                json_response = response.json()
                link = f"https://yaso.su/{json_response['url']}"
                return UploaderResponse(response.status_code, link=link)
            except KeyError:
                return UploaderResponse(response.status_code, message='URL not found in response', response=response.text)
        else:
            return UploaderResponse(response.status_code, response=response.text)
    
    def delete_paste(self, url):
        response = requests.delete(f"https://api.yaso.su/v1/records/{url}", cookies=self.cookies, headers=self.headers)
        if response.status_code == 200:
            return True
        return False
        
    def get_pastes(self) -> list[PasteObject] | None:
        response = requests.get("https://api.yaso.su/v1/user/get_pastes", cookies=self.cookies, headers=self.headers)
        j = response.json()
        if not j["isEmpty"]:
            mass = []
            raw = j['data']
            for item in raw:
                mass.append(PasteObject(self, item["url"], item["createdAt"], item["content"], item["contentType"], item["textContentType"]))
            return mass
        return None