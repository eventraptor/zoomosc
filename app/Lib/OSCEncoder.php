<?php

namespace App\Lib;

class OSCEncoder
{
    protected function encode_osc_string($s): string
    {
        // Append null terminator
        $s .= "\0";
        // Calculate padding to make the length a multiple of 4
        $len = strlen($s);
        $pad = (4 - ($len % 4)) % 4;

        // Add padding
        return $s.str_repeat("\0", $pad);
    }

    protected function encode_osc_int($i): string
    {
        // Pack integer into a 32-bit big-endian binary string
        return pack('N', $i);
    }

    protected function encode_osc_float($f): string
    {
        // Pack float into a 32-bit big-endian binary string
        return pack('G', $f);
    }

    public function encode_osc($address, $args): string
    {
        // Encode the OSC address pattern
        $data = $this->encode_osc_string($address);

        // Initialize the type tag string with a comma
        $type_tags = ',';
        $args_data = '';

        // Loop through each argument to build the type tag string and encode arguments
        foreach ($args as $arg) {
            if (is_int($arg)) {
                $type_tags .= 'i';
                $args_data .= $this->encode_osc_int($arg);
            } elseif (is_float($arg)) {
                $type_tags .= 'f';
                $args_data .= $this->encode_osc_float($arg);
            } elseif (is_string($arg)) {
                $type_tags .= 's';
                $args_data .= $this->encode_osc_string($arg);
            } else {
                // Handle more types as needed
                throw new \Exception('Unsupported argument type: '.gettype($arg));
            }
        }

        // Encode the type tag string
        $data .= $this->encode_osc_string($type_tags);
        // Append the encoded arguments
        $data .= $args_data;

        return $data;
    }
}
