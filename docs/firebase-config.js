/* Ultra Deep Field: Firebase settings (Firebase console → Project settings → Your apps → UDF web).
   These are meant to be public; the security rules (firestore.rules) are what protect the data. */
window.UDF_FIREBASE = {
  apiKey: "AIzaSyBK7Nz8ib6UybEINO05g0Vsr-UwiVwnkek",
  authDomain: "udf-ultra-deep-field.firebaseapp.com",
  databaseURL: "https://udf-ultra-deep-field-default-rtdb.firebaseio.com",
  projectId: "udf-ultra-deep-field",
  storageBucket: "udf-ultra-deep-field.firebasestorage.app",
  messagingSenderId: "1045530344643",
  appId: "1:1045530344643:web:dcc982633b8eb138273676",

  /* The game owner's Firebase user id (Authentication → Users → User UID). Unlocks owner perks and reading feedback. */
  ownerUids: []
};
