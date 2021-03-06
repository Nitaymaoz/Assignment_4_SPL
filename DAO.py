class Suppliers:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, supplierDTO):
        self.connection.execute("""
        INSERT INTO suppliers (id, name)
        VALUES(?, ?)      
        """, [supplierDTO.id, supplierDTO.name])

    def find(self, supplier_id):
        cursor = self.connection.cursor()
        cursor.execute("""
                SELECT name FROM suppliers WHERE id = ?
                """, [supplier_id])
        supplier = cursor.fetchone()
        return supplier


class Hats:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, hatDTO):
        self.connection.execute("""
        INSERT INTO hats (id, topping, supplier, quantity)
        VALUES(?, ?, ?, ?)      
        """, [hatDTO.id, hatDTO.topping, hatDTO.supplier, hatDTO.quantity])

    def find(self, topping):
        cursor1 = self.connection.cursor()
        cursor1.execute("""
        SELECT supplier FROM hats WHERE topping = ?
        """, [topping])
        suppliers_list = cursor1.fetchall()
        suppliers_list.sort()
        supplier = suppliers_list[0][0]

        cursor2 = self.connection.cursor()
        cursor2.execute("""
                SELECT id FROM hats WHERE supplier = ? AND topping = ?
                """, [supplier, topping])
        available_id = cursor2.fetchone()[0]

        self.connection.execute("""
        UPDATE hats
        SET quantity = quantity-1
        WHERE id = ?
        """, [available_id])

        return available_id

    def check_quantity(self, id):
        cursor = self.connection.cursor()
        cursor.execute("""
        SELECT quantity FROM hats WHERE id = ?
        """, [id])
        quantity_left = cursor.fetchone()
        if quantity_left[0] == 0:
            self.connection.execute("""
            DELETE FROM hats
            WHERE id = ?
            """, [id])

    def get_supplier_id(self, hat_id):
        cursor = self.connection.cursor()
        cursor.execute("""
                SELECT supplier FROM hats WHERE id = ?
                """, [hat_id])
        supplier_id = cursor.fetchone()[0]
        return supplier_id


class Orders:
    def __init__(self, connection):
        self.connection = connection

    def insert(self, orderDTO):
        self.connection.execute("""
        INSERT INTO orders (id, location, hat)
        VALUES(?, ?, ?)      
        """, [orderDTO.id, orderDTO.location, orderDTO.hat])
