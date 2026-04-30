import React, { useState } from "react";
import { auth } from "../firebase";
import {
  RecaptchaVerifier,
  signInWithPhoneNumber
} from "firebase/auth";

export default function PhoneOTP() {

  const [phone, setPhone] = useState("");
  const [otp, setOtp] = useState("");
  const [confirmation, setConfirmation] = useState(null);

  // Send OTP
  const sendOTP = async () => {

    window.recaptchaVerifier =
      new RecaptchaVerifier(auth, "recaptcha", {
        size: "invisible",
      });

    const result = await signInWithPhoneNumber(
      auth,
      phone,
      window.recaptchaVerifier
    );

    setConfirmation(result);
    alert("SMS OTP Sent ✅");
  };

  // Verify OTP
  const verifyOTP = async () => {
    await confirmation.confirm(otp);
    alert("Phone Verified 🎉");
  };

  return (
    <div>
      <h3>Phone OTP</h3>

      <input
        placeholder="+919999999999"
        onChange={(e)=>setPhone(e.target.value)}
      />

      <button onClick={sendOTP}>Send OTP</button>

      <input
        placeholder="Enter OTP"
        onChange={(e)=>setOtp(e.target.value)}
      />

      <button onClick={verifyOTP}>Verify OTP</button>

      <div id="recaptcha"></div>
    </div>
  );
}
