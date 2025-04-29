import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;
import 'package:phone_se_app/screens/add_category.dart';

final storage = FlutterSecureStorage();

class CategoryItem {
  final int id;
  final String name;
  final String description;

  CategoryItem({required this.id, required this.name, required this.description});

  Widget buildCategoryItem() {
    return Card(
      child: ListTile(
        title: Text(name),
        subtitle: Text(description),
      ),
    );
  }
}

class AddCategoryItem {
  Widget buildAddCategoryItem(BuildContext context, Function updateCategories) {
    return Card(
      child: InkWell(
        onTap: () {
          // Show dialog to add new category
          showDialog(
            context: context,
            builder: (context) {
              return AddCategoryDialog(updateCategories: updateCategories);
            },
          );
        },
        child: ListTile(
          title: Text('Add Category'),
          subtitle: Text('Click to add a new category'),
        ),
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
        Uri.parse('${constants.apiUrl}/api/category/getByUser'),
        headers: {
          'Authorization': '$token',
          'Content-Type': 'application/json',
        },
      ).then((response) {
        if (response.statusCode == 200) {
          final List<dynamic> data = jsonDecode(response.body)['categories'];
          setState(() {
            categories = data.map((category) => CategoryItem(
              id: category['id'],
              name: category['name'],
              description: category['description'],
            )).toList();
          });
        } else {
          print('Failed to load categories');
        }
      });
    });
  }

  @override
  void initState() {
    super.initState();
    updateCategories();
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
                itemCount: categories.length + 1,
                itemBuilder: (context, index) {
                  if (index == categories.length) {
                    return AddCategoryItem().buildAddCategoryItem(context, updateCategories);
                  }
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