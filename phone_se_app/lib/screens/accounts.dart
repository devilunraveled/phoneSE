import 'package:flutter/material.dart';

class AccountItem {
  final String name;
  final String amount;

  AccountItem({required this.name, required this.amount});
}

class AccountsScreen extends StatelessWidget {
  final List<AccountItem> accounts = [
    AccountItem(name: 'Account 1', amount: '₹1000'),
    AccountItem(name: 'Account 2', amount: '₹2000'),
    AccountItem(name: 'Account 3', amount: '₹3000'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Accounts')),
      body: ListView.builder(
        itemCount: accounts.length,
        itemBuilder: (context, index) {
          return ListTile(
            title: Text(accounts[index].name),
            subtitle: Text(accounts[index].amount),
          );
        },
      ),
    );
  }
}