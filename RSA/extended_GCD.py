def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, xtmp, ytmp = extended_gcd(b, a % b)
        x = ytmp
        y = xtmp - int(a // b) * ytmp
        return gcd, x, y
