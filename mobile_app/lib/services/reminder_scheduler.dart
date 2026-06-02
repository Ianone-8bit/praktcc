import 'package:flutter/foundation.dart';

import '../models/patient.dart';
import '../models/reminder.dart';
import 'notification_service.dart';
import 'patient_service.dart';
import 'reminder_service.dart';

class ReminderScheduler {
  static final PatientService _patientService = PatientService();
  static final ReminderService _reminderService = ReminderService();

  static Future<void> syncAll() async {
    if (kIsWeb) return;

    try {
      final patients = await _patientService.getAll(limit: 200);
      final reminders = <Reminder>[];

      for (final Patient patient in patients) {
        final list = await _reminderService.getByPatient(patient.id);
        reminders.addAll(list);
      }

      if (reminders.isEmpty) return;

      await NotificationService.cancelAll();

      for (final reminder in reminders) {
        if (!reminder.isActive) continue;
        final patientName = reminder.patientName ?? 'Pasien';
        final medicationName = reminder.medicationName ?? 'Obat';

        for (final day in reminder.daysOfWeek) {
          await NotificationService.scheduleWeeklyReminder(
            reminderId: reminder.id,
            dayKey: day,
            time: reminder.timeShort,
            patientName: patientName,
            medicationName: medicationName,
          );
        }
      }
    } catch (_) {
      // Ignore scheduler errors to avoid blocking the UI.
    }
  }
}
