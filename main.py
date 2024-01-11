import usb.core

VID = 0x1532
PID = 0x021E


def calculate_brightness_msg_checksum(message: list):
    checksum = (
        abs(
            -message[1]
            + message[5]
            + message[6]
            + message[7]
            + message[8]
            + message[10]
            - 1
        )
        % 256
    )
    return checksum


def create_brightness_header(brightness: int) -> bytearray:
    header = [0] * 90

    header[1] = 0x1F
    header[5] = 0x03
    header[6] = 0x0F
    header[7] = 0x04
    header[8] = 0x01
    header[10] = int(255 * brightness / 100)

    header[-2] = calculate_brightness_msg_checksum(header)

    return bytearray(header)


def create_brightness_footer(brightness: int) -> bytearray:
    footer = [0] * 90

    footer[0] = 0x02
    footer[1] = 0x1F
    footer[5] = 0x03
    footer[6] = 0x0F
    footer[7] = 0x04
    footer[8] = 0x01
    footer[10] = int(255 * brightness / 100)

    checksum = (
        abs(-footer[1] + footer[5] + footer[6] + footer[7] + footer[8] + footer[10] - 1)
        % 256
    )
    footer[-2] = calculate_brightness_msg_checksum(footer)

    return bytearray(footer)


def create_brightness_message(brightness: int) -> tuple[bytearray]:
    brightness = max(0, min(100, brightness))
    header = create_brightness_header(brightness)
    footer = create_brightness_footer(brightness)
    return header, footer


def print_bytearray(byte_array: bytearray):
    print(
        f"length: {len(byte_array)}",
        "Byte Array:",
        " ".join(format(x, "02x") for x in byte_array),
    )


def main():
    dev = usb.core.find(idVendor=VID, idProduct=PID)

    print(dev)
    if dev is None:
        raise ValueError('Device not found')

    # dev.set_configuration()

    # cfg = dev.get_active_configuration()
    # print(cfg)
    # intf = cfg[(0,0)]
    # print(intf)



if __name__ == "__main__":
    main()
