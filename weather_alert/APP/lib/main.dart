import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'dart:async';
import 'package:geolocator/geolocator.dart';
import 'package:url_launcher/url_launcher.dart';

void main() {
  HttpOverrides.global = new MyHttpOverrides();
  runApp(MyApp());
}

class MyHttpOverrides extends HttpOverrides {
  @override
  HttpClient createHttpClient(SecurityContext? context) {
    return super.createHttpClient(context)
      ..badCertificateCallback = (X509Certificate cert, String host, int port) => true;
  }
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Early Warning System',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: MyHomePage(title: ''),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  String _result = 'No Alerts';
  Timer? _timer;

  Future<void> _getEarlyWarning() async {
    String _locationMessage = '';

    //Future<String> _getLocation(String _locationMessage) async {
    try {
      Position position = await Geolocator.getCurrentPosition(
          desiredAccuracy: LocationAccuracy.high);

      setState(() {
        _locationMessage =
        "lat=${position.latitude}&lng=${position.longitude}";
        // "Latitude: ${position.latitude}, Longitude: ${position.longitude}";
      });
    } catch (e) {
      print(e);
    }
    //}


    // String res = _getLocation(_locationMessage);

    final uri = Uri.parse('https://ec2-18-61-36-245.ap-south-2.compute.amazonaws.com/fetchData?$_locationMessage');
    final httpClient = HttpClient();
    final request = await httpClient.getUrl(uri);
    final response = await request.close();

    if (response.statusCode == 200) {
      final jsonResponse = await response.transform(utf8.decoder).join();
      final Map<String, dynamic> jsonMap = jsonDecode(jsonResponse);
      final String type = jsonMap['type'];
      final String area = jsonMap['area'];
      final String accuweather = jsonMap['accuweather'];
      final String earthquake = jsonMap['earthquake'];
      final String wildfire = jsonMap['wildfire'];

      String warning = '';
      String evacuationInstructions = '';

      if (type == 'Alert') {
        warning = ' No Alert';
        evacuationInstructions = '';
      } else if (accuweather != '') {
        warning = 'Floods Alert';
        evacuationInstructions = accuweather;
      } else if (earthquake != '') {
        warning = 'Earthquake Alert';
        evacuationInstructions = earthquake;
      } else if (wildfire != '') {
        warning = 'Wildfire Alert';
        evacuationInstructions = wildfire;
      }

      setState(() {
        _result = 'Warning: $warning\n';
      });

      print('JSON response: $jsonResponse');
    } else {
      setState(() {
        _result = 'Error: ${response.statusCode}';
      });
    }
  }

  @override
  void initState() {
    super.initState();
    _timer = Timer.periodic(Duration(minutes: 1), (timer) {
      _getEarlyWarning(); // Replace 'default_city' with your desired city
    });
  }

  @override
  void dispose() {
    _timer?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // Remove the app bar
      // body: Stack( // Use Stack to position elements

      // Use a single Container with full screen size
      body: Container(
        // Set decoration with the wallpaper image
        decoration: BoxDecoration(
          image: DecorationImage(
            image: AssetImage('images/Pinterest.jpg'), // Replace with your image path
            fit: BoxFit.cover, // Adjust image fit as needed
          ),
        ),
        child: Stack( // Use Stack to position other elements on top of the image
          children: [
            Positioned( // Position text at top left
              top: 35.0, // Adjust top padding
              left: 16.0, // Adjust left padding
              child: Text(
                "Early Warning System",
                style: TextStyle(
                  fontSize: 25, // Adjust font size as needed
                  fontWeight: FontWeight.bold,
                  color: Colors.white.withOpacity(0.9),
                ),
              ),
            ),
            Center( // Existing content
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: <Widget>[
                  Container(
                    width: MediaQuery.of(context).size.width * 0.8,
                    height: MediaQuery.of(context).size.height * 0.3,
                    padding: EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white54.withOpacity(0.8),
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.grey.withOpacity(0.5),
                          spreadRadius: 2,
                          blurRadius: 5,
                          offset: Offset(0, 3),
                        ),
                      ],
                    ),
                    child: Text(
                      _result,
                      style: const TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),
                  SizedBox(height: 20),
                ],
              ),
            ),
          ],
        ),
      ),
//      ),
    );
  }
}
