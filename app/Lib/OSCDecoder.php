<?php

namespace App\Lib;

class OSCDecoder
{
    protected function decode_osc_string($data)
    {
        $end = strpos($data, "\0");
        $s = substr($data, 0, $end);

        return [$s, substr($data, $end + 4 - ($end % 4))];
    }

    protected function decode_osc_int($data)
    {
        $i = unpack('N', $data)[1];
        if ($i > 0x7FFFFFFF) { // If it's greater than the maximum 32-bit signed integer
            $i -= 0x100000000; // Convert to negative number
        }

        return [$i, substr($data, 4)];
    }

    protected function decode_osc_float($data)
    {
        $f = unpack('f', strrev($data))[1];

        return [$f, substr($data, 4)];
    }

    public function decode_osc($data)
    {
        [$address, $data] = $this->decode_osc_string($data);
        [$type_tags, $data] = $this->decode_osc_string($data);

        $args = [];
        for ($i = 1; $i < strlen($type_tags); $i++) {
            switch ($type_tags[$i]) {
                case 's':
                    [$arg, $data] = $this->decode_osc_string($data);
                    $args[] = $arg;
                    break;
                case 'i':
                    [$arg, $data] = $this->decode_osc_int($data);
                    $args[] = $arg;
                    break;
                case 'f':
                    [$arg, $data] = $this->decode_osc_float($data);
                    $args[] = $arg;
                    break;
                    // Add more types as needed
            }
        }

        return [
            'address' => $address,
            'args' => $args,
        ];
    }
}
