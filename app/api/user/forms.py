from fastapi import Form

class LoginForm:
    def __init__(self, email: str = Form(...), password: str = Form(...)):

        self.email = email
        self.password = password
