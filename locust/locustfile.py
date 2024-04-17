from locust import HttpUser, between, task


class WebsiteUser(HttpUser):

    
    @task
    def index(self):
        self.client.get("/")

    @task
    def login_test(self):
        self.client.post("/accounts/api/V1/token/create/", json={"email":"admin@hamid.com", "password":"M@hla1392"})
