import requests
from django.core.management.base import BaseCommand
from apps.management.models import Country, StateProvince


class Command(BaseCommand):
    help = "Imports countries and state provinces from JSON file"

    def get_data_from_api(self):
        # Get the JSON data from the URL
        url = "https://gist.githubusercontent.com/mebaysan/610479b2e5362853b876637aa1f58883/raw/0969bb2ba61f28da6e6d55a881b088cd83e53ba6/country_state.json"
        response = requests.get(url)
        return response.json()

    def handle(self, *args, **options):
        data = self.get_data_from_api()
        try:
            for country_data in data:
                if Country.objects.filter(name=country_data["name"]).exists():
                    continue
                else:
                    country = Country.objects.create(
                        name=country_data["name"],
                        country_code=country_data["countryCode"],
                        country_code_alpha3=country_data["countryCodeAlpha3"],
                        phone=country_data["phone"],
                        currency=country_data["currency"],
                    )
                    self.stdout.write(f"Created country: {country.name}")
                if country_data["stateProvinces"] != None:
                    for state_data in sorted(
                        country_data["stateProvinces"], key=lambda x: x["name"]
                    ):
                        if StateProvince.objects.filter(
                            name=state_data["name"]
                        ).exists():
                            continue
                        else:
                            state = StateProvince.objects.create(
                                name=state_data["name"],
                                country=country,
                            )
                            self.stdout.write(
                                f"Created state: {state.name} ({country.name})"
                            )
        except Exception as e:
            self.stdout.write(f"Error: {e}")
