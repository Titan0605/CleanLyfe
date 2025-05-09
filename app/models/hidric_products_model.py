from app.utils.db_utils import get_cursor, exec_commit

class Hidcric_products_model:
    def __init__(self) -> None:
        self._cur = get_cursor()
        
    def _open_cursor(self) -> None:
        """Open database cursor if not already open"""
        if not self._cur:
            self._cur = get_cursor()
            
    def _commit_query(self) -> None:
        """Commit current transaction"""
        if self._cur:
            self._cur = exec_commit()
            
    def _close_cursor(self) -> None:
        """Close database cursor if open"""
        if self._cur:
            self._cur.close()
            self._cur = None
            
    def insert_consumption(self, consumption: int) -> str:
        try:
            self._open_cursor()
            if not self._cur:
                raise Exception("Failed to open database cursor")
            
            query = "INSERT INTO hf_water_consumption(consumption) VALUES (%s)"
            values: tuple = (consumption,)
            
            self._cur.execute(query, values)
            self._commit_query()
            
            self._close_cursor()
            return "Consumption inserted succesfully"
        except Exception as error:
            self._close_cursor()
            return (f"Error inserting consumption: {error}")