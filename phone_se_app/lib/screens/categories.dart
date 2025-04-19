import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class CategoryItem {
  final String name;
  final String budgetName;
  final String amount;

  CategoryItem({required this.name, required this.budgetName, required this.amount});

  Widget buildCategoryItem() {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text('Budget: $budgetName\nAmount: $amount'),
      ),
    );
  }
}

class CategoriesScreen extends StatefulWidget {
  const CategoriesScreen({super.key});

  @override
  _CategoriesScreenState createState() => _CategoriesScreenState();
}

class _CategoriesScreenState extends State<CategoriesScreen> {
  List<CategoryItem> categories = [];

  void updateCategories() {
    storage.read(key:'token').then((token) {
      http.get(
        Uri.parse('${constants.apiUrl}/api/category/get/$token'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> data = jsonDecode(response.body)['categories'];
          setState(() {
            categories = data.map((category) => CategoryItem(
              name: category['name'],
              budgetName: category['budget_name'],
              amount: category['amount'].toString(),
            )).toList();
          });
        } else {
          print('Failed to load categories');
        }
      });
    });
  }

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