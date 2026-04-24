from locust import HttpUser, task, between

class WordPressUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def acessa_post_imagem_1mb(self):
        # Substitua ?p=X pelo ID do post com imagem de 1MB
        self.client.get("/?p=1")