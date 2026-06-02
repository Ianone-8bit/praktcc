import { getToken, onMessage } from 'firebase/messaging'
import { messaging } from './firebase'
import notificationService from './notificationService'

const VAPID_KEY = import.meta.env.VITE_FIREBASE_VAPID_KEY

export const initWebPush = async () => {
  if (!('serviceWorker' in navigator)) return null

  const permission = await Notification.requestPermission()
  if (permission !== 'granted') return null

  const registration = await navigator.serviceWorker.register('/firebase-messaging-sw.js')

  const token = await getToken(messaging, {
    vapidKey: VAPID_KEY,
    serviceWorkerRegistration: registration,
  })

  if (!token) return null

  const authToken = localStorage.getItem('token')
  if (authToken) {
    await fetch('/api/notifications/token', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${authToken}`,
      },
      body: JSON.stringify({ token, platform: 'web' }),
    })
  }

  onMessage(messaging, (payload) => {
    const title = payload.notification?.title || 'Waktunya Minum Obat!'
    const body = payload.notification?.body || 'Pengingat minum obat.'
    notificationService.showNotification(title, body, { tag: `fcm-${Date.now()}` })
  })

  return token
}
