#!/usr/bin/php
<?php
require_once(dirname(__FILE__).'/../MessageBuilder.php');

$M=new MessageBuilder();

if ( !isset( $argv[1] ) ) {
    $argv[1] = '-';
}
switch ($argv[1]) {
    case 'noformat': $M->addText('text without formatting', FORMAT_NONE, 0, 0, 0); break;
    case 'bold': $M->addText('bold text', FORMAT_BOLD_TEXT); break;
    case 'html': $M->setRawHtml('<b>html content</b>', FORMAT_NONE, 0, 0, 0); break;
    case 'plain': $M->setAlternativeText('plain text'); break;
    default:
        echo sprintf( "\nUsage: %s <noformat|bold|html|plain>\n\n", $argv[0] );
        return;
}

echo "\n", base64_encode( $M->getProtocolMessage() ), "\n\n";
