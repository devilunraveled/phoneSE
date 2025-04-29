import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;
import 'package:phone_se_app/screens/account/add_account.dart';
import 'package:phone_se_app/screens/category/add_category.dart';

final storage = FlutterSecureStorage();

class CategoryField extends StatelessWidget {
  final TextEditingController controller;
  final List<DropdownMenuItem<String>> categories;
  final Function fetchCategories;
  final Function setCategory;

  CategoryField({super.key, required this.controller, required this.categories, required this.fetchCategories, required this.setCategory});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: 'Category'),
      items: categories,
      onChanged: (value) {
        if (value == '0') {
          // Show dialog to add new category
          showDialog(
            context: context,
            builder: (context) {
              return AddCategoryDialog(updateCategories: fetchCategories);
            },
          );
          controller.text = '';
          setCategory(0);
        } else {
          controller.text = categories[int.parse(value!) - 1].child.toString();
          setCategory(int.parse(value));
        }
      },
    );
  }
}

class AccountField extends StatelessWidget {
  final TextEditingController controller;
  final List<DropdownMenuItem<String>> accounts;
  final Function fetchAccounts;
  final Function setAccount;

  AccountField({super.key, required this.controller, required this.accounts, required this.fetchAccounts, required this.setAccount});

  @override
  Widget build(BuildContext context) {
    return DropdownButtonFormField<String>(
      decoration: InputDecoration(labelText: 'Account'),
      items: accounts,
      onChanged: (value) {
        if (value == '0') {
          // Show dialog to add new account
          showDialog(
            context: context,
            builder: (context) {
              return AddAccountDialog(updateAccounts: fetchAccounts);
            },
          );
          controller.text = '';
          setAccount(0);
        } else {
          controller.text = accounts[int.parse(value!) - 1].child.toString();
          setAccount(int.parse(value));
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
  final TextEditingController currencyController = TextEditingController();
  final TextEditingController categoryController = TextEditingController();
  final TextEditingController accountController = TextEditingController();

  List<DropdownMenuItem<String>> categories = [];
  List<DropdownMenuItem<String>> accounts = [];

  int selectedCategory = 0;
  int selectedAccount = 0;

  void fetchCategories() {
    storage.read(key: 'token').then((token) {
      http.get(
        Uri.parse('${constants.apiUrl}/api/category/getByUser'),
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
        Uri.parse('${constants.apiUrl}/api/account/getByUser'),
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

  void setCategory(int category) {
    setState(() {
      selectedCategory = category;
    });
  }
  void setAccount(int account) {
    setState(() {
      selectedAccount = account;
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
              controller: nameController,
              decoration: InputDecoration(labelText: 'Name'),
            ),
            TextField(
              controller: descriptionController,
              decoration: InputDecoration(labelText: 'Description'),
            ),
            TextField(
              controller: amountController..text = widget.amount?.toString() ?? '',
              decoration: InputDecoration(labelText: 'Amount'),
              keyboardType: TextInputType.number,
            ),
            TextField(
              controller: currencyController,
              decoration: InputDecoration(labelText: 'Currency'),
              // set default to INR
              
            ),
            CategoryField(controller: categoryController, categories: categories, fetchCategories: fetchCategories, setCategory: setCategory),
            AccountField(controller: accountController, accounts: accounts, fetchAccounts: fetchAccounts, setAccount: setAccount),
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
                      'currency': currencyController.text,
                      'payer': selectedAccount,
                      'payee': selectedAccount,
                      'categories': [selectedCategory],
                    }),
                  ).then((response) {
                    if (response.statusCode == 200) {
                      // Successfully logged expense
                      print('Expense logged successfully');
                      Navigator.pop(context);
                    } else {
                      // Handle error
                      print('Failed to log expense');
                    }
                  });
                });
              },
              child: Text('Save Expense'),
            ),
          ],
        ),
      ),
    );
  }
}