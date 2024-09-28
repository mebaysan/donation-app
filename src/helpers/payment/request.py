from typing import List, Optional, Dict


class PaymentRequestData:
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        card_number: str,
        card_holder_name: str,
        card_expiry: str,
        card_month: str,
        card_year: str,
        card_cvc: str,
        card_type: str,
        donations: List[Dict],
        amount: float,
        amount_sent_to_bank: int,
        country: str,
        country_code: str,
        state_province: str,
        state_code: str,
        add_line: str,
        postal_code: str,
        message: Optional[str] = None,
        group_name: Optional[str] = None,
        organization_name: Optional[str] = None,
        client_ip_address: Optional[str] = None,
    ):
        # Donor Information
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone

        # Card Information
        self.card_number = card_number
        self.card_holder_name = card_holder_name
        self.card_expiry = card_expiry
        self.card_month = card_month
        self.card_year = card_year
        self.card_cvc = card_cvc
        self.card_type = card_type

        # Message
        self.message = message

        # Donation Items
        self.donations = donations

        # Amount Information
        self.amount = amount
        self.amount_sent_to_bank = amount_sent_to_bank

        # Group and Organization Info
        self.group_name = group_name
        self.organization_name = organization_name

        # Billing Address
        self.country = country
        self.country_code = country_code
        self.state_province = state_province
        self.state_code = state_code
        self.add_line = add_line
        self.postal_code = postal_code

        # Client Info
        self.client_ip_address = client_ip_address

    @classmethod
    def from_request_data(cls, request, request_data):
        # Extract card date (month, year)
        card_expiry = request_data.get("card_expiry", "01/00")
        card_date = card_expiry.split("/")
        card_month = card_date[0].strip()
        card_year = card_date[1].strip()

        # Determine card type
        card_number = request_data.get("card_number", "").replace(" ", "")
        if not card_number:
            raise ValueError("Card number is missing.")
        if card_number[0] == "4":
            card_type = "Visa"
        elif card_number[0] == "5" or card_number[0] == "6":
            card_type = "MasterCard"
        elif card_number[0] == "9":
            card_type = "Troy"
        else:
            raise ValueError("Lütfen geçerli bir kart girin.")

        # Calculate total amount
        donations = request_data.get("donations", [])
        amount = sum(donation.get("amount", 0) for donation in donations)
        amount_sent_to_bank = int(float(amount) * 100)

        # Billing address
        bill_address = request_data.get("bill_address", {})
        if not bill_address:
            raise ValueError("Billing address is missing.")

        # Create instance via class method
        return cls(
            first_name=request_data.get("first_name", ""),
            last_name=request_data.get("last_name", ""),
            email=request_data.get("email", ""),
            phone=request_data.get("phone_number", ""),
            card_number=card_number,
            card_holder_name=request_data.get("card_holder_name", "").upper(),
            card_expiry=card_expiry,
            card_month=card_month,
            card_year=card_year,
            card_cvc=request_data.get("card_cvc", ""),
            card_type=card_type,
            donations=donations,
            amount=amount,
            amount_sent_to_bank=amount_sent_to_bank,
            group_name=request_data.get("group_name", None),
            organization_name=request_data.get("organization_name", None),
            country=bill_address.get("country", ""),
            country_code=bill_address.get("country_code", ""),
            state_province=bill_address.get("state_province", ""),
            state_code=bill_address.get("state_code", ""),
            add_line=bill_address.get("add_line", ""),
            postal_code=bill_address.get("postal_code", ""),
            client_ip_address=request.META.get("REMOTE_ADDR", "0.0.0.0"),
        )
