import 'package:flutter/material.dart';

import 'package:phone_se_app/screens/login.dart';

void main() {
  runApp(PhoneSEApp());
}

class PhoneSEApp extends StatelessWidget {
  const PhoneSEApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'phoneSE - Finance App',
      theme: ThemeData(primarySwatch: Colors.teal),
      home: LoginScreen(),
    );
  }
}
