import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class AddCategoryDialog extends StatelessWidget {
  final TextEditingController controller = TextEditingController();
  final TextEditingController descriptionController = TextEditingController();

  final Function? updateCategories;
  AddCategoryDialog({super.key, this.updateCategories});

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text('Add New Category'),
      content: TextField(
        controller: controller,
        decoration: InputDecoration(labelText: 'Category Name'),
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
            String categoryName = controller.text;
            String categoryDescription = descriptionController.text;
            if (categoryName.isNotEmpty) {
              // Call API to add category
              storage.read(key:'token').then((token) {
                http.post(
                  Uri.parse('${constants.apiUrl}/api/category/create'),
                  headers: {
                    'Content-Type': 'application/json',
                    'Authorization': '$token',
                  },
                  body: jsonEncode({
                    'name': categoryName,
                    'description': categoryDescription,
                  }),
                ).then((response) {
                  if (response.statusCode == 200) {
                    if (updateCategories != null) {
                      updateCategories!();
                    }
                    Navigator.pop(context);
                  } else {
                    print('Failed to add category');
                  }
                });
              });
            }
          },
          child: Text('Add'),
        ),
      ],
    );
  }
}