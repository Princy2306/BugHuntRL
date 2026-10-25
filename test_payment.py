
from payment_system import process_payment

print("Normal payment:")
print(process_payment(100, "PAY001"))

print("\nZero payment:")
print(process_payment(0, "PAY002"))

print("\nNegative payment:")
print(process_payment(-10, "PAY003"))
