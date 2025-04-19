import 'package:flutter/material.dart';

class PaymentScreen extends StatelessWidget {
  final TextEditingController merchantController = TextEditingController();
  final TextEditingController amountController = TextEditingController();

  PaymentScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Make Payment')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: merchantController, decoration: InputDecoration(labelText: 'Merchant ID')),
            TextField(controller: amountController, decoration: InputDecoration(labelText: 'Amount'), keyboardType: TextInputType.number),
            ElevatedButton(
              onPressed: () {
                Navigator.pop(context);
              },
              child: Text('Pay Now'),
            ),
          ],
        ),
      ),
    );
  }
}