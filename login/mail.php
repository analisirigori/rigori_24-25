<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $to = "pianeserigori@gmail.com";  // Inserisci qui l'indirizzo email dove vuoi ricevere la notifica
    $subject = "Notifica di accesso";
    $message = "L'utente $username ha effettuato l'accesso al sito.";
    $headers = "From: noreply@tuodominio.com";

    if (mail($to, $subject, $message, $headers)) {
        echo "Email inviata con successo.";
    } else {
        echo "Errore nell'invio dell'email.";
    }
}
?>
