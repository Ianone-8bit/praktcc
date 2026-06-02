import 'package:firebase_messaging/firebase_messaging.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'notification_service.dart';
import 'api_client.dart';
import '../config/api_config.dart';

class PushNotificationService {
  static final FirebaseMessaging _messaging = FirebaseMessaging.instance;

  static Future<void> initialize() async {
    await _messaging.requestPermission();

    FirebaseMessaging.onMessage.listen((message) {
      final title = message.notification?.title ?? 'Waktunya Minum Obat!';
      final body = message.notification?.body ?? 'Pengingat minum obat.';
      NotificationService.showNotification(
        id: DateTime.now().millisecondsSinceEpoch % 100000,
        title: title,
        body: body,
      );
    });
  }

  static Future<void> registerToken() async {
    final prefs = await SharedPreferences.getInstance();
    final token = prefs.getString('token');
    if (token == null || token.isEmpty) return;

    final fcmToken = await _messaging.getToken();
    if (fcmToken == null || fcmToken.isEmpty) return;

    final client = ApiClient(ApiConfig.medBaseUrl);
    await client.post('/notifications/token', body: {
      'token': fcmToken,
      'platform': 'android',
    });
  }
}
