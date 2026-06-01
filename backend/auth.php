<?php
header("Access-Control-Allow-Origin: *");
header("Access-Control-Allow-Headers: Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With");
header("Access-Control-Allow-Methods: POST, GET, OPTIONS");
header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    exit(0);
}

$host = 'db';
$db   = 'cooking_db';
$user = 'root';
$pass = 'secret_password';
$charset = 'utf8mb4';

$dsn = "mysql:host=$host;dbname=$db;charset=$charset";
$options = [
    PDO::ATTR_ERRMODE            => PDO::ERRMODE_EXCEPTION,
    PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
    PDO::ATTR_EMULATE_PREPARES   => false,
];

try {
     $pdo = new PDO($dsn, $user, $pass, $options);
} catch (\PDOException $e) {
     echo json_encode(['success' => false, 'message' => 'Връзката с базата данни пропадна: ' . $e->getMessage()]);
     exit;
}

$input = json_decode(file_get_contents('php://input'), true);
$action = $input['action'] ?? '';

if ($action === 'register') {
    $username = trim($input['username'] ?? '');
    $email = trim($input['email'] ?? '');
    $password = trim($input['password'] ?? '');

    if (!$username || !$email || !$password) {
        echo json_encode(['success' => false, 'message' => 'Всички полета са задължителни!']);
        exit;
    }

    $stmt = $pdo->prepare('SELECT id FROM users WHERE username = ?');
    $stmt->execute([$username]);
    if ($stmt->fetch()) {
        echo json_encode(['success' => false, 'message' => 'Потребителското име вече е заето!']);
        exit;
    }

    $hashedPassword = password_hash($password, PASSWORD_DEFAULT);
    $stmt = $pdo->prepare('INSERT INTO users (username, email, password) VALUES (?, ?, ?)');
    
    if ($stmt->execute([$username, $email, $hashedPassword])) {
        echo json_encode(['success' => true, 'username' => $username]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Възникна грешка при запис в базата данни.']);
    }

} elseif ($action === 'login') {
    $username = trim($input['username'] ?? '');
    $password = trim($input['password'] ?? '');

    if (!$username || !$password) {
        echo json_encode(['success' => false, 'message' => 'Моля, попълнете потребителско име и парола!']);
        exit;
    }

    $stmt = $pdo->prepare('SELECT username, password FROM users WHERE username = ?');
    $stmt->execute([$username]);
    $userRow = $stmt->fetch();

    if ($userRow && password_verify($password, $userRow['password'])) {
        echo json_encode(['success' => true, 'username' => $userRow['username']]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Невалидно потребителско име или парола!']);
    }
    
} else {
    echo json_encode(['success' => false, 'message' => 'Невалидно действие.']);
}