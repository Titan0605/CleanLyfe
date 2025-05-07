from app.utils.db_utils import get_cursor, exec_commit

class Hidcric_products_model:
    def __init__(self) -> None:
        self._cur = get_cursor()
        
    def _openCursor(self) -> None:
        """Open database cursor if not already open"""
        if not self._cur:
            self._cur = get_cursor()
            
    def _commitQuery(self) -> None:
        """Commit current transaction"""
        if self._cur:
            self._cur = exec_commit()
            
    def _closeCursor(self) -> None:
        """Close database cursor if open"""
        if self._cur:
            self._cur.close()
            self._cur = None