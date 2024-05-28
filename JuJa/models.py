from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
def get_default_date():
    return timezone.now().strftime('%Y-%m-%d')
class UserTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=100)

class TableRow(models.Model):
    user_table = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    column1 = models.CharField(max_length=100)
    column2 = models.CharField(max_length=100)
    column3 = models.CharField(max_length=100)
    column4 = models.CharField(max_length=100, default="0")
    column5 = models.CharField(max_length=100, default="0")
    column6 = models.CharField(max_length=100, default = "Nėra.")
class UserData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    invoice_date = models.CharField(max_length=100, default=get_default_date())
    payment_date = models.CharField(max_length=100, default=get_default_date())
    document_number = models.CharField(max_length=100, blank=True, default="0")
    company_code = models.CharField(max_length=100, blank=True, default="ĮMONĖS KODAS")
    company_name = models.CharField(max_length=100, blank=True, default="ĮMONĖ")
    client_address = models.CharField(max_length=100, blank=True, default="KLIENTO ADRESAS")
    client_code = models.CharField(max_length=100, blank=True, default="KLIENTO ĮMONĖS KODAS")
    vat_code = models.CharField(max_length=100, blank=True, default="KLIENTO PVM KODAS")
    buyer_name = models.CharField(max_length=100, blank=True, default="ĮMONĖS PAVADINIMAS")
    buyer_code = models.CharField(max_length=100, blank=True, default="ĮMONĖS KODAS")
    buyer_pvm_code = models.CharField(max_length=100, blank=True, default="PVM MOKĖTOJO KODAS")
    seller_address = models.CharField(max_length=100, blank=True, default="PARDAVĖJO ADRESAS")
    seller_phone_number = models.CharField(max_length=100, blank=True, default="PARDAVĖJO TEL. NR.")
    bank_name = models.CharField(max_length=100, blank=True, default="BANKAS")
    bank_account = models.CharField(max_length=100, blank=True, default="BANKO SĄSKAITA")
    swift = models.CharField(max_length=100, blank=True, default="SWIFT")
    alternative_payment = models.CharField(max_length=100, blank=True, default="ALTERNATYVUS MOKĖJIMAS")
    alternative_account = models.CharField(max_length=100, blank=True, default="ALTERNATYVI SĄSKAITA")
    member1 = models.CharField(max_length=100, blank=True, default="NARYS1")
    member2 = models.CharField(max_length=100, blank=True, default="NARYS2")
    member3 = models.CharField(max_length=100, blank=True, default="NARYS3")
    member4 = models.CharField(max_length=100, blank=True, default="NARYS4")
    responsible_member = models.CharField(max_length=100, blank=True, default="ATSAKINGAS DARBUOTOJAS")
class WriteTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    write_table_name = models.CharField(max_length=100)
class WriteOffRow(models.Model):
    write_table = models.ForeignKey(WriteTable, on_delete=models.CASCADE)
    user_table = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    