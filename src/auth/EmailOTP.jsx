import { auth } from "../firebase";
import {
  sendSignInLinkToEmail,
  isSignInWithEmailLink,
  signInWithEmailLink
} from "firebase/auth";

const actionCodeSettings = {
  url: "http://localhost:3000",
  handleCodeInApp: true,
};

export const sendEmailOTP = async (email) => {

  await sendSignInLinkToEmail(
    auth,
    email,
    actionCodeSettings
  );

  localStorage.setItem("email", email);

  alert("Email OTP Sent ✅");
};

export const verifyEmailOTP = async () => {

  if (isSignInWithEmailLink(auth, window.location.href)) {

    const email = localStorage.getItem("email");

    await signInWithEmailLink(
      auth,
      email,
      window.location.href
    );

    alert("Email Verified 🎉");
  }
};
