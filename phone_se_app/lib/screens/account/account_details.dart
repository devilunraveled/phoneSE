import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class TransactionItem {
  final int id;
  final String name;
  final String description;
  final double amount;
  final String currency;
  final String timestamp;

  TransactionItem({
    required this.id,
    required this.name,
    required this.description,
    required this.amount,
    required this.currency,
    required this.timestamp,
  });
  Widget buildTransactionItem(BuildContext context, Function updateTransactions) {
    return Card(
      child: ListTile(
        title: Text('$name - $timestamp'),
        subtitle: Text(description),
        trailing: Text('$amount $currency'),
      ),
    );
  }
}

class AccountDetailsScreen extends StatefulWidget {
  final int accountId;
  final String accountName;
  final double accountBalance;
  final String accountCurrency;

  AccountDetailsScreen({
    super.key,
    required this.accountId,
    required this.accountName,
    required this.accountBalance,
    required this.accountCurrency,
  });

  @override
  _AccountDetailsScreenState createState() => _AccountDetailsScreenState();
}

class _AccountDetailsScreenState extends State<AccountDetailsScreen> {
  List<TransactionItem> transactions = [];

  void fetchTransactions() {
    storage.read(key: 'token').then((token) {
      http.get(
        Uri.parse('${constants.apiUrl}/api/transaction/getByAccount/${widget.accountId}'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          List<dynamic> data = jsonDecode(response.body)['transactions'];
          setState(() {
            transactions = data.map((item) {
              return TransactionItem(
                id: item['id'],
                name: item['name'],
                description: item['description'],
                amount: item['amount'],
                currency: item['currency'],
                timestamp: item['timestamp'],
              );
            }).toList();
          });
        } else {
          print('Failed to load transactions');
        }
      });
    });
  }

  @override
  void initState() {
    super.initState();
    // Fetch transactions for the account
    fetchTransactions();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.accountName),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Account Name: ${widget.accountName}', style: TextStyle(fontSize: 20)),
            Text('Balance: ${widget.accountBalance} ${widget.accountCurrency}', style: TextStyle(fontSize: 20)),
            SizedBox(height: 20),
            Text('Transactions:', style: TextStyle(fontSize: 18)),
            SizedBox(height: 10),
            Expanded(
              child: ListView.builder(
                itemCount: transactions.length,
                itemBuilder: (context, index) {
                  return transactions[index].buildTransactionItem(context, fetchTransactions);
                },
              ),
            ),
            // Add more account details here
          ],
        ),
      ),
    );
  }
}