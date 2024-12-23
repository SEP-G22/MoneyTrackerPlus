from models.transaction import TransactionCategory 


perdifinedCategories = {
            "Allowance": TransactionCategory(category="Allowance", type="Income"),
            "Bonus": TransactionCategory(category="Bonus", type="Income"),
            "Clothes": TransactionCategory(category="Clothes", type="Expense"),
            "Education": TransactionCategory(category="Education", type="Expense"),
            "Entertainment": TransactionCategory(category="Entertainment", type="Expense"),
            "Food & Drinks": TransactionCategory(category="Food & Drinks", type="Expense"),
            "Housing & Utilities": TransactionCategory(category="Housing & Utilities", type="Expense"),
            "Personal": TransactionCategory(category="Personal", type="Expense"),
            "Salary": TransactionCategory(category="Salary", type="Income"),
            "Transportation": TransactionCategory(category="Transportation", type="Expense"),
        }

class getCategories():
    
    def setUp(self):
        categories = TransactionCategory.predefined_categories().values()
        return categories