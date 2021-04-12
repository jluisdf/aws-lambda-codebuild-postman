import unittest
import lambda_function

class TestMyModule(unittest.TestCase):

	# Pruebas con funciones:
    
    #def test_sum(self):
        #self.assertEqual(lambda_function.sum(5, 7), 12)

    def test_doblar(self):
        self.assertEqual(lambda_function.doblar(10), 20)
        self.assertEqual(lambda_function.doblar('Ab'), 'AbAb')


    def test_es_par(self):
        self.assertEqual(lambda_function.es_par(11), False)
        self.assertEqual(lambda_function.es_par(68), True)

    # Pruebas con cadenas:

    def test_sumar(self):
        self.assertEqual(lambda_function.sumar(-15, 15), 0)
        self.assertEqual(lambda_function.sumar('Ab' ,'cd'), 'Abcd')


    def test_upper(self):
        self.assertEqual('hola'.upper(), 'HOLA')

    def test_isupper(self):
        self.assertTrue('HOLA'.isupper())
        self.assertFalse('Hola'.isupper())

    def test_split(self):
        s = 'Hola mundo'
        self.assertEqual(s.split(), ['Hola', 'mundo'])

    # Preparacion y limieza (antes de  y despues de ejecutar una prueba)


if __name__ == "__main__":
    unittest.main()

