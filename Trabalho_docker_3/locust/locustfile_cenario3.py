from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def acessa_post_imagem_300kb(self):
        self.client.get("/?p=11")