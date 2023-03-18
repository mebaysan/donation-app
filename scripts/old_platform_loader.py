import pandas as pd
from apps.donor.models import DonationItem
from apps.payment.models import DonationTransaction, Donation
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

df = pd.read_csv("<PATH_TO_CSV_FILE>")

df["telefon"] = df["telefon"].apply(
    lambda x: "+" + str(x) if str(x).startswith("9") else x
)

old_donation = DonationItem.objects.filter(name="Eski Platform Bağışı").first()

error_count = 0
for i, j in df.iterrows():
    try:
        new_user = User.objects.create(username=j[0], email=j[0], phone_number=j[1])
        new_user.set_password(str(uuid.uuid4()))
        new_user.save()
        new_transaction = DonationTransaction(
            first_name="",
            last_name="",
            email=new_user.email,
            phone_number=new_user.phone_number,
            amount=j[3],
            amount_sent_to_bank=j[2],
            merchant_order_id="eski-platform-bagisi",
            message="Eski Platform Bağışı",
            group_name="",
            organization_name="",
            is_complete=True,
            status_code="00",
            status_code_description="Eski Platform Bağışı (Başarılı).",
            user=new_user,
            md_code="eski-platform-bagisi",
        )
        new_transaction.save()
        new_donation = Donation.objects.create(
            donation_item=old_donation,
            amount=j[3],
            donation_transaction=new_transaction,
            user=new_transaction.user,
        )
        new_donation.save()
    except Exception as e:
        print(e)
        print(f"Error occured: {j[0]} {j[1]}")
        error_count += 1
        print(f"Error count: {error_count}")
