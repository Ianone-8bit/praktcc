# Notifications (Option A - Local Only)

This project uses local scheduling for mobile and in-tab notifications for web.
There is no push notification service (Firebase/FCM) in this option.

## Web (React)
- Notifications only work while the tab is open.
- Open the Reminders page and enable browser notifications.
- Create a reminder scheduled 1-2 minutes ahead and keep the tab open.

## Mobile (Flutter - Android)
- Notifications are scheduled locally on the device.
- Make sure these are enabled:
  - App notifications: Settings > Apps > ObatLansia > Notifications > Allow
  - Alarms & reminders: Settings > Apps > Special app access > Alarms & reminders > Allow
  - Battery: Settings > Apps > ObatLansia > Battery saver > No restrictions
  - Autostart: Settings > Apps > ObatLansia > Autostart > ON
- Use the Reminders screen > Tes Jadwal to verify.

## Common Issues
- Closing the web tab stops web notifications.
- Force closing the mobile app may stop scheduled alarms until reopened.
- Flutter Web does not support local notifications.

## Next Upgrade (Optional)
For full sync across web and mobile, add a push notification service (FCM).
