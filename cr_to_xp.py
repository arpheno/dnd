_cr = [200, 450, 700, 1100, 1800, 2300, 2900, 3900, 5000, 5900,
       7200, 8400, 10000, 11500, 13000, 15000, 18000, 20000, 22000, 25000, 33000, 41000, 50000, 62000]
cr_to_xp = {
    '1/8': 25,
    '1/4': 50,
    '1/2': 100,
    '30': 155000
}
for i, cr in enumerate(_cr, start=1):
    cr_to_xp[i] = cr
    cr_to_xp[str(i)] = cr
print(cr_to_xp)
