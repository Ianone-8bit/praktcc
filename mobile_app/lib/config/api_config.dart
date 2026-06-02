// ============ FILE: mobile_app/lib/config/api_config.dart ============
import 'package:flutter/foundation.dart';

class ApiConfig {
  // Override via build flag: --dart-define=API_HOST=192.168.x.x
  static const String _envHost = String.fromEnvironment('API_HOST', defaultValue: '');

  static String get _baseHost {
    if (_envHost.isNotEmpty) return _envHost;
    if (kIsWeb) return 'localhost';
    if (defaultTargetPlatform == TargetPlatform.android) return '10.0.2.2';
    return '127.0.0.1';
  }

  static String get authBaseUrl => 'http://$_baseHost:8001/api/auth';
  static String get medBaseUrl => 'http://$_baseHost:8002/api';

  static const Duration timeout = Duration(seconds: 15);

  static Map<String, String> headers(String? token) {
    final h = <String, String>{
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    if (token != null && token.isNotEmpty) {
      h['Authorization'] = 'Bearer $token';
    }
    return h;
  }
}
