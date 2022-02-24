from random import choice, randint, shuffle

estados = ['Aguascalientes', 'Baja_California', 'Baja_California_Sur', 'Campeche', 'Chiapas', 'Chihuahua',
           'Coahuila_de_Zaragoza', 'Colima', 'Distrito_Federal', 'Durango', 'Guanajuato', 'Guerrero', 'Hidalgo',
           'Jalisco', 'México', 'Michoacán_de_Ocampo', 'Morelos', 'Nayarit', 'Nuevo_León', 'Oaxaca',
           'Puebla', 'Querétaro', 'Quintana_Roo', 'San_Luis_Potosí', 'Sinaloa', 'Sonora', 'Tabasco', 'Tamaulipas',
           'Tlaxcala', 'Veracruz_de_Ignacio_de_la_Llave', 'Yucatán', 'Zacatecas']


def generate_api_key():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_l = [choice(letters) for _ in range(randint(8, 10))]
    password_s = [choice(symbols) for _ in range(randint(2, 4))]
    password_n = [choice(numbers) for _ in range(randint(2, 4))]

    api_key = password_l + password_s + password_n

    shuffle(api_key)

    api_key = "".join(api_key)

    return api_key
