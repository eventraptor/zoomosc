<?php

namespace App\Console\Commands;

use App\Lib\OSCDecoder;
use Exception;
use Illuminate\Console\Command;
use React\Datagram\Factory;
use React\Datagram\Socket;
use React\EventLoop\Loop;

class OSCLogger extends Command
{
    protected $signature = 'logger {address=127.0.0.1:1234}';

    protected $description = 'Logs and Displays ZoomOSC Messages';

    public function handle(): void
    {
        $loop = Loop::get();
        $server = new Factory($loop);
        $address = $this->argument('address');

        $osc_decoder = new OSCDecoder;

        $server->createServer($address)
            ->then(
                function (Socket $server) use ($osc_decoder) {
                    $server->on('message', function ($message, $address, $socket) use ($osc_decoder, &$handler) {
                        $result = $osc_decoder->decode_osc($message);
                        $result['time'] = microtime(true);

                        $type = basename($result['address']);
                        if (in_array($type, [
                            'audioLevels',
                            'audioRouting',
                            'outputRouting',
                            'engineState',
                        ])) {
                            return;
                        }

                        $message = round($result['time'], 1).
                                   ' '.
                                   $result['address'].
                                   ' '.
                                   implode(' ', $result['args']).
                                   PHP_EOL;
                        echo $message;
                    });
                },
                function (Exception $error) {
                    $this->warn(sprintf('ERROR: %s', $error->getMessage()));
                });

        $this->info(sprintf('Listening on %s', $address));
        $loop->run();
    }
}
