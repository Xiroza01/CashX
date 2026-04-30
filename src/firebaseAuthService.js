import { 
  RecaptchaVerifier, 
  signInWithPhoneNumber,
  sendSignInLinkToEmail,
  isSignInWithEmailLink,
  signInWithEmailLink 
} from "firebase/auth";
import { auth } from "./firebase";


/**
 * Initialize reCAPTCHA for phone number verification.
 * @param {string} elementId - The ID of the HTML element where reCAPTCHA will be rendered (e.g., 'recaptcha-container')
 */
export const setupRecaptcha = (elementId) => {
  if (!window.recaptchaVerifier) {
    window.recaptchaVerifier = new RecaptchaVerifier(auth, elementId, {
      'size': 'invisible',
      'callback': (response) => {
        // reCAPTCHA solved, allow signInWithPhoneNumber.
        console.log("Recaptcha verified");
      },
      'expired-callback': () => {
        // Response expired. Ask user to solve reCAPTCHA again.
        console.warn("Recaptcha expired");
      }
    });
  }
};

/**
 * Send OTP via SMS to the provided phone number.
 * @param {string} phoneNumber - The phone number to send OTP to (format: +1234567890)
 */
export const sendSMSOTP = async (phoneNumber) => {
  const appVerifier = window.recaptchaVerifier;
  if (!appVerifier) {
    throw new Error("RecaptchaVerifier not initialized. Call setupRecaptcha first.");
  }
  
  try {
    const confirmationResult = await signInWithPhoneNumber(auth, phoneNumber, appVerifier);
    // Store confirmationResult in window object to be used for verification
    window.confirmationResult = confirmationResult;
    return confirmationResult;
  } catch (error) {
    console.error("Error sending SMS OTP:", error);
    // Reset recaptcha on error so user can try again
    if (window.recaptchaVerifier) {
      window.recaptchaVerifier.render().then(function(widgetId) {
        window.grecaptcha.reset(widgetId);
      });
    }
    throw error;
  }
};

/**
 * Verify the OTP code entered by the user.
 * @param {string} otpCode - The OTP code received via SMS
 */
export const verifySMSOTP = async (otpCode) => {
  if (!window.confirmationResult) {
    throw new Error("No pending OTP confirmation. Send OTP first.");
  }

  try {
    const result = await window.confirmationResult.confirm(otpCode);
    const user = result.user;
    return user;
  } catch (error) {
    console.error("Error verifying SMS OTP:", error);
    throw error;
  }
};


const actionCodeSettings = {
  // URL you want to redirect back to. Ensure it's whitelisted in Firebase Console.
  url: window.location.origin + '/auth/verify-email', 
  handleCodeInApp: true,
};

/**
 * Send an authentication link to the user's email.
 * @param {string} email - The user's email address
 */
export const sendEmailOTP = async (email) => {
  try {
    await sendSignInLinkToEmail(auth, email, actionCodeSettings);
    // Save the email locally so you don't need to ask the user for it again
    // if they open the link on the same device.
    window.localStorage.setItem('emailForSignIn', email);
    return true;
  } catch (error) {
    console.error("Error sending Email link:", error);
    throw error;
  }
};

/**
 * Verify the email link when the user is redirected back to the application.
 * @param {string} [email] - (Optional) Provide email if it's not stored in localStorage (e.g. cross-device)
 * @param {string} [windowUrl] - (Optional) Current window URL, defaults to window.location.href
 */
export const verifyEmailLink = async (email = null, windowUrl = window.location.href) => {
  if (isSignInWithEmailLink(auth, windowUrl)) {
    let emailToVerify = email || window.localStorage.getItem('emailForSignIn');
    
    if (!emailToVerify) {
      // User opened the link on a different device, ask for email
      throw new Error("Please provide email for verification");
    }
    
    try {
      const result = await signInWithEmailLink(auth, emailToVerify, windowUrl);
      // Clear email from storage after successful sign in
      window.localStorage.removeItem('emailForSignIn');
      return result.user;
    } catch (error) {
      console.error("Error signing in with email link:", error);
      throw error;
    }
  } else {
    throw new Error("Invalid email sign-in link.");
  }
};
