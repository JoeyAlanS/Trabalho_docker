from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        self.client.get("/", name="Home")

    @task(2)
    def imagem_1mb(self):
        self.client.get("/?p=6", name="Imagem 1MB")

    @task(5)
    def texto_400kb(self):
        self.client.get("/?p=9", name="Texto 400KB")

    @task(3)
    def imagem_300kb(self):
        self.client.get("/?p=11", name="Imagem 300KB")

    @task(2)
    def home(self):
        self.client.get("/", name="Home")