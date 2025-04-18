import 'package:flutter/material.dart';

class ManualEntryScreen extends StatelessWidget {
  final TextEditingController amountController = TextEditingController();
  final TextEditingController categoryController = TextEditingController();

  ManualEntryScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Manual Expense Entry')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: amountController, decoration: InputDecoration(labelText: 'Amount'), keyboardType: TextInputType.number),
            TextField(controller: categoryController, decoration: InputDecoration(labelText: 'Category')),
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