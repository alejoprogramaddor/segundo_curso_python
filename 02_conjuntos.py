# un conjunto es un grupo de elementos que contienen algo en comun , por ejemplo 

'''las propiedades principales de los conjuntos son los siguientes 
1ra se pueden modificar 
2da no tienen un orden en especifico 
3ra no permite duplicados '''

set_countries ={
    'colombia',
    'mexico',
    'bolivia'
}

print(set_countries)
print(type(set_countries))

'''como podemos observar en el type aparece set , que significa conjuntos '''
'''si se vuelve a poner colombia y queda dos veces , de inmediato lo va a quitar por que no acepta documentos duplicados 
tambien podemos tener un conjunto de numeros , como por ejemplo '''

set_numbers = {1, 2, 3, 4, 5}
print(set_numbers)

'''tambien podemos poner un conjunto con diferentes tipos de datos como por ejemplo '''

set_types = {1, 'hola',  False, 12.12}
print(set_types)


'''otra forma de definir conjuntos es apartir de otras estructuras de datos , por ejemplo'''

set_from_string = set('hola')
print(set_from_string)

'''como podemos observar cada string lo partio en cada uno de los caracteres y creo un conjunto de cada uno de los caracteres que encontro '''

set_from_tupla = set(('abc', 'cbv', 'as', 'abc'))
print(set_from_tupla)

'''esta es una tupla en un conjunto , como podemos observar enb la terminal solo aparece una vez abc , y es por que los conjuntos no se repiten '''

numbers = [1, 2, 3, 4, 5, 6]
set_numbers = set(numbers)
print(set_numbers)

'''en la parte de arriba vemos que se transforma a un set(numbers) y asi es que se convierte a un conjunto 
se puede volver a convertir de un conjunto o set a una lista y es de la siguiente forma '''

convetir_lista = list(set_numbers)
print(convetir_lista)

print(type(convetir_lista))


