import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class BudgetItem {
  final List<String> categories;
  final List<String> accounts;
  final double amount;
  final String name;
  final String description;

  BudgetItem({required this.categories, required this.accounts, required this.amount, required this.name, required this.description});

  Widget buildBudgetItem() {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text('Description:$description\nAmount: $amount\nCategories: ${categories.join(', ')}\nAccounts: ${accounts.join(', ')}'),
      ),
    );
  }
}

class BudgetsScreen extends StatefulWidget {
  const BudgetsScreen({super.key});

  @override
  State<BudgetsScreen> createState() => _BudgetsScreenState();
}

class _BudgetsScreenState extends State<BudgetsScreen> {
  List<BudgetItem> budgets = [];

  void fetchBudgets() async {
    storage.read(key: 'token').then((token) async {
      final response = await http.get(
        Uri.parse('${constants.apiUrl}/budgets'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> responseBody = json.decode(response.body)['accounts'];
          setState(() {
            budgets = responseBody.map((budget) => BudgetItem(
              categories: List<String>.from(budget['categories']),
              accounts: List<String>.from(budget['accounts']),
              amount: budget['amount'],
              name: budget['name'],
              description: budget['description'],
            )).toList();
          });
        } else {
          // Handle error
          print('Failed to load accounts: ${response.body}');
        }
      });
    });
  }

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