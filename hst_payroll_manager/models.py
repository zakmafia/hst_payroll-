from django.db import models
import uuid
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
# Create your models here.


class Department(models.Model):
    STATUS_TYPE = (
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('inactive', 'Inactive')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    department_name = models.CharField(max_length=200)
    department_description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=200, choices=STATUS_TYPE, null=True, blank=True, default='active')

    def __str__(self):
        return self.department_name


class Position(models.Model):
    STATUS_TYPE = (
        ('active', 'Active'),
        ('pending', 'Pending'),
        ('inactive', 'Inactive')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    position_name = models.CharField(max_length=200)
    position_description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=200, choices=STATUS_TYPE, null=True, blank=True, default='active')

    def __str__(self):
        return self.position_name
    
class Tax(models.Model):
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    initial_range = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    final_range = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    tax_rate = models.DecimalField(max_digits=3, decimal_places=1, default=0, validators=PERCENTAGE_VALIDATOR)
    deduction = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    class Meta:
        verbose_name_plural = 'Taxes'
    
    def __str__(self):
        return str(self.tax_rate)
    
class Deduction(models.Model):
    deduction_name = models.CharField(max_length=200)
    is_taxable = models.BooleanField(default=False)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.deduction_name
    
class Allowance(models.Model):
    allowance_name = models.CharField(max_length=200)
    is_taxable = models.BooleanField(default=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    
    def __str__(self):
        return self.allowance_name


class Employee(models.Model):
    GENDER_TYPES = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    STATUS_TYPE = (
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    gender = models.CharField(
        max_length=200, choices=GENDER_TYPES, null=True, blank=True)
    email = models.EmailField(max_length=500, null=True, blank=True)
    birthday = models.DateField(
        help_text="Employee's birthday", null=True, blank=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True)
    account_number = models.PositiveBigIntegerField(null=True, blank=True)
    bank_name = models.CharField(max_length=500, null=True, blank=True)
    date_hired = models.DateField(
        help_text="Employee's date hired", null=True, blank=True)
    status = models.CharField(
        max_length=200, choices=STATUS_TYPE, null=True, blank=True, default='active')
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class EmployeeAllowance(models.Model):
    CURRENCY_TYPES = (
        ('etb', 'ETB'),
        ('usd', 'USD')
    )
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='employee_allowances')
    allowance = models.ForeignKey(Allowance, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_currency = models.CharField(
        max_length=200, choices=CURRENCY_TYPES, null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee} - {self.allowance}"

class EmployeeDeduction(models.Model):
    CURRENCY_TYPES = (
        ('etb', 'ETB'),
        ('usd', 'USD')
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deduction = models.ForeignKey(Deduction, on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    payment_currency = models.CharField(
        max_length=200, choices=CURRENCY_TYPES, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} - {self.deduction}"
    

# Employee Percentage Deduction
class EmployeePercentageDeduction(models.Model):
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deduction = models.ForeignKey(Deduction, on_delete=models.CASCADE)
    deduction_percentage = models.DecimalField(max_digits=3, decimal_places=1, validators=PERCENTAGE_VALIDATOR)
    
    def __str__(self):
        return f"{self.employee} - {self.deduction}"

class Salary(models.Model):
    CURRENCY_TYPES = (
        ('etb', 'ETB'),
        ('usd', 'USD')
    )
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]
    employee = models.OneToOneField(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    total_working_days = models.IntegerField(null=True, blank=True)
    
    # Gross salary is taxable
    gross_salary = models.DecimalField(default=0.0,
        max_digits=10, decimal_places=2, null=True, blank=True)
    
    payment_currency = models.CharField(
        max_length=200, choices=CURRENCY_TYPES, null=True, blank=True)
    
    # Foreign currency adjustment is taxable
    foreign_currency_adjustment = models.DecimalField(default=0.0,
        max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Pension input in percentage
    pension = models.DecimalField('Pension %', max_digits=3, decimal_places=1, default=7, validators=PERCENTAGE_VALIDATOR)
    
    # transport_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # Housing allowance is taxable
    # housing_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # Overtime payment is taxable
    # overtime_payment = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # medical_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # Annual bonus is taxable
    # annual_bonus = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # Performace allowance is taxable
    # performance_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # One-time signing bonus is taxable
    # one_time_signing_bonus = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # # Car allowance is taxable
    # car_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    # fuel_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Mobile allowance is taxable
    # mobile_allowance = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # School fee is taxable
    # school_fee = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # pension_contribution_employer = models.DecimalField('Pension contribution of the employer', default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # provident_fund_contribution_employer = models.DecimalField('Provident fund contribution of the employer', default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Holiday pay is taxable
    # holiday_pay = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    ################ Deductions ################
    
    # Credit card association contribution input using percentage
    # credit_association_contribution = models.DecimalField('Credit Association Contribution %', max_digits=3, decimal_places=1, default=2, validators=PERCENTAGE_VALIDATOR)
        
    # edir_contribution = models.DecimalField( default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Red cross contribution input using percentage
    # red_cross_contribution = models.DecimalField('Red Cross Contribution %',max_digits=3, decimal_places=1, default=0.5, validators=PERCENTAGE_VALIDATOR)
    
    # social_welfare_contribution = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    # loan_deduction_short_term = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    # loan_deduction_long_term = models.DecimalField(default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    # provident_fund_contribution = models.DecimalField('Provident fund contribution of the Employee', default=0.0,
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Total gross, net, tax, pension contribution deduction report
    
    # total_gross_salary = models.DecimalField(
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # total_tax = models.DecimalField(
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    pension_contribution = models.DecimalField('Total Pension contribution of the employee in amount', 
        max_digits=10, decimal_places=2, null=True, blank=True)
    
    created_on = models.DateTimeField(auto_now_add=True)
    # total_deduction = models.DecimalField(
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    # net_salary = models.DecimalField(
    #     max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Salaries' 
        
    # def calculate_total_gross_salary(self):
    #     total_gross_salary = self.gross_salary + self.foreign_currency_adjustment + self.transport_allowance + self.housing_allowance + self.overtime_payment + self.medical_allowance + self.annual_bonus + self.performance_allowance + self.one_time_signing_bonus + self.car_allowance + self.fuel_allowance + self.mobile_allowance + self.school_fee + self.provident_fund_contribution_employer + self.pension_contribution_employer + self.holiday_pay
        
    #     return total_gross_salary
        
    # def calculate_tax_on_component(self, component_amount, component_name):
    #     # Implement tax calculation logic for a specific component
    #     try:
    #         # Fetch the applicable tax rate based on the component amount
            
    #         # Check if the component_amount is None
    #         component_amount_value = component_amount if component_amount is not None else 0
            
    #         tax = Tax.objects.filter(initial_range__lte=component_amount_value, final_range__gte=component_amount_value).first()

    #         if tax:
    #             return ((component_amount_value * (tax.tax_rate / 100)) - tax.deduction)
    #         else:
    #             # If no matching tax range is found, use the default tax rate
    #             default_tax = Tax.objects.order_by('-final_range').first()
    #             return ((component_amount_value * (default_tax.tax_rate / 100)) - default_tax.deduction)
    #     except Tax.DoesNotExist:
    #         return 0
        
    # def calculate_tax(self):
    #     # Calculate tax for each taxable component separately
    #     tax_on_total_gross_salary = self.calculate_tax_on_component(self.calculate_total_gross_salary(), 'Total Gross Salary')

    #     return tax_on_total_gross_salary
    
    def calculate_pension_contribution(self):
        pension = self.gross_salary * (self.pension / 100) if self.pension is not None else 0
        return pension
    
    # def calculate_total_deduction(self):
    #     # Total deduction calculation logic here
    #     total_deduction = 0
    #     # Add up all the deduction fields
    #     total_deduction += (self.gross_salary * (self.credit_association_contribution / 100)) if self.credit_association_contribution is not None else 0
    #     total_deduction += self.edir_contribution if self.edir_contribution is not None else 0
    #     total_deduction += (self.gross_salary * (self.red_cross_contribution / 100)) if self.red_cross_contribution is not None else 0
    #     total_deduction += self.social_welfare_contribution if self.social_welfare_contribution is not None else 0
    #     total_deduction += self.loan_deduction_short_term if self.loan_deduction_short_term is not None else 0
    #     total_deduction += self.loan_deduction_long_term if self.loan_deduction_long_term is not None else 0
    #     total_deduction += self.provident_fund_contribution if self.provident_fund_contribution is not None else 0
        
    #     return total_deduction
    
    # def calculate_net_salary(self):
    #      # Net Salary logic here
    #      net_salary = self.calculate_total_gross_salary() - self.calculate_tax() - self.calculate_pension_contribution() - self.calculate_total_deduction()
         
    #      return net_salary
         
    
    def save(self, *args, **kwargs):
        # Before saving the Salary instance, calculate and update tax, pension, total deduction, and net salary fields
        super().save(*args, **kwargs)
        # self.total_gross_salary = self.calculate_total_gross_salary()
        # self.total_tax = self.calculate_tax()
        self.gross_salary = self.gross_salary + self.foreign_currency_adjustment
        self.pension_contribution = self.calculate_pension_contribution()
        # self.total_deduction = self.calculate_total_deduction()
        # self.net_salary = self.calculate_net_salary()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee}'s Salary"
    
    
class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)
    from_date = models.DateField('From Date', null=True, blank=True)
    to_date = models.DateField('To Date', null=True, blank=True)
    total_gross_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    total_tax = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    pension_contribution = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    total_deduction = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    net_salary = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.employee)
    
    
    

