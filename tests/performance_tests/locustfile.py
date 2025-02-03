from locust import HttpUser, task


class ProjectPerfTest(HttpUser):

    @task
    def load_index(self):
        """Test : Chargement de la page d'accueil en ≤ 5 secondes."""
        with self.client.get("/", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(f"Index trop lent ({response.elapsed.total_seconds()}s)")

    @task
    def load_points_display(self):
        """Test : Chargement de la page des points en ≤ 5 secondes."""
        with self.client.get("/points_display", catch_response=True) as response:
            if response.elapsed.total_seconds() > 5:
                response.failure(f"Page points trop lente ({response.elapsed.total_seconds()}s)")

    @task
    def login_and_show_summary(self):
        """Test : Connexion en ≤ 2 secondes."""
        with self.client.post("/showSummary", data={"email": "john@simplylift.co"}, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Connexion trop lente ({response.elapsed.total_seconds()}s)")

    @task
    def book_places(self):
        """Test : Réservation de places en ≤ 2 secondes."""
        with self.client.post("/purchasePlaces", data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": "1"
        }, catch_response=True) as response:
            if response.elapsed.total_seconds() > 2:
                response.failure(f"Réservation trop lente ({response.elapsed.total_seconds()}s)")
