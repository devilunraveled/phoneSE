import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class AddAccountDialog extends StatelessWidget {
  final TextEditingController controller = TextEditingController();
  final TextEditingController balanceController = TextEditingController();
  final TextEditingController descriptionController = TextEditingController();
  final Function? updateAccounts;

  AddAccountDialog({super.key, this.updateAccounts});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Add New Account'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          TextField(
            controller: controller,
            decoration: InputDecoration(labelText: 'Account Name'),
          ),
          TextField(
            controller: balanceController,
            decoration: InputDecoration(labelText: 'Initial Balance'),
            keyboardType: TextInputType.number,
          ),
          TextField(
            controller: descriptionController,
            decoration: InputDecoration(labelText: 'Description'),
          ),
        ],
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
            String accountName = controller.text;
            if (accountName.isNotEmpty) {
              // Call API to add account
              storage.read(key: 'token').then((token) {
                http.post(
                  Uri.parse('${constants.apiUrl}/api/account/create/$token'),
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer $token',
                  },
                  body: jsonEncode({
                    'name': accountName,
                    'balance': double.tryParse(balanceController.text) ?? 0.0,  
                  }),
                ).then((response) {
                  if (response.statusCode == 200) {
                    // Successfully added account
                    print('Account added successfully');
                    // Update the accounts list
                    updateAccounts!();
                  } else {
                    // Handle error
                    print('Failed to add account');
                  }
                });
              });
            } else {
              // Show error message
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Account name cannot be empty')),
              );
            }
            // Close the dialog
            Navigator.pop(context);
          },
          child: Text('Add'),
        ),
      ],
    );
  }
}