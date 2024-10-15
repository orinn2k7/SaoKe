import tabula

df = tabula.convert_into("./pdf/vtb_CT1111_10-12_09_2024.pdf", "output.csv", output_format="csv", pages="all")
