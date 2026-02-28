from django.db import models

# Create your models here.
import uuid
from django.db import models
from django.core.validators import MinValueValidator


class FeeCategory(models.Model):
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="fee_categories")
    name = models.CharField(max_length=100)
    is_compulsory = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("school", "name")
        ordering = ["name"]

    def __str__(self):
        return self.name


class FeeStructure(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="fee_structures")
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE)
    term = models.ForeignKey("schools.Term", on_delete=models.CASCADE, related_name="fee_structures")
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    applies_to = models.CharField(
        max_length=10,
        choices=[("all", "All Students"), ("boarder", "Boarders Only"), ("day", "Day Scholars Only")],
        default="all",
    )
    class_level = models.ForeignKey("academics.ClassLevel", on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    description = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return f"{self.category.name} — {self.term} — KES {self.amount:,.0f}"


class FeeInvoice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="fee_invoices")
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="fee_invoices")
    academic_year = models.ForeignKey("schools.AcademicYear", on_delete=models.CASCADE)
    term = models.ForeignKey("schools.Term", on_delete=models.CASCADE, related_name="fee_invoices")
    invoice_number = models.CharField(max_length=30, unique=True)
    invoice_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    total_expected = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"), ("partial", "Partially Paid"),
            ("paid", "Fully Paid"), ("overpaid", "Overpaid"), ("waived", "Waived"),
        ],
        default="pending",
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "academic_year", "term")
        ordering = ["-academic_year__year", "-term__number"]

    def __str__(self):
        return f"{self.invoice_number} — {self.student}"

    @property
    def balance(self):
        return self.total_expected - self.total_paid - self.discount

    @property
    def is_cleared(self):
        return self.balance <= 0


class FeeInvoiceItem(models.Model):
    invoice = models.ForeignKey(FeeInvoice, on_delete=models.CASCADE, related_name="items")
    category = models.ForeignKey(FeeCategory, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.invoice.invoice_number} — {self.description}"


class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice = models.ForeignKey(FeeInvoice, on_delete=models.CASCADE, related_name="payments")
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="payments")
    receipt_number = models.CharField(max_length=30, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_date = models.DateTimeField()
    method = models.CharField(
        max_length=20,
        choices=[
            ("mpesa", "M-Pesa"), ("cash", "Cash"), ("bank", "Bank Transfer"),
            ("cheque", "Cheque"), ("bursary", "Bursary/Scholarship"),
        ],
        default="mpesa",
    )
    mpesa_transaction_id = models.CharField(max_length=50, blank=True)
    mpesa_phone = models.CharField(max_length=20, blank=True)
    mpesa_paybill = models.CharField(max_length=20, blank=True)
    mpesa_account_ref = models.CharField(max_length=50, blank=True)
    mpesa_raw_callback = models.JSONField(null=True, blank=True)
    mpesa_checkout_request_id = models.CharField(max_length=100, blank=True)
    mpesa_status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "STK Push Sent"), ("confirmed", "Payment Confirmed"),
            ("failed", "Payment Failed"), ("cancelled", "Cancelled"), ("na", "Not Applicable"),
        ],
        default="na",
    )
    bank_reference = models.CharField(max_length=100, blank=True)
    received_by = models.ForeignKey("accounts.User", on_delete=models.SET_NULL, null=True, blank=True,
        related_name="received_payments")
    notes = models.TextField(blank=True)
    is_reversed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-payment_date"]

    def __str__(self):
        return f"{self.receipt_number} — KES {self.amount:,.0f}"


class MPesaTransaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    school = models.ForeignKey("schools.School", on_delete=models.CASCADE, related_name="mpesa_transactions")
    phone_number = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=50)
    description = models.CharField(max_length=200, blank=True)
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_description = models.CharField(max_length=300, blank=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    transaction_date = models.CharField(max_length=20, blank=True)
    raw_callback = models.JSONField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ("initiated", "STK Push Initiated"), ("pending", "Waiting for User"),
            ("success", "Successful"), ("failed", "Failed"), ("timeout", "Timed Out"),
        ],
        default="initiated",
    )
    linked_payment = models.OneToOneField(Payment, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="mpesa_log")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"M-Pesa: {self.phone_number} — KES {self.amount} — {self.status}"