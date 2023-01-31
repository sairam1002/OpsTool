from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from flask_excel_app import db
class slt_owners:
    def slt_owners_bookingforecast(self):
        st='SELECT DISTINCT slt_owner from booking_forecast;'
        res=db.session.execute(st).fetchall()
        print(res)

slt_owners().slt_owners_bookingforecast()
