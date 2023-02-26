import requests
from django.core.management.base import BaseCommand
from apps.management.models import Country, StateProvince


class Command(BaseCommand):
    help = "Imports countries and state provinces from JSON file"

    def handle(self, *args, **options):
        # Get the JSON data from the URL
        url = "https://gist.githubusercontent.com/mebaysan/610479b2e5362853b876637aa1f58883/raw/0969bb2ba61f28da6e6d55a881b088cd83e53ba6/country_state.json"
        response = requests.get(url)
        data = response.json()

        for country_data in data:
            country, created = Country.objects.get_or_create(
                name=country_data["name"],
                country_code=country_data["countryCode"],
                country_code_alpha3=country_data["countryCodeAlpha3"],
                phone=country_data["phone"],
                currency=country_data["currency"],
            )
            if country_data["stateProvinces"] != None:
                for state_data in sorted(
                    country_data["stateProvinces"], key=lambda x: x["name"]
                ):
                    try:
                        state, created = StateProvince.objects.get_or_create(
                            name=state_data["name"],
                            country=country,
                        )

                        if created:
                            self.stdout.write(
                                f"Created state: {state.name} ({country.name})"
                            )
                    except Exception as e:
                        self.stdout.write(f"Error: {e}")
