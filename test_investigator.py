from ai_investigator import investigate_exception

exception = """
Transaction ID: TXN044
Issue: Missing Settlement
Order Amount: ₹4,500
Fee: ₹90
Expected Settlement: ₹4,410
Actual Settlement: ₹0
Difference: ₹4,410
Priority: HIGH
"""

result = investigate_exception(exception)

print(result)