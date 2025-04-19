import 'package:flutter/material.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:http/http.dart' as http;
import 'dart:convert';

import 'package:phone_se_app/screens/sign_up.dart';
import 'package:phone_se_app/screens/dashboard.dart';
import 'package:phone_se_app/constants.dart' as constants;

final storage = FlutterSecureStorage();

class LoginScreen extends StatelessWidget {
  final TextEditingController phoneNoController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();

  LoginScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            TextField(controller: phoneNoController, decoration: InputDecoration(labelText: 'Phone Number')),
            TextField(controller: passwordController, decoration: InputDecoration(labelText: 'Password'), obscureText: true),
            ElevatedButton(
              onPressed: () {
                // Call the login API
                final String phoneNo = phoneNoController.text;
                final String password = passwordController.text;
                final String url = '${constants.apiUrl}/api/user/login';
                final Map<String, String> headers = {
                  'Content-Type': 'application/json',
                };
                final Map<String, String> body = {
                  'phoneNumber': phoneNo,
                  'password': password,
                };
                http.post(Uri.parse(url), headers: headers, body: json.encode(body)).then((response) {
                  String token = '';
                  if (response.statusCode == 200) {
                    // Parse the response body
                    final Map<String, dynamic> responseBody = json.decode(response.body);
                    token = responseBody['token'].toString();
                    // Save the token in shared preferences or any other storage
                    storage.write(key: 'token', value: token);
                    // Navigate to the dashboard screen
                    // ignore: use_build_context_synchronously
                    Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => DashboardScreen()));
                  } else {
                    // Handle error
                    print('Login failed: ${response.body}');
                  }
                });
              },
              child: Text('Login'),
            ),
            TextButton(
              onPressed: () => Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => SignupScreen())),
              child: Text("Don't have an account? Sign up"),
            )
          ],
        ),
      ),
    );
  }
}