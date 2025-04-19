import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class AccountItem {
  final String id;
  final String name;
  final String amount;
  final String budgetName;

  AccountItem({required this.id, required this.name, required this.amount, required this.budgetName});

  Widget buildAccountItem() {
    return Card(
      child: InkWell(
        onTap: () {
          // Handle account item tap
          if (id == '0') {
            // Navigate to add account screen
            print('Navigate to add account screen');
          } else {
            // Navigate to account details screen
            print('Navigate to account details screen for account ID: $id');
          }
        },
        child: ListTile(
          title: Text(name),
          subtitle: Text('Budget: $budgetName\nAmount: $amount'),
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
  late List<AccountItem> accounts;

  @override
  void initState() {
    super.initState();
    storage.read(key: 'token').then((token) {
      http.get(Uri.parse('${constants.apiUrl}/api/accounts/getUserAccounts'),
        headers: {
          'Authorization': 'Bearer $token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> responseBody = json.decode(response.body);
          setState(() {
            accounts = responseBody.map((account) => AccountItem(
              id: account['id'],
              name: account['name'],
              amount: account['amount'],
              budgetName: account['budgetName'],
            )).toList();
            accounts.add(AccountItem(
              id: '0',
              name: 'Add Account',
              amount: '',
              budgetName: '',
            ));
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
      appBar: AppBar(title: Text('Accounts')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Accounts', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: accounts.length,
                itemBuilder: (context, index) {
                  return accounts[index].buildAccountItem();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}