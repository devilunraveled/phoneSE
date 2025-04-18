import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

import 'package:phone_se_app/screens/manual_entry.dart';
import 'package:phone_se_app/screens/payment.dart';
import 'package:phone_se_app/screens/qr_scan.dart';

class SpendingChart extends StatelessWidget {
  const SpendingChart({super.key});

  @override
  Widget build(BuildContext context) {
    return PieChart(
      PieChartData(
        sections: [
          PieChartSectionData(value: 30, title: 'Food', color: Colors.blue),
          PieChartSectionData(value: 20, title: 'Transport', color: Colors.red),
          PieChartSectionData(value: 25, title: 'Bills', color: Colors.green),
          PieChartSectionData(value: 25, title: 'Others', color: Colors.orange),
        ],
      ),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Dashboard')),
      body: Column(
        children: [
          SizedBox(height: 200, child: SpendingChart()),
          ElevatedButton(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ManualEntryScreen())),
            child: Text('Add Expense Manually'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => QRScanScreen())),
            child: Text('Scan QR to Auto-Log'),
          ),
          ElevatedButton(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => PaymentScreen())),
            child: Text('Make Payment'),
          ),
        ],
      ),
    );
  }
}