from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def acessa_post_texto_400kb(self):
        # Substitua ?p=X pelo ID do post com texto de 400KB
        self.client.get("/?p=2")