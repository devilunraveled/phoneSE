import 'package:flutter/material.dart';

class AddAccountDialog extends StatelessWidget {
  final TextEditingController controller;
  final String? selectedAccount;
  final List<String> accounts;

  const AddAccountDialog({super.key, required this.controller, this.selectedAccount, required this.accounts});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Add New Account'),
      content: TextField(
        controller: controller,
        decoration: InputDecoration(labelText: 'Account Name'),
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
            // Add the new account logic here
            Navigator.pop(context);
          },
          child: Text('Add'),
        ),
      ],
    );
  }
}