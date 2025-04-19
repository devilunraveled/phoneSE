import 'package:flutter/material.dart';

import 'package:phone_se_app/screens/add_account.dart';

class CategoryField extends StatelessWidget {
  final TextEditingController controller;
  final String? selectedCategory;

  final List<String> categories;

  const CategoryField({super.key, required this.controller, this.selectedCategory, required this.categories});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: 'Category'),
      items: [
        DropdownMenuItem(value: '1', child: Text(categories[0])),
        DropdownMenuItem(value: '2', child: Text(categories[1])),
        DropdownMenuItem(value: '3', child: Text(categories[2])),
        DropdownMenuItem(value: '0', child: Text('Add New Category')),
      ],
      onChanged: (value) {
        if (value == 'Add New Category') {
          // Show dialog to add new category
          showDialog(
            context: context,
            builder: (context) {
              return AlertDialog(
                title: Text('Add New Category'),
                content: TextField(
                  controller: controller,
                  decoration: InputDecoration(labelText: 'Category Name'),
                ),
                actions: [
                  TextButton(
                    onPressed: () {
                      Navigator.pop(context);
                    },
                    child: Text('Cancel'),
                  ),
                  TextButton(
                    onPressed: () {
                      // Add the new category logic here
                      Navigator.pop(context);
                    },
                    child: Text('Add'),
                  ),
                ],
              );
            },
          );
        } else {
          controller.text = categories[int.parse(value!) - 1];
        }
      },
    );
  }
}

class AccountField extends StatelessWidget {
  final TextEditingController controller;
  final String? selectedAccount;

  final List<String> accounts;

  const AccountField({super.key, required this.controller, this.selectedAccount, required this.accounts});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: 'Account'),
      items: [
        DropdownMenuItem(value: '1', child: Text(accounts[0])),
        DropdownMenuItem(value: '2', child: Text(accounts[1])),
        DropdownMenuItem(value: '0', child: Text('Add New Account')),
      ],
      onChanged: (value) {
        if (value == 'Add New Account') {
          // Show dialog to add new account
          showDialog(
            context: context,
            builder: (context) {
              return AddAccountDialog(
                controller: controller,
                selectedAccount: selectedAccount,
                accounts: accounts,
              );
            },
          );
        } else {
          controller.text = accounts[int.parse(value!) - 1];
        }
      },
    );
  }
}

class ExpenseLogScreen extends StatelessWidget {
  final TextEditingController amountController = TextEditingController();
  final TextEditingController categoryController = TextEditingController();
  final TextEditingController accountController = TextEditingController();

  List<String> categories = ['Food', 'Transport', 'Bills'];
  List<String> accounts = ['Account 1', 'Account 2'];

  ExpenseLogScreen({super.key, this.amount});

  final String? amount;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Log Expense')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: amountController..text = amount ?? '',
              decoration: InputDecoration(labelText: 'Amount'),
              keyboardType: TextInputType.number,
            ),
            CategoryField(controller: categoryController, categories: categories),
            AccountField(controller: accountController, accounts: accounts),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Save Expense'),
            ),
          ],
        ),
      ),
    );
  }
}