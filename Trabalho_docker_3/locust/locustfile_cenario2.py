from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def acessa_post_texto_400kb(self):
        self.client.get("/?p=9")