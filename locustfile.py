from locust import HttpUser, task, between

class OpenBMCUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://localhost:2443"

    @task
    def get_system_info(self):
        self.client.get("/redfish/v1/Systems/system", auth=("root", "0penBmc"), verify=False, name="SystemInfo")

    @task
    def check_power_state(self):
        with self.client.get("/redfish/v1/Systems/system", 
                           auth=("root", "0penBmc"), 
                           verify=False,
                           catch_response=True, name="Check Power") as response:
            data = response.json()
            power_state = data.get("PowerState")
            if power_state in ["On", "Off"]:
                response.success()
                print(f"Current PowerState: {power_state}")

class PublicAPIUser(HttpUser):
    wait_time = between(1, 3)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def get_posts(self):
        self.client.get("/posts")

    @task
    def get_weather(self):
        self.client.get("https://yandex.ru/pogoda/ru/novosibirsk")
