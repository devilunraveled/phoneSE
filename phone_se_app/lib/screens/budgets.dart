import 'package:flutter/material.dart';

class BudgetItem {
  final List<String> categories;
  final List<String> accounts;
  final double amount;
  final String budgetName;

  BudgetItem({required this.categories, required this.accounts, required this.amount, required this.budgetName});

  Widget buildBudgetItem() {
    return Card(
      child: ListTile(
        title: Text(budgetName),
        subtitle: Text('Amount: $amount\nCategories: ${categories.join(', ')}\nAccounts: ${accounts.join(', ')}'),
      ),
    );
  }
}

class BudgetsScreen extends StatelessWidget {
  final List<BudgetItem> budgets = [
    BudgetItem(categories: ['Food', 'Transport'], accounts: ['Cash', 'Credit Card'], amount: 500.0, budgetName: 'Monthly Budget'),
    BudgetItem(categories: ['Entertainment'], accounts: ['Debit Card'], amount: 200.0, budgetName: 'Weekly Budget'),
  ];

  BudgetsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Budgets')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Budgets', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: budgets.length,
                itemBuilder: (context, index) {
                  return budgets[index].buildBudgetItem();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}