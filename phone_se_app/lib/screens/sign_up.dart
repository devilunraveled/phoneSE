import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/screens/dashboard.dart';
import 'package:phone_se_app/constants.dart' as constants;

class SignupScreen extends StatelessWidget {
  final TextEditingController firstNameController = TextEditingController();
  final TextEditingController lastNameController = TextEditingController();
  final TextEditingController callingCodeController = TextEditingController();
  final TextEditingController phoneNoController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  SignupScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Sign Up')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: firstNameController, decoration: InputDecoration(labelText: 'First Name')),
            TextField(controller: lastNameController, decoration: InputDecoration(labelText: 'Last Name')),
            TextField(controller: callingCodeController, decoration: InputDecoration(labelText: 'Country Code')),
            TextField(controller: phoneNoController, decoration: InputDecoration(labelText: 'Phone Number')),
            TextField(controller: passwordController, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
            ElevatedButton(
              onPressed: () {
                // Call the signup API
                final String firstName = firstNameController.text;
                final String lastName = lastNameController.text;
                final String callingCode = callingCodeController.text;
                final String phoneNo = phoneNoController.text;
                final String password = passwordController.text;
                final String url = '${constants.apiUrl}/api/user/register';
                final Map<String, String> headers = {
                  'Content-Type': 'application/json',
                };
                final Map<String, String> body = {
                  'firstName': firstName,
                  'lastName': lastName,
                  'callingCode': callingCode,
                  'phoneNumber': phoneNo,
                  'password': password,
                };
                http.post(Uri.parse(url), headers: headers, body: json.encode(body)).then((response) {
                  String token = '';
                  if (response.statusCode == 201) {
                    // Parse the response body
                    final Map<String, dynamic> responseBody = json.decode(response.body);
                    token = responseBody['token'];
                    // Save the token in shared preferences or any other storage
                    print('Token: $token');
                    // Navigate to the dashboard screen
                    // ignore: use_build_context_synchronously
                    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => DashboardScreen()));
                  } else {
                    // Handle error
                    print('Signup failed: ${response.body}');
                  }
                });
              },
              child: Text('Create Account'),
            ),
          ],
        ),
      ),
    );
  }
}