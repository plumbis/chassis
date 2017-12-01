#!/usr/bin/env python3

hostname_base = "chassis1"
hostname_linecard = "-lc"
hostname_fabriccard = "-fc"

backpack = [4, 2, 4, 1, 4]
omp800 = [8, 2, 4, 2, 2]


def generate_dot(num_lc, num_lc_asic, num_fc, num_fc_asic, num_links,):

    lc_counter = [[0 for x in range(num_lc_asic)] for y in range(num_lc)]
    fc_counter = [[0 for x in range(num_fc_asic)] for y in range(num_fc)]

    for fabric in range(1, num_fc + 1):
        for fabric_asic in range(1, num_fc_asic + 1):
            for lc in range(1, num_lc + 1):
                for lc_asic in range(1, num_lc_asic + 1):
                    for link in range(1, num_links + 1):

                        dot_line = []
                        dot_line.append("\"" + hostname_base + hostname_linecard + str(lc) + "-" + str(lc_asic) + "\":")
                        dot_line.append("\"fp")
                        dot_line.append(str(lc_counter[lc - 1][lc_asic - 1]))
                        dot_line.append("\" -- ")
                        dot_line.append("\"" + hostname_base + hostname_fabriccard + str(fabric) + "-" + str(fabric_asic) + "\":")
                        dot_line.append("\"fp")
                        dot_line.append(str(fc_counter[fabric - 1][fabric_asic - 1]))
                        dot_line.append("\"")

                        lc_counter[lc - 1][lc_asic - 1] = lc_counter[lc - 1][lc_asic - 1] + 1
                        fc_counter[fabric - 1][fabric_asic - 1] = fc_counter[fabric - 1][fabric_asic - 1] + 1

                        print("".join(dot_line))


def main():

    generate_dot(*backpack)


if __name__ == "__main__":
    main()
