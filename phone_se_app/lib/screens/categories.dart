import 'package:flutter/material.dart';

class Category {
  final String name;
  final String budgetName;
  final String amount;

  Category({required this.name, required this.budgetName, required this.amount});

  Widget buildCategoryItem() {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text('Budget: $budgetName\nAmount: $amount'),
      ),
    );
  }
}

class CategoriesScreen extends StatelessWidget {
  final List<Category> categories = [
    Category(name: 'Food', budgetName: 'Monthly Budget', amount: '₹5000'),
    Category(name: 'Transport', budgetName: 'Weekly Budget', amount: '₹2000'),
    Category(name: 'Entertainment', budgetName: 'Monthly Budget', amount: '₹3000'),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Categories')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Text('Categories', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
            SizedBox(height: 16),
            Expanded(
              child: ListView.builder(
                itemCount: categories.length,
                itemBuilder: (context, index) {
                  return categories[index].buildCategoryItem();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}