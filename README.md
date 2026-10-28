# SecurePass — Web Based Password Strength Checker

A runnable mini-project based on the uploaded SecurePass report. It uses **HTML, CSS, JavaScript and PHP**, and does not require MySQL. Passwords are analyzed for the current request only; the project does not save passwords or evaluation history.

## Features included from the report

- Real-time password strength evaluation
- Score from 0–100 and Weak / Moderate / Strong classification
- Colour-coded strength meter
- Checks for length, uppercase, lowercase, digits and special characters
- Detection of common password strings, three repeated characters, and simple keyboard/alphanumeric sequences
- Suggestions that update as the password changes
- Show/hide password control
- Live estimated crack time with selectable online, offline slow-hash and offline fast-hash scenarios
- Input validation and a responsive interface
- PHP server-side evaluation endpoint using the same scoring rules
- No password storage or logging

The optional MySQL database described in the report is not needed for this rule-based version.

## Requirements

- Windows 10/11
- Visual Studio Code (or another editor)
- PHP 8.0+ available on PATH, **or XAMPP** with Apache/PHP
- A modern browser such as Chrome or Edge

## Option A — Run with PHP (recommended if PHP is installed)

1. Extract the `SecurePass` folder.
2. Open the folder in Visual Studio Code.
3. Open **Terminal → New Terminal**.
4. Run this command from inside the `SecurePass` folder:

   ```powershell
   php -S localhost:8000
   ```

5. Open `http://localhost:8000` in Chrome or Edge.

If PowerShell says `php` is not recognized, use Option B or install PHP and add it to PATH.

## Option B — Run with XAMPP

1. Install XAMPP if it is not installed.
2. Copy the entire `SecurePass` folder into `C:\xampp\htdocs\SecurePass`.
3. Open the XAMPP Control Panel and click **Start** next to Apache.
4. Open `http://localhost/SecurePass/` in your browser.

No MySQL service is required.

## Quick checks

- Type `abc123`: it should show Weak.
- Type `Password1`: common-word detection should lower the score.
- Type a long, mixed sample such as `Xk9#mP2$vL7!qR4z`: it should score strongly.
- Click **SHOW/HIDE** to toggle visibility.
- Change **Assumed attack scenario** to compare illustrative crack-time estimates. The rate assumptions are examples, not guarantees; predictable passwords can be cracked much faster.
- The score, meter, checklist and suggestions should update while typing.

Use sample passwords only. Do not enter a password you currently use for a real account.

## Project structure

```text
SecurePass/
├── index.php
├── api/
│   └── evaluate.php
├── assets/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
└── README.md
```

## Important project note

The score follows the rule-based algorithm in the report; it is a learning aid and not a guarantee of real-world password resistance. It does not query breached-password databases, implement AI/ML, MFA, biometrics or account authentication. Those are listed as excluded/future-scope features in the report.

## Troubleshooting

- **Blank page / PHP code downloads:** open through `http://localhost...`, not by double-clicking `index.php`.
- **`php` not recognized:** use XAMPP Option B.
- **Page loads but server-side status says browser-side analysis:** make sure you opened the page through PHP/XAMPP and that `api/evaluate.php` exists.
- **Port 8000 already in use:** run `php -S localhost:8080` and open `http://localhost:8080`.
