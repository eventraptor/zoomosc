<?php

namespace App\Lib;

use App\Services\UdpSender;

class SendMessage
{
    public function __construct(protected string $message, protected array $args) { }

    public function send($ip = '127.0.0.1', $port = 9090): void
    {
        $udpSender = new UdpSender();
        try {
            $encoder = new OSCEncoder();
            $packet = $encoder->encode_osc($this->message, $this->args);
            $udpSender->send($ip, $port, $packet);
        } catch (\Exception $e) {
            echo 'Error: '.$e->getMessage(), PHP_EOL;
        }
    }
}
