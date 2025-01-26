import requests

MAX_MESSAGE_SIZE = 2000


class DiscordAPI(object):
    def __init__(self, auth_token=None):
        self.auth_token = auth_token

    def get_headers(self):
        return {"Authorization": self.auth_token}

    def check_content(self, content):
        if len(content) > MAX_MESSAGE_SIZE:
            print("Can't send discord message of size " + str(len(content)))
            return False
        return True

    def check_can_send(self, content=""):
        return self.auth_token is not None and self.check_content(content)

    def post(self, url, content, file=None):
        if self.check_can_send(content):
            if file is None:
                res = requests.post(url, headers=self.get_headers(), data={"content": content})
            else:
                res = requests.post(url, headers=self.get_headers(), data={"content": content}, files={'file': file})
            return res.status_code
        return False

    def get(self, url):
        if self.check_can_send():
            r = requests.get(url, headers=self.get_headers())
            data = r.json()
            return data

    def delete(self, url):
        if self.check_can_send():
            r = requests.delete(url, headers=self.get_headers())
            return r.status_code == 204  # all went good
