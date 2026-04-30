// src/firebase.js

import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Firebase config
const firebaseConfig = {
  apiKey: "AIzaSyBmSPIy1sekPNUdlHWOy-RZIG3NB211JXE",
  authDomain: "cashx-4e8ce.firebaseapp.com",
  projectId: "cashx-4e8ce",
  storageBucket: "cashx-4e8ce.firebasestorage.app",
  messagingSenderId: "687486924161",
  appId: "1:687486924161:web:8faaa8c98b157787536480",
  measurementId: "G-4YCFN1TCE2"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Auth
export const auth = getAuth(app);

export default app;