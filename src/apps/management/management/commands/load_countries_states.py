import json
from django.core.management.base import BaseCommand
from apps.management.models import Country, StateProvince
from django.conf import settings


class Command(BaseCommand):
    help = "Imports countries and state provinces from JSON file"

    def get_country_state_data_from_file(self):
        with open(settings.DATA_FILE_COUNTRIES_STATES) as f:
            data = json.load(f)
        f.close()
        return data

    def get_city_iso_code_data_from_file(self):
        with open(settings.DATA_FILE_ISO_CODES) as f:
            data = json.load(f)
        f.close()
        return data

    def handle(self, *args, **options):
        country_states_data = self.get_country_state_data_from_file()
        state_province_iso_codes = self.get_city_iso_code_data_from_file()

        try:
            for country_data in country_states_data:
                country_obj = Country.objects.filter(name=country_data["name"]).first()
                if country_obj:
                    # update country data
                    country_obj.name = country_data["name"]
                    country_obj.country_code = country_data["countryCode"]
                    country_obj.country_code_alpha3 = country_data["countryCodeAlpha3"]
                    country_obj.phone = country_data["phone"]
                    country_obj.currency = country_data["currency"]
                    country_obj.save()
                    self.stdout.write(f"Updated country: {country_obj.name}")
                else:
                    country_obj = Country.objects.create(
                        name=country_data["name"],
                        country_code=country_data["countryCode"],
                        country_code_alpha3=country_data["countryCodeAlpha3"],
                        phone=country_data["phone"],
                        currency=country_data["currency"],
                    )
                    self.stdout.write(f"Created country: {country_obj.name}")
                if country_data["stateProvinces"] != None:
                    for state_data in sorted(
                        country_data["stateProvinces"], key=lambda x: x["name"]
                    ):
                        state_iso_code = self.get_state_iso_code(
                            state_province_iso_codes,
                            country_obj.country_code,
                            state_data["name"],
                        )
                        state_province_obj = StateProvince.objects.filter(
                            name=state_data["name"]
                        ).first()
                        if state_province_obj:
                            # update state data
                            state_province_obj.name = state_data["name"]
                            state_province_obj.country = country_obj
                            state_province_obj.state_code = state_iso_code
                            state_province_obj.save()
                            self.stdout.write(
                                f"Updated state: {state_province_obj.name} ({country_obj.name})"
                            )
                        else:
                            state_province_obj = StateProvince.objects.create(
                                name=state_data["name"],
                                country=country_obj,
                                state_code=state_iso_code,
                            )
                            self.stdout.write(
                                f"Created state: {state_province_obj.name} ({country_obj.name})"
                            )
        except Exception as e:
            self.stdout.write(f"Error: {e}")

    def get_state_iso_code(self, state_province_iso_codes, country_code, state_name):
        try:
            state_name_in_search = state_name
            # convert Turkish chars to English chars
            # iso code data has English chars
            state_name_in_search = (
                state_name.replace("ı", "i")
                .replace("ğ", "g")
                .replace("ü", "u")
                .replace("ş", "s")
                .replace("ö", "o")
                .replace("ç", "c")
                .replace("İ", "I")
                .replace("Ğ", "G")
                .replace("Ü", "U")
                .replace("Ş", "S")
                .replace("Ö", "O")
                .replace("Ç", "C")
            )
            state_code = state_province_iso_codes.get(country_code, {}).get(
                state_name_in_search
            )["iso_code"]
            return state_code
        except Exception as e:
            self.stdout.write(
                f"An error occured while trying to get_state_iso_code ({country_code} - {state_name}): {e}"
            )
            return ""
