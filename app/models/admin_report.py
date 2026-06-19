from datetime import datetime

class Report:
    def __init__(self, database):
        self.db = database
        self.create_table()

    def create_table(self):
        """Create reports table if it doesn't exist"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reports (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    title VARCHAR(255) NOT NULL,
                    description TEXT,
                    location VARCHAR(255),
                    type VARCHAR(50),
                    status VARCHAR(50) DEFAULT 'Pending',
                    image VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            self.db.commit()
            print("Reports table created/verified successfully!")
        except Exception as e:
            print(f"Error creating reports table: {e}")

    def get_all_reports(self, search=None, status=None, report_type=None, page=1, per_page=10):
        """Get all reports with optional search, filter and pagination"""
        cursor = self.db.get_cursor()
        try:
            query = """
                SELECT r.*, u.username, u.email, u.fullname
                FROM reports r
                JOIN users u ON r.user_id = u.id
                WHERE 1=1
            """
            params = []

            if search:
                query += " AND (r.title LIKE %s OR r.location LIKE %s)"
                params.extend([f"%{search}%", f"%{search}%"])

            if status:
                query += " AND r.status = %s"
                params.append(status)

            if report_type:
                query += " AND r.type = %s"
                params.append(report_type)

            # total count
            count_query = f"SELECT COUNT(*) as total FROM ({query}) as counted"
            cursor.execute(count_query, params)
            total = cursor.fetchone()['total']

            # paginate
            query += " ORDER BY r.created_at DESC LIMIT %s OFFSET %s"
            offset = (page - 1) * per_page
            params.extend([per_page, offset])

            cursor.execute(query, params)
            reports = cursor.fetchall()

            return {"success": True, "reports": reports, "total": total}
        except Exception as e:
            print(f"Error fetching reports: {e}")
            return {"success": False, "reports": [], "total": 0}

    def get_report_by_id(self, report_id):
        """Get a single report by ID with user info"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("""
                SELECT r.*, u.username, u.email, u.fullname
                FROM reports r
                JOIN users u ON r.user_id = u.id
                WHERE r.id = %s
            """, (report_id,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error fetching report: {e}")
            return None

    def update_status(self, report_id, status):
        """Update report status"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute(
                "UPDATE reports SET status = %s WHERE id = %s",
                (status, report_id)
            )
            self.db.commit()
            return {"success": True, "message": "Status updated successfully!"}
        except Exception as e:
            return {"success": False, "message": f"Error updating status: {e}"}

    def delete_report(self, report_id):
        """Delete a report by ID"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("DELETE FROM reports WHERE id = %s", (report_id,))
            self.db.commit()
            return {"success": True, "message": "Report deleted successfully!"}
        except Exception as e:
            return {"success": False, "message": f"Error deleting report: {e}"}

    def get_stats(self):
        """Get total, pending and resolved counts"""
        cursor = self.db.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as total FROM reports")
            total = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM reports WHERE status = 'Pending'")
            pending = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM reports WHERE status = 'Resolved'")
            resolved = cursor.fetchone()['total']

            return {"total": total, "pending": pending, "resolved": resolved}
        except Exception as e:
            print(f"Error fetching stats: {e}")
            return {"total": 0, "pending": 0, "resolved": 0}