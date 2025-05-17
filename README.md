# YasoSuUploader
Reversed API for yaso.su pastebin

# How to use?

1. Go to [yaso.su](https://yaso.su)
2. Click F12 - Network
3. We write any pasta, we pass the captcha
4. Looking for 200 POST to `api.yaso.su`, `records`
   
![session](https://github.com/user-attachments/assets/126eb7a6-5c72-468f-9f4b-9541b9110324)

![captcha](https://github.com/user-attachments/assets/1a3a6e0f-4e4f-4d46-a9dc-a169faa281c2)

5. Take the session and captcha

# Template

```python
if __name__ == "__main__":
    uploader = YasoSuUploader("session","captcha")
    result = uploader.upload(input("txt > "), input("url > "))
    print(result.link)
```
