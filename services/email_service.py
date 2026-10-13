import resend
from resend.exceptions import ResendError

from brain.config import ENVIRONMENT_VARIABLES
from constants.server_codes import INTERNAL_SERVER_ERROR, SUCCESS


def send_verification_email(email: str, otp: str) -> dict:
    try:
        resend.api_key = ENVIRONMENT_VARIABLES.get("RESEND_API_KEY")
        r = resend.Emails.send({
        "from": "onboarding@codevaults.org",
        "to": email,
        "subject": "Please verify your email address for Ticketer",
        "html": f"<p><strong>Your verification OTP is <h1>{otp}</h1></strong></p>"
        })
        return {
            "status_code": SUCCESS,
            "message": f"Verification email sent successfully to {email}",
        }
    except ResendError as e:
        return {
            "status_code": INTERNAL_SERVER_ERROR,
            "message": f"Error sending email: {str(e)}"
        }