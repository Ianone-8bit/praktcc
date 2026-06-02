/* eslint-disable no-undef */
importScripts('https://www.gstatic.com/firebasejs/10.13.1/firebase-app-compat.js')
importScripts('https://www.gstatic.com/firebasejs/10.13.1/firebase-messaging-compat.js')

firebase.initializeApp({
  apiKey: 'AIzaSyBUM6Tk5jwMbe-c8BrTDCG-_oTR_0ynVkA',
  authDomain: 'projecttcc-e3405.firebaseapp.com',
  projectId: 'projecttcc-e3405',
  storageBucket: 'projecttcc-e3405.firebasestorage.app',
  messagingSenderId: '1084640948044',
  appId: '1:1084640948044:web:9eb32bd5f842b83f4aa9e9',
})

const messaging = firebase.messaging()

messaging.onBackgroundMessage((payload) => {
  const title = payload.notification?.title || 'Waktunya Minum Obat!'
  const options = {
    body: payload.notification?.body || 'Pengingat minum obat.',
    icon: '/favicon.ico',
  }
  self.registration.showNotification(title, options)
})
