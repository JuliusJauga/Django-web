from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.http import HttpResponse
from .models import TableRow, UserTable, UserData, WriteTable, WriteOffRow
from django.utils import timezone
from django.template.loader import get_template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from xhtml2pdf import pisa
# Create your views here.
import locale

locale.setlocale(locale.LC_ALL, '')


def index(request):
    return render(request, "JuJa/nav_bar.html")

def login_user(request):
    if request.user.is_authenticated:
        return redirect('JuJa:index')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('JuJa:index')
        else:
            messages.success(request, ("Nepavyko prisijungti..."))
            return redirect('JuJa:login_user')
    return render(request, 'JuJa/auth.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("Atsijungėte..."))
    return redirect('JuJa:index')

def register_user(request):
    if request.user.is_authenticated:
        return redirect('JuJa:index')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, ("You have registered..."))
            return redirect('JuJa:index')
    else:
        form = UserCreationForm()
    return render(request, 'JuJa/register.html', {"form": form})

@login_required
def make_invoice(request):
    if request.method == "POST":
        table_data = request.POST.getlist('table_data[]')
        table_name = request.POST.get('table_name')
        user = request.user
        user_table = UserTable.objects.create(user=user, table_name=table_name)

        for key in request.POST.keys():
            if key.startswith("product_"):
                row_number = key.split("_")[1]
                product = request.POST.get(key)
                price = request.POST.get('price_' + row_number)
                quantity = request.POST.get('quantity_' + row_number)
                purpose = request.POST.get('purpose_' + row_number)
                if not purpose:
                    purpose = "Nėra."
                if not product:
                    continue
                if not price:
                    price = "0"
                if not quantity:
                    quantity = "0"
                row_instance = TableRow.objects.create(
                    user_table=user_table,
                    column1=product,
                    column2=price,
                    column3=quantity,
                    column4=str(float(price) * float(quantity)),
                    column5=str(float(price) * float(quantity) * 1.21),
                    column6=purpose
                )
        return redirect('JuJa:view_invoices')
    return render(request, 'JuJa/make_invoice.html', {})

@login_required
def view_invoices(request, invoice_id=None):
    if not UserTable.objects.filter(user=request.user).exists():
        return redirect('JuJa:index')
    user_tables = UserTable.objects.filter(user=request.user)
    context = {'user_tables': user_tables}
    return render(request, 'JuJa/view_invoices.html', context)

@login_required
def view_invoice(request, invoice_id):
    user_data, created = UserData.objects.get_or_create(user=request.user)
    table_rows = TableRow.objects.filter(user_table=invoice_id)
    sum = 0
    formatted_sum = "0.00"
    formatted_sum_with_vat = "0.00"
    formatted_vat = "0.00"
    for row in table_rows:
        sum += float(row.column4)
        sum_with_vat = sum * 1.21
        vat = sum * 0.21
        formatted_sum = locale.format_string("%.2f", sum, grouping=True)
        formatted_sum_with_vat = locale.format_string("%.2f", sum_with_vat, grouping=True)
        formatted_vat = locale.format_string("%.2f", vat, grouping=True)
    return render(request, 'JuJa/product_invoice.html', {'table_rows': table_rows, 'invoice_id': invoice_id, 'sum': formatted_sum, 'sum_with_vat': formatted_sum_with_vat, 'vat': formatted_vat, 'user_data': user_data})

@login_required
def delete_invoices(request):
    if not UserTable.objects.filter(user=request.user).exists():
        return redirect('JuJa:index')
    user_tables = UserTable.objects.filter(user=request.user)
    context = {'user_tables': user_tables}
    return render(request, 'JuJa/delete_invoices.html', context)

@login_required
def edit_invoice(request, invoice_id):
    table_rows = TableRow.objects.filter(user_table=invoice_id)
    sum = 0
    for row in table_rows:
        sum += float(row.column4)
        sum_with_vat = sum * 1.21
        vat = sum * 0.21
        formatted_sum = locale.format_string("%.2f", sum, grouping=True)
        formatted_sum_with_vat = locale.format_string("%.2f", sum_with_vat, grouping=True)
        formatted_vat = locale.format_string("%.2f", vat, grouping=True)
    return render(request, 'JuJa/edit_invoice.html', {'table_rows': table_rows, 'invoice_id': invoice_id, 'sum': formatted_sum, 'sum_with_vat': formatted_sum_with_vat, 'vat': formatted_vat})

@login_required
def make_write_off(request):
    if request.method == "POST":
        selected_tables = request.POST.getlist('selected_tables')
        write_table_name = request.POST.get('write_table_name')
        write_table = WriteTable.objects.create(user=request.user, write_table_name=write_table_name)
        for table_id in selected_tables:
            user_table = UserTable.objects.get(id=table_id)
            WriteOffRow.objects.create(write_table=write_table, user_table=user_table)
        return redirect('JuJa:view_write_offs')
    user_tables = UserTable.objects.filter(user=request.user)
    context = {'user_tables': user_tables}
    return render(request, 'JuJa/make_write_off.html', context)

@login_required
def enter_information(request):
    if request.method == "POST":
        user = request.user
        if UserData.objects.filter(user=user).exists():
            UserData.objects.filter(user=user).delete()
        
        invoice_date_str = request.POST.get('invoice_date')
        payment_date_str = request.POST.get('payment_date')
        if invoice_date_str:
            invoice_date = timezone.datetime.strptime(invoice_date_str, '%Y-%m-%d')
        else:
            invoice_date = timezone.now()

        if payment_date_str:
            payment_date = timezone.datetime.strptime(payment_date_str, '%Y-%m-%d')
        else:
            payment_date = timezone.now()
        formatted_invoice = invoice_date.strftime('%Y-%m-%d')
        formatted_payment = payment_date.strftime('%Y-%m-%d')
        user_data = UserData.objects.create(user=user,
                            document_number=request.POST.get('document_number', '0'),
                            company_name=request.POST.get('company_name', 'ĮMONĖ'),
                            client_address=request.POST.get('client_address', 'KLIENTO ADRESAS'),
                            company_code=request.POST.get('company_code', 'ĮMONĖS KODAS'),
                            vat_code=request.POST.get('vat_code', 'KLIENTO PVM KODAS'),
                            invoice_date=formatted_invoice,
                            payment_date=formatted_payment,
                            buyer_name=request.POST.get('buyer_name', 'ĮMONĖS PAVADINIMAS'),
                            buyer_code=request.POST.get('buyer_code', 'ĮMONĖS KODAS'),
                            buyer_pvm_code=request.POST.get('buyer_pvm_code', 'PVM MOKĖTOJO KODAS'),
                            seller_address=request.POST.get('seller_address', 'ADRESAS'),
                            seller_phone_number=request.POST.get('seller_phone_number', 'TELEFONAS'),
                            bank_name=request.POST.get('bank_name', 'BANKAS'),
                            bank_account=request.POST.get('bank_account', 'BANKO SASKAITA'),
                            swift=request.POST.get('swift', 'SWIFTAS'),
                            alternative_payment=request.POST.get('alternative_payment', 'ALTERNATYVUS MOKĖJIMAS'),
                            alternative_account=request.POST.get('alternative_account', 'ALTERNATYVI SĄSKAITA'),
                            member1=request.POST.get('member1', 'NARYS1'),
                            member2=request.POST.get('member2', 'NARYS2'),
                            member3=request.POST.get('member3', 'NARYS3'),
                            member4=request.POST.get('member4', 'NARYS4'),
                            responsible_member=request.POST.get('responsible_member', 'ATSAKINGAS DARBUOTOJAS')
        )
        if (user_data.document_number == ""):
            user_data.document_number = "0"
        if (user_data.company_name == ""):
            user_data.company_name = "ĮMONĖ"
        if (user_data.client_address == ""):
            user_data.client_address = "KLIENTO ADRESAS"
        if (user_data.company_code == ""):
            user_data.company_code = "ĮMONĖS KODAS"
        if (user_data.vat_code == ""):
            user_data.vat_code = "KLIENTO PVM KODAS"
        if (user_data.buyer_name == ""):
            user_data.buyer_name = "ĮMONĖS PAVADINIMAS"
        if (user_data.buyer_code == ""):
            user_data.buyer_code = "ĮMONĖS KODAS"
        if (user_data.buyer_pvm_code == ""):
            user_data.buyer_pvm_code = "PVM MOKĖTOJO KODAS"
        if (user_data.seller_address == ""):
            user_data.seller_address = "ADRESAS"
        if (user_data.seller_phone_number == ""):
            user_data.seller_phone_number = "TELEFONAS"
        if (user_data.bank_name == ""):
            user_data.bank_name = "BANKAS"
        if (user_data.bank_account == ""):
            user_data.bank_account = "BANKO SASKAITA"
        if (user_data.swift == ""):
            user_data.swift = "SWIFTAS"
        if (user_data.alternative_payment == ""):
            user_data.alternative_payment = "ALTERNATYVUS MOKĖJIMAS"
        if (user_data.alternative_account == ""):
            user_data.alternative_account = "ALTERNATYVI SĄSKAITA"
        if (user_data.member1 == ""):
            user_data.member1 = "NARYS1"
        if (user_data.member2 == ""):
            user_data.member2 = "NARYS2"
        if (user_data.member3 == ""):
            user_data.member3 = "NARYS3"
        if (user_data.member4 == ""):
            user_data.member4 = "NARYS4"
        if (user_data.responsible_member == ""):
            user_data.responsible_member = "ATSAKINGAS DARBUOTOJAS"
        user_data.save()
        return redirect('JuJa:view_invoices')
    return render(request, 'JuJa/information_collect.html', {})

@login_required
def delete_invoice(request, invoice_id):
    UserTable.objects.filter(id=invoice_id).delete()
    return redirect('JuJa:delete_invoices')

@login_required
def view_write_offs(request, write_off_id=None):
    if not WriteTable.objects.filter(user=request.user).exists():
        return redirect('JuJa:index')
    user_write_offs = WriteTable.objects.filter(user=request.user)
    context = {'user_write_offs': user_write_offs}
    return render(request, 'JuJa/view_write_offs.html', context)

@login_required
def view_write_off(request, write_off_id):
    write_off_rows = WriteOffRow.objects.filter(write_table=write_off_id)
    table_rows = TableRow.objects.filter(user_table__in=write_off_rows.values('user_table'))
    sum = 0
    invoice_id = write_off_id
    user_data, created = UserData.objects.get_or_create(user=request.user)
    formatted_sum = "0.00"
    formatted_sum_with_vat = "0.00"
    formatted_vat = "0.00"
    for row in table_rows:
        sum += float(row.column4)
        sum_with_vat = sum * 1.21
        vat = sum * 0.21
        formatted_sum = locale.format_string("%.2f", sum, grouping=True)
        formatted_sum_with_vat = locale.format_string("%.2f", sum_with_vat, grouping=True)
        formatted_vat = locale.format_string("%.2f", vat, grouping=True)
    context = {'table_rows': table_rows, 'invoice_id': invoice_id, 'sum': formatted_sum, 'sum_with_vat': formatted_sum_with_vat, 'vat': formatted_vat, 'user_data': user_data}
    if request.method == "POST":
        saveToPdf(request, context)
    return render(request, 'JuJa/write_off.html', context)

@login_required
def delete_write_offs(request):
    if not WriteTable.objects.filter(user=request.user).exists():
        return redirect('JuJa:index')
    user_write_offs = WriteTable.objects.filter(user=request.user)
    context = {'user_write_offs': user_write_offs}
    return render(request, 'JuJa/delete_write_offs.html', context)

@login_required
def delete_write_off(request, write_off_id):
    WriteTable.objects.filter(id=write_off_id).delete()
    WriteOffRow.objects.filter(write_table=write_off_id).delete()
    return redirect('JuJa:delete_write_offs')

@login_required
def saveToPdf(request, context):
    html_content = render_to_string('JuJa/write_off_proxy.html', context)
    with open('invoicas.pdf', 'wb') as output_file:
        pisa_status = pisa.CreatePDF(
            html_content,
            dest=output_file,
            encoding='utf-8'
        )
    return pisa_status.err == 0


