import java.math.BigInteger;
import java.util.Random;

/**
 * Emiliano Galeana Araujo
 * César Eduardo Jardines Mendoza
 * César Gustavo Sánchez de la Rosa 
 * Criptografía y Seguridad 2020-2
 */
public class RSA {

    private class Tup<T> {
        /*Número n.*/
        private T n;
        /*Número e.*/
        private T e;
        /*Número d.*/
        private T d;
        /*
         * Constructor de la clase Tup, recibimos los 3 datos (N,E,D) para la 
         * llave.
         */
        public Tup(T e, T d, T n) {
            this.e = e;
            this.d = d;
            this.n = n;
        }
        /*
         * Método get que nos regresa n,d,e según se indique.
         */
        public T get(char c) {
            T ret = null;
            switch (c) {
            case 'n':
                ret = this.n;
                break;
            case 'd':
                ret = this.d;
                break;
            case 'e':
                ret = this.e;
                break;
            }
            return ret;
        }
        /*
         * Método toString de la clase privada tup.
         */
        public String toString() {
            return "(" + this.n + ", " + this.e + ", " + this.d + ")";
        }
    }
    /*
     * Método que crea tuplas con los parámetros que nos pasan.
     */
    public Tup<BigInteger> createTup(String $e, String $d, String $n) {
        return new Tup<BigInteger>(new BigInteger($e),
                                   new BigInteger($d),
                                   new BigInteger($n));
    }
    /*
     * Método para generar llaves, es random por lo que no recibe parámetros.
     * Regresa una tupla de la forma (e,d,n)
     */
    public Tup<BigInteger> generateKeys() {
        Random r = new Random(); // Random
        BigInteger p = BigInteger.probablePrime(1024, r); // P prime
        BigInteger q = BigInteger.probablePrime(1024, r); // Q prime
        BigInteger n = p.multiply(q); // N = P*Q
        BigInteger phi = p.subtract(BigInteger.ONE).
            multiply(q.subtract(BigInteger.ONE));
        BigInteger e = BigInteger.probablePrime(512, r);
        BigInteger d;
        while ( phi.gcd(e).compareTo(BigInteger.ONE) > 0
                && e.compareTo(phi) < 0 )
            e.add(BigInteger.ONE);
        d = e.modInverse(phi);
        return new Tup<BigInteger>(e,d,n);
    }
    /*
     * Método para encriptar un mensaje.
     * @param mensaje en arreglo de bytes y una tupla con las claves.
     */
    public byte[] encrypt(byte[] m, Tup<BigInteger> t) {
        BigInteger n = t.get('n');
        BigInteger e = t.get('e');
        return (new BigInteger(m)).modPow(e, n).toByteArray();
    }
    /*
     * Método para desencriptar un mensaje.
     * @param mensaje en arreglo de bytes y una tupla con las claves.
     */
    public byte[] decrypt(byte[] m, Tup<BigInteger> t) {
        BigInteger n = t.get('n');
        BigInteger d = t.get('d');        
        return (new BigInteger(m)).modPow(d, n).toByteArray();
    }
    /*
     * Método que pasa un arreglo de bytes a una cadena, usamos el separador '%'.
     */
    private static String bytesToString(byte[] encrypted) {
        String test = "";
        for (byte b : encrypted)
            test += Byte.toString(b) + "%";
        return test;
    }
    /*
     * Método que pasa un arreglo de cadenas a un arreglo de bytes.
     * El arreglo de cadenas ya son bytes, pero hay que parsearlos.
     */
    private static byte[] stringToBytes(String[] s) {
        byte[] encrypted = new byte[s.length];
        int i = 0;
        while (i < s.length) {
            encrypted[i] = (byte)Integer.parseInt(s[i]);
            i++;
        }
        return encrypted;
    }
    
    public static void main(String[] args) {
        
        RSA rsa = new RSA(); // Objeto.
                
        if (args.length == 0) {
            System.out.println("Intenta con banderas.");
            System.out.println("Leer documentación.");
        } else {
            if (args[0].equals("-k")) { // get keys
                RSA.Tup<BigInteger> b = rsa.generateKeys();
                System.out.println(b.get('n'));
                System.out.println();
                System.out.println();
                System.out.println(b.get('d'));
                System.out.println();
                System.out.println();
                System.out.println(b.get('e'));
                System.out.println();
                System.out.println();
            } else if (args[0].equals("-e")) { // encrypt
                if (args.length != 4) {
                    System.out.println("Error en el input.");
                    System.exit(1);
                }
                String m = args[1];
                String n = args[2];
                String e = args[3];
                RSA.Tup<BigInteger> clave = rsa.createTup(e, e, n);

                byte[] encrypted = rsa.encrypt(m.getBytes(), clave);
                System.out.println(bytesToString(encrypted));
            } else if (args[0].equals("-d")) { // decrypt
                if (args.length != 4) {
                    System.out.println("Error en el input.");
                    System.exit(1);
                }
                String m = args[1];
                String n = args[2];
                String d = args[3];
                RSA.Tup<BigInteger> clave = rsa.createTup(d, d, n);

                String[] strEnc = m.split("%");
                
                byte[] encrypted = stringToBytes(strEnc);
                byte[] decrypted = rsa.decrypt(encrypted, clave);
                System.out.println(new String(decrypted));
            } else {
                System.out.println("Bandera erronea.");
                byte[] prueba = {1,2,3,4,5,6,(byte)700};
                System.out.println(bytesToString(prueba));
            }
        }
    }
}
