# Intelligent Accident Detection & Real-Time Alerts

🏆 **Project Expo winner**

A computer-vision system that watches a live camera or a traffic video, classifies every frame with a convolutional neural network, and when it detects an accident, saves the frame, sounds a buzzer and emails an alert with the snapshot attached.

```text
camera / video  →  OpenCV frames  →  CNN classifier  →  confidence > 80%  →  snapshot · buzzer · email alert
```

![TensorFlow](https://img.shields.io/badge/TensorFlow-161B22?style=flat-square&logo=tensorflow&logoColor=A78BFA)
![Keras](https://img.shields.io/badge/Keras-161B22?style=flat-square&logo=keras&logoColor=A78BFA)
![OpenCV](https://img.shields.io/badge/OpenCV-161B22?style=flat-square&logo=opencv&logoColor=A78BFA)
![Python](https://img.shields.io/badge/Python-161B22?style=flat-square&logo=python&logoColor=A78BFA)

## Highlights

- **Custom CNN:** four convolution blocks (32 → 256 filters) with batch normalisation, 22.5M parameters, 250×250 RGB input.
- **91.8% best validation accuracy** on a held-out set of 98 images, after training on 791 labelled traffic images.
- **Two input modes:** a live camera feed or any video file.
- **Alerts with evidence:** the saved frame, a buzzer, and an email with the source, date, time and snapshot. A two-minute cooldown stops one incident from flooding the inbox.
- **Web version:** a Streamlit app for monitoring uploaded videos in the browser lives in [MalliACC](https://github.com/MallikarjunaRaoPotti/MalliACC).

## How it works

1. `main.py` starts `camera.py`, which asks for the input: **1** for the live camera or **2** for a video file path.
2. Each frame is converted to RGB, resized to 250×250 and passed to the model (`detection.py`).
3. When the model predicts **Accident** with more than 80% confidence, the label and confidence are drawn on the frame.
4. If more than two minutes have passed since the last alert, the system:
   - saves the frame to `accident_images/accident_<timestamp>.jpg`
   - sounds a buzzer
   - emails the alert with the snapshot attached
5. Press **q** to stop.

## Model

Defined and trained in [`accident-classification.ipynb`](accident-classification.ipynb). The architecture is saved in `model.json`.

| Layer | Details |
| :-- | :-- |
| Batch normalisation | on the 250×250×3 input |
| Conv2D + max pooling ×4 | 32, 64, 128 and 256 filters, 3×3 kernels, ReLU |
| Flatten → Dense | 512 units, ReLU |
| Dense (output) | 2 units, softmax: `Accident`, `Non Accident` |

**Training:** Adam optimiser, sparse categorical cross-entropy, batch size 100, 20 epochs. A `ModelCheckpoint` keeps the weights with the best validation accuracy.

| Split | Images |
| :-- | --: |
| `data/train` | 791 |
| `data/val` | 98 |
| `data/test` | 100 |

The best checkpoint reached **91.8% validation accuracy** (epoch 20), with 97.9% training accuracy.

## Run it yourself

**1. Install the dependencies** (developed on Python 3.12):

```bash
git clone https://github.com/MallikarjunaRaoPotti/Intelligent-Accident-Detection-Using-Deep-Learning-and-Real-Time-Alert-Generation-.git
cd Intelligent-Accident-Detection-Using-Deep-Learning-and-Real-Time-Alert-Generation-
pip install -r requirements.txt
```

**2. Get the model weights.** `model_weights.h5` (about 270 MB) isn't stored in this repository. Either:

- train it by running `accident-classification.ipynb`, which saves `model_weights.h5` as it goes, or
- download the trained weights from [MalliACC](https://github.com/MallikarjunaRaoPotti/MalliACC), which uses the same `model.json` and stores the weights with Git LFS.

Put `model_weights.h5` in the project root.

**3. Configure email alerts** with a Gmail address and a [Gmail app password](https://support.google.com/accounts/answer/185833). Credentials are read from environment variables and never stored in the code:

```powershell
$env:ALERT_EMAIL_SENDER = "your.address@gmail.com"
$env:ALERT_EMAIL_APP_PASSWORD = "your-app-password"
$env:ALERT_EMAIL_RECEIVER = "who.gets.alerts@example.com"
python test_mail.py   # sends a test email
```

On macOS or Linux, use `export ALERT_EMAIL_SENDER=...` instead. If the variables aren't set, detection still runs and alerts are saved locally without an email.

**4. Run it:**

```bash
python main.py
```

Choose **1** for the live camera or **2** to enter the path of a video file. A sample traffic clip is included in the repository.

## Project structure

```text
main.py                        entry point
camera.py                      capture loop, confidence check, alerts (buzzer + email)
detection.py                   loads model.json + model_weights.h5 and runs predictions
test_mail.py                   checks the email configuration
accident-classification.ipynb  dataset loading, CNN definition, training and evaluation
model.json                     saved model architecture
data/                          train / val / test images (Accident, Non Accident)
accident_images/               frames saved by alerts during test runs
```

## Limitations

- Each frame is classified on its own, with no temporal smoothing, so a single misclassified frame can trigger an alert. The cooldown limits repeats.
- The buzzer uses `winsound`, so it only works on Windows.
- The dataset is small (791 training images), so accuracy will vary with new camera angles and lighting.
- The "location" in an alert is the input source name (camera or file name), not a GPS position.

## Tech stack

Python · TensorFlow / Keras · OpenCV · NumPy · smtplib · Jupyter

## Author

**Mallikarjuna Rao Potti** · [GitHub](https://github.com/MallikarjunaRaoPotti) · [Portfolio](https://portfolio-p5o1.vercel.app) · [LinkedIn](https://www.linkedin.com/in/mallikarjuna7)
