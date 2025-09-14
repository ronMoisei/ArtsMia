from database.DB_connect import DBConnect
from model.driver import Driver
from model.arcoPiloti import Arco


class DAO():

    @staticmethod
    def getAllPiloti():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result = []
        query = """
        select d.*
        from drivers d
        """

        cursor.execute(query)

        for row in cursor:
            result.append(Driver(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllArchiPiloti(idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        result  = []
        query = """
                SELECT r1.driverId as d1, r2.driverId as d2, count(*) as peso
                FROM results r1, results r2 
                WHERE r1.raceId = r2.raceId
                and r1.driverId < r2.driverId
                group by r1.driverId, r2.driverId 
                order by peso desc
            """

        cursor.execute(query)

        for row in cursor:
            result.append(Arco(idMap[row["d1"]], idMap[row["d2"]], row["peso"]))

        cursor.close()
        conn.close()
        if len(result) == 0:
            return None
        return result

if __name__ == '__main__':
    DAO = DAO()
    DAO.getAllArchiPiloti()

