<?php

$to = "avivoron@gmail.com";
$subject = "My subject";
$txt = "Hello world!";
$headers = "From: webmaster@example.com" . "\r\n" . "CC: somebodyelse@example.com";
printf("finished");

mail($to,$subject,$txt,$headers);
printf("finished");
?>