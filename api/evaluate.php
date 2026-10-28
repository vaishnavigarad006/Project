<?php
declare(strict_types=1);
header('Content-Type: application/json; charset=utf-8');
header('Cache-Control: no-store, max-age=0');
header('X-Content-Type-Options: nosniff');

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['success' => false, 'error' => 'Use POST for password evaluation.']);
    exit;
}

$raw = file_get_contents('php://input');
$body = json_decode($raw ?: '', true);
if (!is_array($body) || !isset($body['password']) || !is_string($body['password'])) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'A password string is required.']);
    exit;
}

$password = $body['password'];
if ($password === '') {
    echo json_encode(['success' => true, 'empty' => true]);
    exit;
}
// Limit processing size to keep requests lightweight. Do not log or persist the value.
if (strlen($password) > 4096) {
    http_response_code(413);
    echo json_encode(['success' => false, 'error' => 'Please use a password under 4096 bytes for this demo.']);
    exit;
}

function securepass_evaluate(string $pw): array {
    $score = 0;
    $length = strlen($pw); // ASCII scoring is consistent with the project's rules.
    if ($length >= 16) $score += 40;
    elseif ($length >= 12) $score += 30;
    elseif ($length >= 8) $score += 20;

    $hasUpper = preg_match('/[A-Z]/', $pw) === 1;
    $hasLower = preg_match('/[a-z]/', $pw) === 1;
    $hasDigit = preg_match('/[0-9]/', $pw) === 1;
    $hasSpecial = preg_match('/[^A-Za-z0-9]/', $pw) === 1;
    if ($hasUpper) $score += 15;
    if ($hasLower) $score += 15;
    if ($hasDigit) $score += 15;
    if ($hasSpecial) $score += 15;

    $common = ['password', '123456', '123456789', 'qwerty', 'admin', 'welcome',
        'letmein', 'iloveyou', 'monkey', 'dragon', 'sunshine', 'abc123', 'passw0rd'];
    $lower = strtolower($pw);
    $commonFound = false;
    foreach ($common as $word) {
        if (str_contains($lower, $word)) { $commonFound = true; break; }
    }
    $repeated = preg_match('/(.)\1\1/s', $pw) === 1;
    $sequence = false;
    $lowerAscii = strtolower($pw);
    $sequences = ['abcdefghijklmnopqrstuvwxyz', '0123456789', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm'];
    foreach ($sequences as $seq) {
        for ($i = 0; $i <= strlen($seq) - 3; $i++) {
            $part = substr($seq, $i, 3);
            if (str_contains($lowerAscii, $part) || str_contains($lowerAscii, strrev($part))) {
                $sequence = true; break 2;
            }
        }
    }
    if ($commonFound) $score -= 30;
    if ($repeated) $score -= 10;
    if ($sequence) $score -= 10;
    $score = max(0, min(100, $score));
    $label = $score < 40 ? 'Weak' : ($score < 70 ? 'Moderate' : 'Strong');

    $tips = [];
    if ($length < 12) $tips[] = 'Use at least 12 characters; a longer passphrase is even better.';
    if (!$hasUpper) $tips[] = 'Add an uppercase letter (A–Z), if it fits your passphrase.';
    if (!$hasLower) $tips[] = 'Add a lowercase letter (a–z).';
    if (!$hasDigit) $tips[] = 'Consider including a number (0–9).';
    if (!$hasSpecial) $tips[] = 'Consider including a symbol such as !, @, # or $.';
    if ($commonFound) $tips[] = 'Avoid common passwords and predictable words such as “password” or “welcome”.';
    if ($repeated) $tips[] = 'Avoid three or more identical characters in a row.';
    if ($sequence) $tips[] = 'Avoid simple keyboard or character sequences such as abc or 123.';
    if (!$tips) $tips[] = 'Good job. Keep it unique to one account and store it in a reputable password manager.';

    return [
        'score' => $score, 'label' => $label, 'tips' => $tips,
        'checks' => [
            'length' => ['ok' => $length >= 12, 'title' => '12+ characters'],
            'uppercase' => ['ok' => $hasUpper, 'title' => 'Uppercase letter'],
            'lowercase' => ['ok' => $hasLower, 'title' => 'Lowercase letter'],
            'number' => ['ok' => $hasDigit, 'title' => 'Number'],
            'special' => ['ok' => $hasSpecial, 'title' => 'Special character'],
            'patterns' => ['ok' => !$commonFound && !$repeated && !$sequence, 'title' => 'No obvious patterns']
        ],
        'weaknesses' => ['common' => $commonFound, 'repeated' => $repeated, 'sequence' => $sequence]
    ];
}

echo json_encode(['success' => true, 'result' => securepass_evaluate($password)], JSON_UNESCAPED_UNICODE);
