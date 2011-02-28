<?
require_once(dirname(__FILE__).'/../PushConnection.php');

$P=new PushConnection(123456, 'login', 'hasło');
$P->setUrl('http://twojademona.pl/bot.php');
