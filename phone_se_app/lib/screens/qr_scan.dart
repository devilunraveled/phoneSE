import 'dart:io';
import 'dart:math';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';
import 'package:flutter_upi_india/flutter_upi_india.dart';

import 'package:phone_se_app/screens/expense_log.dart';

class QRScanScreen extends StatefulWidget {
  const QRScanScreen({super.key});

  @override
  _QRScanScreenState createState() => _QRScanScreenState();
}

class _QRScanScreenState extends State<QRScanScreen> {
  String? _upiAddr;
  String? _amount;
  List<ApplicationMeta>? _apps;

  @override
  void initState() {
    super.initState();
    // initially empty UPI and amount
    _amount = (Random.secure().nextDouble() * 10).toStringAsFixed(2);
  }

  Future<void> _fetchUpiApps() async {
    // discover all installed and supported-only apps
    final apps = await UpiPay.getInstalledUpiApplications(
      statusType: UpiApplicationDiscoveryAppStatusType.all,
    );
    setState(() => _apps = apps);
  }

  Future<void> _startPayment(ApplicationMeta app) async {
    if (_upiAddr == null || _upiAddr!.split('@').length != 2) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Invalid UPI ID: $_upiAddr')),
      );
      return;
    }
    final txRef = Random.secure().nextInt(1 << 32).toString();
    if (kDebugMode) print('TxRef: $txRef');

    // print all the details
    if (kDebugMode) {
      print('UPI ID: $_upiAddr');
      print('Amount: $_amount');
      print('App: ${app.upiApplication}');
    }

    final response = await UpiPay.initiateTransaction(
      amount: _amount!,
      app: app.upiApplication,
      receiverName: 'Merchant',
      receiverUpiAddress: _upiAddr!,
      transactionRef: txRef,
      transactionNote: 'Payment via phoneSE',
    );

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Status: ${response.status}')),
    );
    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => ExpenseLogScreen(amount:double.tryParse(_amount!))));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Scan QR & Pay')),
      body: Column(
        children: [
          Expanded(
            flex: 2,
            child: MobileScanner(
              onDetect: (capture) {
                final raw = capture.barcodes.first.rawValue ?? '';
                if (raw.isNotEmpty) {
                  // upi address is in the format 'upi://pay?pa=upi_id&<blahblah>
                  // so we need to extract the upi_id from the raw string
                  final uri = Uri.parse(raw);
                  final upiId = uri.queryParameters['pa'];
                  if (upiId == null) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(content: Text('Invalid UPI QR code')),
                    );
                    return;
                  }
                  final amount = uri.queryParameters['am'];
                  if (amount != null) {
                    // set the amount to the amount in the QR code
                    _amount = amount;
                  }
                  else {
                    _amount = "0.00";
                  }

                  // set the upi address
                  _upiAddr = upiId;
                  _fetchUpiApps();
                }
              },
            ),
          ),
          if (_upiAddr != null) ...[
            Padding(
              padding: const EdgeInsets.all(8.0),
              child: Text('UPI ID: $_upiAddr'),
            ),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      decoration: InputDecoration(labelText: 'Amount'),
                      keyboardType: TextInputType.number,
                      onChanged: (v) => _amount = v,
                      controller: TextEditingController(text: _amount),
                    ),
                  ),
                  IconButton(
                    icon: Icon(Icons.loop),
                    onPressed: () {
                      setState(() {
                        _amount = (Random.secure().nextDouble() * 10).toStringAsFixed(2);
                      });
                    },
                  )
                ],
              ),
            ),
            if (_apps != null)
              Expanded(
                flex: 1,
                child: GridView.count(
                  crossAxisCount: 4,
                  children: _apps!
                      .map((app) => InkWell(
                            onTap: () => _startPayment(app),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                app.iconImage(48),
                                Text(app.upiApplication.getAppName(), textAlign: TextAlign.center),
                              ],
                            ),
                          ))
                      .toList(),
                ),
              ),
          ] else ...[
            Expanded(
              flex: 1,
              child: Center(child: Text('Scan a QR code to begin payment')),
            ),
          ]
        ],
      ),
    );
  }
}

String? _validateUpiAddress(String value) {
  if (value.isEmpty) return 'UPI VPA is required.';
  if (value.split('@').length != 2) return 'Invalid UPI VPA';
  return null;
}
