from text_utils import num_to_bits


def gen_heading(endian, dtype, codex, channel_order, correction_level):
    header = "1010"

    if endian == "big":
        header += "1"
    elif endian == "little":
        header += "0"
    else:
        return -1

    if dtype == "utf-8":
        header += "000"
    elif dtype == "ascii":
        header += "001"
    elif dtype == "bin":
        header += "010"
    else:
        header += "011"

    for i in codex:
        header += num_to_bits(i)
    for i in channel_order:
        header += num_to_bits(i)[6:]

    if correction_level == "none":
        header += "00"
    elif correction_level == "low":
        header += "01"
    elif correction_level == "medium":
        header += "10"
    elif correction_level == "high":
        header += "11"
    else:
        return -1

    if len(header) != 40:
        return -1
    return int(header, 2)


def read_heading(heading):
    heading_bits = num_to_bits(heading)
    print(heading_bits)
    header_dict = {}

    if heading_bits[:4] != "1010":
        return -1

    header_dict['endian'] = "big" if heading_bits[4] == '1' else "little"

    if heading_bits[5:8] == "000":
        header_dict['data_type'] = "utf_8"
    elif heading_bits[5:8] == "001":
        header_dict['data_type'] = "ascii"
    elif heading_bits[5:8] == "010":
        header_dict['data_type'] = "bin"
    else:
        header_dict['data_type'] = "other"

    codex = [int(heading_bits[8:16], 2), int(heading_bits[16:24], 2), int(heading_bits[24:32], 2)]
    order = [int(heading_bits[32:34], 2), int(heading_bits[34:36], 2), int(heading_bits[36:38], 2)]

    header_dict['codex'] = codex
    header_dict['channel_order'] = order

    if heading_bits[38:] == "00":
        header_dict['correction_level'] = "none"
    elif heading_bits[38:] == "01":
        header_dict['correction_level'] = "low"
    elif heading_bits[38:] == "10":
        header_dict['correction_level'] = "medium"
    elif heading_bits[38:] == "11":
        header_dict['correction_level'] = "high"

    return header_dict


if __name__ == "__main__":
    test_endian = "big"
    test_dtype = "utf-8"
    test_codex = [255, 255, 255]
    test_order = [0, 1, 2]
    test_correction = "none"
    test_heading = gen_heading(test_endian, test_dtype, test_codex, test_order, test_correction)

    print(read_heading(test_heading))
