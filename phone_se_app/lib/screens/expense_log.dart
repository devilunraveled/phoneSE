import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;
import 'package:phone_se_app/screens/add_account.dart';

final storage = FlutterSecureStorage();

class CategoryField extends StatelessWidget {
  final TextEditingController controller;

  final List<DropdownMenuItem> categories;

  const CategoryField({super.key, required this.controller, required this.categories});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<dynamic>(
      decoration: InputDecoration(labelText: 'Category'),
      items: categories,
      onChanged: (value) {
        if (value == '0') {
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
          controller.text = categories[int.parse(value!) - 1].child.toString();
        }
      },
    );
  }
}

class AccountField extends StatelessWidget {
  final TextEditingController controller;

  final List<DropdownMenuItem> accounts;

  const AccountField({super.key, required this.controller,required this.accounts});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<dynamic>(
      decoration: InputDecoration(labelText: 'Account'),
      items: accounts,
      onChanged: (value) {
        if (value == '0') {
          // Show dialog to add new account
          showDialog(
            context: context,
            builder: (context) {
              return AddAccountDialog();
            },
          );
        } else {
          controller.text = accounts[int.parse(value!) - 1].child.toString();
        }
      },
    );
  }
}

class ExpenseLogScreen extends StatefulWidget {
  final double? amount;

  const ExpenseLogScreen({super.key, this.amount});

  @override
  _ExpenseLogScreenState createState() => _ExpenseLogScreenState();
}

class _ExpenseLogScreenState extends State<ExpenseLogScreen> {
  final TextEditingController nameController = TextEditingController();
  final TextEditingController descriptionController = TextEditingController();
  final TextEditingController amountController = TextEditingController();
  final TextEditingController categoryController = TextEditingController();
  final TextEditingController accountController = TextEditingController();

  List<DropdownMenuItem> categories = [];
  List<DropdownMenuItem> accounts = [];

  void fetchCategories() {
    storage.read(key: 'token').then((token) {
      http.get(
        Uri.parse('${constants.apiUrl}/api/getUserCategories/$token'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> data = jsonDecode(response.body)['categories'];
          setState(() {
            categories = data.map((category) => DropdownMenuItem(
              value: category['id'].toString(),
              child: Text(category['name']),
            )).toList();
            categories.add(DropdownMenuItem(value: '0', child: Text('Add New Category')));
          });
        } else {
          print('Failed to load categories');
        }
      });
    });
  }

  void fetchAccounts() {
    storage.read(key: 'token').then((token) {
      http.get(
        Uri.parse('${constants.apiUrl}/api/account/getUserAccounts'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> data = jsonDecode(response.body)['accounts'];
          setState(() {
            accounts = data.map((account) => DropdownMenuItem(
              value: account['id'].toString(),
              child: Text(account['name']),
            )).toList();
            accounts.add(DropdownMenuItem(value: '0', child: Text('Add New Account')));
          });
        } else {
          print('Failed to load accounts');
        }
      });
    });
  }

  @override
  void initState() {
    super.initState();
    fetchCategories();
    fetchAccounts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Log Expense')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(
              controller: amountController..text = widget.amount?.toString() ?? '',
              decoration: InputDecoration(labelText: 'Amount'),
              keyboardType: TextInputType.number,
            ),
            CategoryField(controller: categoryController, categories: categories),
            AccountField(controller: accountController, accounts: accounts),
            ElevatedButton(
              onPressed: () {
                storage.read(key: 'token').then((token) {
                  http.post(
                    Uri.parse('${constants.apiUrl}/api/transaction/create'),
                    headers: {
                      'Content-Type': 'application/json',
                      'Authorization': '$token',
                    },
                    body: jsonEncode({
                      'name': nameController.text,
                      'description': descriptionController.text,
                      'amount': double.tryParse(amountController.text) ?? 0.0,
                      'category_id': categoryController.text,
                      'account_id': accountController.text,
                    }),
                  ).then((response) {
                    if (response.statusCode == 200) {
                      // Successfully logged expense
                      print('Expense logged successfully');
                      // Optionally, you can navigate back or show a success message
                    } else {
                      // Handle error
                      print('Failed to log expense');
                    }
                  });
                });
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