import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/screens/add_account.dart';
import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class AccountItem {
  final int id;
  final String name;
  final double balance;
  final String currency;

  AccountItem({required this.id, required this.name, required this.balance, required this.currency});

  Widget buildAccountItem(BuildContext context, Function updateAccounts) {
    return Card(
      child: InkWell(
        onTap: () {
          // Navigate to account details screen
          print('Navigate to account details screen for account ID: $id');
        },
        child: ListTile(
          title: Text(name),
          subtitle: Text('Balance: $balance $currency'),
        ),
      )
    );
  }
}

class AddAccountItem {
  Widget buildAddAccountItem(BuildContext context, Function updateAccounts) {
    return Card(
      child: InkWell(
        onTap: () {
          // Show dialog to add new account
          showDialog(
            context: context,
            builder: (context) {
              return AddAccountDialog(updateAccounts: updateAccounts);
            },
          );
        },
        child: ListTile(
          title: Text('Add Account'),
          subtitle: Text('Click to add a new account'),
        ),
      )
    );
  }
}

class AccountsScreen extends StatefulWidget {
  const AccountsScreen({super.key});

  @override
  _AccountsScreenState createState() => _AccountsScreenState();
}

class _AccountsScreenState extends State<AccountsScreen> {
  List<AccountItem> accounts = [];

  void updateAccounts() {
    storage.read(key: 'token').then((token) {
      http.get(Uri.parse('${constants.apiUrl}/api/account/getUserAccounts/$token'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> responseBody = json.decode(response.body)['accounts'];
          setState(() {
            accounts = responseBody.map((account) => AccountItem(
              id: account['id'],
              name: account['name'],
              balance: account['balance'],
              currency: account['currency'],
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
  void initState() {
    super.initState();
    updateAccounts();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Accounts')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Accounts', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: accounts.length + 1,
                itemBuilder: (context, index) {
                  if (index == accounts.length) {
                    return AddAccountItem().buildAddAccountItem(context, updateAccounts);
                  }
                  return accounts[index].buildAccountItem(context, updateAccounts);
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}