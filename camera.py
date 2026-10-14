import cv2
import numpy as np
from detection import AccidentDetectionModel
import os
import time
import winsound
import smtplib
from email.message import EmailMessage

font = cv2.FONT_HERSHEY_SIMPLEX


# 🔔 BUZZER
def play_buzzer():
    winsound.Beep(1000, 1500)


# 📧 EMAIL WITH IMAGE + DESCRIPTION
def send_email_with_image(image_path, source_type, source_name):
    # Credentials come from environment variables, never from the code
    sender_email = os.environ.get("ALERT_EMAIL_SENDER")
    receiver_email = os.environ.get("ALERT_EMAIL_RECEIVER")
    app_password = os.environ.get("ALERT_EMAIL_APP_PASSWORD")

    if not (sender_email and receiver_email and app_password):
        print("⚠️ Email not sent: set ALERT_EMAIL_SENDER, ALERT_EMAIL_RECEIVER and ALERT_EMAIL_APP_PASSWORD")
        return

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    body = f"""
🚨 Accident Detected!


Location  : {source_name}
Date & Time : {timestamp}

Please find the attached accident image for reference.
"""

    msg = EmailMessage()
    msg["Subject"] = "🚨 Accident Alert"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content(body)

    with open(image_path, "rb") as f:
        img_data = f.read()

    msg.add_attachment(
        img_data,
        maintype="image",
        subtype="jpeg",
        filename=os.path.basename(image_path)
    )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("📧 Email sent with description and image")


def startapplication():
    print("\nSelect Input Source:")
    print("1️⃣  Live Camera")
    print("2️⃣  Video File")

    choice = input("Enter choice (1 or 2): ").strip()
    cap = None

    # SOURCE DETAILS (ADDED)
    source_type = ""
    source_name = ""

    # CAMERA OPTION
    if choice == "1":
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        source_type = "Live Camera"
        source_name = "Camera 0"

    # VIDEO OPTION
    elif choice == "2":
        video_path = input("Enter full video path: ").strip().strip('"')

        if not os.path.exists(video_path):
            print("❌ Video file not found")
            return

        cap = cv2.VideoCapture(video_path)
        source_type = "Video File"
        source_name = os.path.basename(video_path)

    else:
        print("❌ Invalid choice")
        return

    if not cap.isOpened():
        print("❌ Cannot open source")
        return

    print("✅ Source opened successfully")

    # LOAD MODEL (UNCHANGED)
    model = AccidentDetectionModel("model.json", "model_weights.h5")
    print("✅ Model loaded")

    # ALERT CONTROL
    last_alert_time = 0
    ALERT_COOLDOWN = 120  # 2 minutes

    os.makedirs("accident_images", exist_ok=True)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        roi = cv2.resize(rgb, (250, 250))

        pred, prob = model.predict_accident(roi[np.newaxis, :, :])
        current_time = time.time()

        # 🔴 CORE ACCIDENT LOGIC (UNCHANGED)
        if pred == "Accident":
            confidence = round(prob[0][0] * 100, 2)

            if confidence > 80:
                cv2.rectangle(frame, (0, 0), (340, 40), (0, 0, 0), -1)
                cv2.putText(
                    frame,
                    f"{pred} {confidence}%",
                    (20, 30),
                    font,
                    1,
                    (0, 0, 255),
                    2
                )

                # 🚨 ALERT SYSTEM
                if current_time - last_alert_time > ALERT_COOLDOWN:
                    print("🚨 Accident detected – sending alert")

                    timestamp = time.strftime("%Y%m%d_%H%M%S")
                    image_path = f"accident_images/accident_{timestamp}.jpg"
                    cv2.imwrite(image_path, frame)

                    play_buzzer()
                    send_email_with_image(image_path, source_type, source_name)

                    last_alert_time = current_time

        cv2.imshow("Accident Detection System", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    startapplication()
