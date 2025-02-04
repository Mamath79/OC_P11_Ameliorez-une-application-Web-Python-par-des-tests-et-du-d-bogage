from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):

    wait_time = between(0.1, 1)

    @task
    def load_index(self):
        """Test : Chargement de la page d'accueil."""
        self.client.get("/")

    @task
    def load_points_display(self):
        """Test : Chargement de la page des points."""
        self.client.get("/points_display")

    @task
    def login_and_show_summary(self):
        """Test : Connexion en ≤ 2 secondes."""
        self.client.post("/showSummary", data={"email": "john@simplylift.co"})

    @task
    def book_places(self):
        """Test : Réservation de places en ≤ 2 secondes."""
        self.client.post(
            "/purchasePlaces",
            data={
                "competition": "Spring Festival",
                "club": "Simply Lift",
                "places": "1",
            },
        )
