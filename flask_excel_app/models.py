from datetime import datetime
from flask_excel_app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

    # def __repr__(self):
    #     return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class BookingForecast(db.Model):
    #   Table name booking_forecast
    # project_id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), primary_key=True, nullable=False)
    practice = db.Column(db.String(50), nullable=True)
    slt_owner = db.Column(db.String(50), nullable=True)
    practice_owner = db.Column(db.String(50), nullable=True)
    quarter = db.Column(db.String(3), nullable=True)
    sales_stage = db.Column(db.String(25), nullable=True)
    project_type = db.Column(db.String(15), nullable=True)
    region = db.Column(db.String(15), nullable=True)
    country = db.Column(db.String(15), nullable=True)
    win_prob = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(10), nullable=True)
    currency = db.Column(db.String(5), nullable=True)
    deal_value = db.Column(db.Float, nullable=True)
    deal_value_eur = db.Column(db.Float, nullable=True)
    last_updated_by = db.Column(db.String(50), nullable=True)
    updated_date_time = db.Column(db.DateTime, nullable=True)

    # start_date_deal = db.Column(db.Date, nullable=False)
    # end_date_deal = db.Column(db.Date, nullable=False)
    # commit = db.relationship("CommitBookingForecast", backref="resource", lazy=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def __repr__(self):
        return f"BookingForecast('{self.project_name}','{self.last_updated_by}','{self.updated_date_time}','{self.practice}','{self.slt_owner}','{self.practice_owner}','{self.quarter}','{self.sales_stage}','{self.project_type}','{self.region}','{self.country}','{self.win_prob}','{self.status}','{self.currency}','{self.deal_value})"


class Demand(db.Model):
    __tablename__ = "Demand"
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(50), nullable=True)
    practice = db.Column(db.String(50), nullable=True)
    slt_owner = db.Column(db.String(50), nullable=True)
    owner = db.Column(db.String(50), nullable=True)
    dsr_id = db.Column(db.String(50), nullable=True)
    acc = db.Column(db.String(20), nullable=True)
    practice_owner = db.Column(db.String(20), nullable=True)
    hire_type = db.Column(db.String(20), nullable=True)
    new_hire = db.Column(db.String(15), nullable=True)
    rep_email = db.Column(db.String(40), nullable=True)
    skill = db.Column(db.String(50), nullable=True)
    # other_skill=db.Column(db.String(50), nullable=True)
    head_count = db.Column(db.Integer, nullable=True)
    loc = db.Column(db.String(20), nullable=True)
    # other_loc=db.Column(db.String(20), nullable=True)
    emp_grade = db.Column(db.String(30), nullable=True)
    res_status = db.Column(db.String(30), nullable=True)
    # join_date=db.Column(db.Date, nullable=True)
    action_pending = db.Column(db.String(30), nullable=True)
    ext_int = db.Column(db.String(10), nullable=True)
    dor = db.Column(db.Date, nullable=True)
    age=db.Column(db.Integer, nullable=True)
    Resource_name=db.Column(db.String(30), nullable=True)
    Resource_emp_id=db.Column(db.String(20), nullable=True)
    no_of_resumes=db.Column(db.Integer, nullable=True)
    screen_selects=db.Column(db.Integer, nullable=True)
    last_updated_by = db.Column(db.String(50), nullable=True)
    updated_date_time = db.Column(db.DateTime, nullable=True)
    
    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def __repr__(self):

        return f"""Demand('{self.project_name}','
                           {self.practice}','
                           {self.slt_owner}','
                           {self.owner}','
                            {self.last_updated_by}','
                           {self.updated_date_time}','
                          {self.dsr_id}','
                          {self.acc}','
                          {self.practice_owner}','
                          {self.hire_type}','
                          {self.new_hire}','
                          {self.rep_email}','
                          {self.skill}','
                          
                          {self.head_count}','
                          {self.loc}','
                          
                          {self.emp_grade}','
                          {self.res_status}','
                          {self.action_pending}','
                          {self.ext_int}','
                          {self.dor}','
                          {self.Resource_name}','
                          {self.Resource_emp_id}','
                          {self.no_of_resumes}','
                          {self.screen_selects}')"""


class Interview(db.Model):
    __tablename__ = "Interview"
    id = db.Column(db.Integer, primary_key=True)
    dsr_id = db.Column(db.String(50), nullable=True)
    res_name = db.Column(db.String(50), nullable=True)
    loc = db.Column(db.String(50), nullable=True)
    skill = db.Column(db.String(50), nullable=True)
    project_name = db.Column(db.String(50), nullable=True)
    final_select = db.Column(db.String(50), nullable=True)
    active_inactive = db.Column(db.String(50), nullable=True)
    ext_int = db.Column(db.String(50), nullable=True)
    r1_panel = db.Column(db.String(50), nullable=True)
    r1_date = db.Column(db.Date, nullable=True)
    r1_status = db.Column(db.String(50), nullable=True)
    r2_panel = db.Column(db.String(50), nullable=True)
    r2_date = db.Column(db.Date, nullable=True)
    r2_status = db.Column(db.String(50), nullable=True)
    current_status = db.Column(db.String(50), nullable=True)
    act_pending = db.Column(db.String(50), nullable=True)
    ops_action = db.Column(db.String(50), nullable=True)
    due_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.String(50), nullable=True)
    last_updated_by = db.Column(db.String(50), nullable=True)
    updated_date_time = db.Column(db.DateTime, nullable=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def __repr__(self):

        return f"""Interview('{self.id}','
                            {self.res_name}','
                            {self.dsr_id}','
                           {self.final_select}','
                           {self.active_inactive}','
                           {self.loc}','
                           {self.skill}','
                           {self.last_updated_by}','
                           {self.updated_date_time}','
                           {self.project_name}','
                          {self.ext_int}','
                          {self.r1_panel}','
                          {self.r1_date}','
                          {self.r1_status}','
                          {self.r2_panel}','
                          {self.r2_date}','
                          {self.r2_status}','
                          {self.current_status}','
                          {self.act_pending}','
                          {self.ops_action}','
                          {self.due_date}','
                          {self.remarks}')"""


class Commit(db.Model):
    __tablename__ = "commit_table"
    # project_id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(50), nullable=False)
    slt_owner = db.Column(db.String(50), nullable=True)
    practice = db.Column(db.String(50), nullable=True)
    quarter = db.Column(db.String(3), nullable=True)
    project_manager = db.Column(db.String(50), nullable=True)
    resource_name = db.Column(db.String(50), nullable=True)
    resource_country = db.Column(db.String(15), nullable=True)
    resource_level = db.Column(db.String(25), nullable=True)
    onshore_offshore = db.Column(db.String(20), nullable=True)
    fte = db.Column(db.Integer, nullable=True)
    revenue_daily_rate = db.Column(db.Float, nullable=False)
    adrc = db.Column(db.Float, nullable=True)

    start_date_commit = db.Column(db.Date, nullable=False)
    end_date_commit = db.Column(db.Date, nullable=False)

    days_jan = db.Column(db.Integer, nullable=False)
    days_feb = db.Column(db.Integer, nullable=False)
    days_mar = db.Column(db.Integer, nullable=False)
    days_apr = db.Column(db.Integer, nullable=False)
    days_may = db.Column(db.Integer, nullable=False)
    days_jun = db.Column(db.Integer, nullable=False)
    days_jul = db.Column(db.Integer, nullable=False)
    days_aug = db.Column(db.Integer, nullable=False)
    days_sep = db.Column(db.Integer, nullable=False)
    days_oct = db.Column(db.Integer, nullable=False)
    days_nov = db.Column(db.Integer, nullable=False)
    days_dec = db.Column(db.Integer, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)

    eur_jan = db.Column(db.Integer, nullable=False)
    eur_feb = db.Column(db.Integer, nullable=False)
    eur_mar = db.Column(db.Integer, nullable=False)
    eur_apr = db.Column(db.Integer, nullable=False)
    eur_may = db.Column(db.Integer, nullable=False)
    eur_jun = db.Column(db.Integer, nullable=False)
    eur_jul = db.Column(db.Integer, nullable=False)
    eur_aug = db.Column(db.Integer, nullable=False)
    eur_sep = db.Column(db.Integer, nullable=False)
    eur_oct = db.Column(db.Integer, nullable=False)
    eur_nov = db.Column(db.Integer, nullable=False)
    eur_dec = db.Column(db.Integer, nullable=False)

    total_revenue = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    cm = db.Column(db.Float, nullable=False)
    resource_wise_cm_percet = db.Column(db.Float, nullable=False)
    last_updated_by = db.Column(db.String(50), nullable=True)
    updated_date_time = db.Column(db.DateTime, nullable=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def __repr__(self):
        return f"""Commit('{self.project_name}','
                             {self.slt_owner}','
                             {self.practice}','
                             {self.quarter}','
                             {self.last_updated_by}','
                             {self.updated_date_time}','
                             {self.project_manager}','
                             {self.resource_name}','
                             {self.project_country}','
                             {self.resource_level}','
                             {self.onshore_offshore}','
                             {self.fte}','
                             {self.revenue_daily_rate}','
                             {self.ardc}','
                             {self.days_jan}','
                             {self.days_feb}','
                             {self.days_mar}','
                             {self.days_apr}','
                             {self.days_may}','
                             {self.days_jun}','
                             {self.days_jul}','
                             {self.days_aug}','
                             {self.days_sep}','
                             {self.days_oct}','
                             {self.days_nov}','
                             {self.days_dec}','
                             {self.total_days}','
                             {self.eur_jan}','
                             {self.eur_feb}','
                             {self.eur_mar}','
                             {self.eur_apr}','
                             {self.eur_may}','
                             {self.eur_jun}','
                             {self.eur_jul}','
                             {self.eur_aug}','
                             {self.eur_sep}','
                             {self.eur_oct}','
                             {self.eur_nov}','
                             {self.eur_dec}','
                             {self.total_revenue}','
                             {self.total_cost}','
                             {self.cm}','
                             {self.resource_wise_cm_percet}')"""


class WonDeals(db.Model):
    __tablename__ = "wondeals_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email_id=db.Column(db.String(50),nullable=False)
    project_id = db.Column(db.String(50), nullable=True)
    carryforward = db.Column(db.String(50), nullable=True)
    project_type=db.Column(db.String(50), nullable=True)
    email_id = db.Column(db.String(50), nullable=True)
    project_name = db.Column(db.String(50), nullable=False)
    slt_owner = db.Column(db.String(50), nullable=True)
    practice_owner = db.Column(db.String(50), nullable=True)
    practice = db.Column(db.String(50), nullable=True)
    quarter = db.Column(db.String(3), nullable=True)
    project_manager = db.Column(db.String(50), nullable=True)
    resource_name = db.Column(db.String(50), nullable=True)
    resource_country = db.Column(db.String(15), nullable=True)
    resource_level = db.Column(db.String(25), nullable=True)
    onshore_offshore = db.Column(db.String(20), nullable=True)
    project_country = db.Column(db.String(15), nullable=True)
    fte = db.Column(db.Integer, nullable=True)
    revenue_daily_rate = db.Column(db.Float, nullable=False)
    adrc = db.Column(db.Float, nullable=True)

    start_date_wondeals = db.Column(db.Date, nullable=False)
    end_date_wondeals = db.Column(db.Date, nullable=False)

    days_jan = db.Column(db.Integer, nullable=False)
    days_feb = db.Column(db.Integer, nullable=False)
    days_mar = db.Column(db.Integer, nullable=False)
    days_apr = db.Column(db.Integer, nullable=False)
    days_may = db.Column(db.Integer, nullable=False)
    days_jun = db.Column(db.Integer, nullable=False)
    days_jul = db.Column(db.Integer, nullable=False)
    days_aug = db.Column(db.Integer, nullable=False)
    days_sep = db.Column(db.Integer, nullable=False)
    days_oct = db.Column(db.Integer, nullable=False)
    days_nov = db.Column(db.Integer, nullable=False)
    days_dec = db.Column(db.Integer, nullable=False)
    total_days = db.Column(db.Integer, nullable=False)

    eur_jan = db.Column(db.Integer, nullable=False)
    eur_feb = db.Column(db.Integer, nullable=False)
    eur_mar = db.Column(db.Integer, nullable=False)
    eur_apr = db.Column(db.Integer, nullable=False)
    eur_may = db.Column(db.Integer, nullable=False)
    eur_jun = db.Column(db.Integer, nullable=False)
    eur_jul = db.Column(db.Integer, nullable=False)
    eur_aug = db.Column(db.Integer, nullable=False)
    eur_sep = db.Column(db.Integer, nullable=False)
    eur_oct = db.Column(db.Integer, nullable=False)
    eur_nov = db.Column(db.Integer, nullable=False)
    eur_dec = db.Column(db.Integer, nullable=False)

    total_revenue = db.Column(db.Float, nullable=False)
    total_cost = db.Column(db.Float, nullable=False)
    cm = db.Column(db.Float, nullable=False)
    resource_wise_cm_percet = db.Column(db.Float, nullable=False)
    last_updated_by = db.Column(db.String(50), nullable=True)
    updated_date_time = db.Column(db.DateTime, nullable=True)
    li_lr_id=db.Column(db.String(15),nullable=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]

    def __repr__(self):

        return f"""WonDeals('{self.email_id}','
                             {self.project_id}','
                             {self.carryforward}','
                             {self.project_type}','
                             {self.project_name}','
                             {self.last_updated_by}','
                             {self.updated_date_time}','
                             {self.slt_owner}','
                             {self.practice}','
                             {self.practice_owner}','
                             {self.quarter}','
                             {self.project_manager}','
                             {self.resource_name}','
                             {self.resource_country}','
                             {self.resource_level}','
                             {self.onshore_offshore}','
                             {self.fte}','
                             {self.project_country}','
                             {self.revenue_daily_rate}','
                             {self.adrc}','
                             {self.days_jan}','
                             {self.days_feb}','
                             {self.days_mar}','
                             {self.days_apr}','
                             {self.days_may}','
                             {self.days_jun}','
                             {self.days_jul}','
                             {self.days_aug}','
                             {self.days_sep}','
                             {self.days_oct}','
                             {self.days_nov}','
                             {self.days_dec}','
                             {self.total_days}','
                             {self.eur_jan}','
                             {self.eur_feb}','
                             {self.eur_mar}','
                             {self.eur_apr}','
                             {self.eur_may}','
                             {self.eur_jun}','
                             {self.eur_jul}','
                             {self.eur_aug}','
                             {self.eur_sep}','
                             {self.eur_oct}','
                             {self.eur_nov}','
                             {self.eur_dec}','
                             {self.total_revenue}','
                             {self.total_cost}','
                             {self.cm}','
                             {self.resource_wise_cm_percet}')"""

class Leaves(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    project_id = db.Column(db.String(50), nullable=False)
    email_id = db.Column(db.String(50), nullable=False)
    start_date=db.Column(db.Date,nullable=False)
    end_date=db.Column(db.Date,nullable=False)
    reason=db.Column(db.String(100),nullable=True)

      
    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]
    def __repr__(self):
        return f""""Leaves('{self.project_id}','
                            {self.email_id}','
                            
        ) """
class ResourceMaster(db.Model):
    __tablename__="resource_master"
    li_lr_id=db.Column(db.String(20),nullable=True)
    region=db.Column(db.String(20),nullable=True)
    first_name=db.Column(db.String(20),nullable=True)
    middle_name=db.Column(db.String(20),nullable=True)
    last_name=db.Column(db.String(20),nullable=True)
    nt_login_id=db.Column(db.String(20),nullable=True)
    global_date_joining=db.Column(db.Date,nullable=True)
    local_date_joining=db.Column(db.Date,nullable=True)
    email_id=db.Column(db.String(50),nullable=True,primary_key=True,unique=1)
    sub_practice=db.Column(db.String(50),nullable=True)
    organization=db.Column(db.String(20),nullable=True)
    designation=db.Column(db.String(20),nullable=True)
    base_location=db.Column(db.String(20),nullable=True)
    local_grade=db.Column(db.String(20),nullable=True)
    people_manager_name=db.Column(db.String(50),nullable=True)
    account_name=db.Column(db.String(50),nullable=True)
    project_number=db.Column(db.String(50),nullable=True)
    project_start_date=db.Column(db.String(50),nullable=True)
    project_rolloff_date=db.Column(db.String(50),nullable=True)
    billability=db.Column(db.String(50),nullable=True)
    last_project_code=db.Column(db.String(50),nullable=True)
    adrc=db.Column(db.Integer,nullable=True)
    slt_owners=db.Column(db.String(50),nullable=True)
    next_assignment=db.Column(db.String(50),nullable=True)
    remarks=db.Column(db.String(50),nullable=True)
    resign_date = db.Column(db.Date,nullable=True)
    last_working_date = db.Column(db.Date,nullable=True)

    def __iter__(self):
        values = vars(self)
        for attr in self.__mapper__.columns.keys():
            if attr in values:
                yield attr, values[attr]
    

# class CommitBookingForecast(db.Model):

#     commit_id = db.Column(db.Integer, primary_key=True)

#     project_id = db.Column(
#         db.Integer, db.ForeignKey("booking_forecast.project_id"), nullable=False
#     )
#     project_name = db.Column(
#         db.String(50), db.ForeignKey("booking_forecast.project_name"), nullable=False
#     )
#     practice = db.Column(
#         db.String(20), db.ForeignKey("booking_forecast.practice"), nullable=False
#     )
#     slt_owner = db.Column(
#         db.String(15), db.ForeignKey("booking_forecast.slt_owner"), nullable=False
#     )
#     practice_owner = db.Column(
#         db.String(15), db.ForeignKey("booking_forecast.practice_owner"), nullable=False
#     )
#     quarter = db.Column(
#         db.String(3), db.ForeignKey("booking_forecast.quarter"), nullable=False
#     )
#     sales_stage = db.Column(
#         db.String(20), db.ForeignKey("booking_forecast.sales_stage"), nullable=False
#     )
#     project_type = db.Column(
#         db.String(15), db.ForeignKey("booking_forecast.project_type"), nullable=False
#     )
#     region = db.Column(
#         db.String(15), db.ForeignKey("booking_forecast.region"), nullable=False
#     )
#     country = db.Column(
#         db.String(15), db.ForeignKey("booking_forecast.country"), nullable=False
#     )
#     win_prob = db.Column(
#         db.Integer, db.ForeignKey("booking_forecast.win_prob"), nullable=False
#     )
#     status = db.Column(
#         db.String(10), db.ForeignKey("booking_forecast.status"), nullable=False
#     )
#     currency = db.Column(
#         db.String(5), db.ForeignKey("booking_forecast.currency"), nullable=False
#     )
#     deal_value = db.Column(
#         db.Float, db.ForeignKey("booking_forecast.id"), nullable=True
#     )
#     deal_value_eur = db.Column(
#         db.Float, db.ForeignKey("booking_forecast.deal_value_eur"), nullable=True
#     )
#     start_date_deal = db.Column(
#         db.Date, db.ForeignKey("booking_forecast.start_date_deal"), nullable=False
#     )
#     end_date_deal = db.Column(
#         db.Date, db.ForeignKey("booking_forecast.end_date_deal"), nullable=False
#     )

#     resource = db.Column(db.String(30), nullable=False)
#     region = db.Column(db.String(15), nullable=False)
#     adrc = db.Column(db.Float, nullable=False)
#     cor = db.Column(db.Float, nullable=False)
#     onshore_offshore = db.Column(db.String(20), nullable=False)
#     resource_start_date = db.Column(db.Date, nullable=False)
#     resource_end_date = db.Column(db.Date, nullable=False)

# days_jan = db.Column(db.Integer, nullable=False)
# days_feb = db.Column(db.Integer, nullable=False)
# days_mar = db.Column(db.Integer, nullable=False)
# days_apr = db.Column(db.Integer, nullable=False)
# days_may = db.Column(db.Integer, nullable=False)
# days_jun = db.Column(db.Integer, nullable=False)
# days_jul = db.Column(db.Integer, nullable=False)
# days_aug = db.Column(db.Integer, nullable=False)
# days_sep = db.Column(db.Integer, nullable=False)
# days_oct = db.Column(db.Integer, nullable=False)
# days_nov = db.Column(db.Integer, nullable=False)
# days_dec = db.Column(db.Integer, nullable=False)

# total_days = db.Column(db.Integer, nullable=False)
# eur_jan = db.Column(db.Integer, nullable=False)
# eur_feb = db.Column(db.Integer, nullable=False)
# eur_mar = db.Column(db.Integer, nullable=False)
# eur_apr = db.Column(db.Integer, nullable=False)
# eur_may = db.Column(db.Integer, nullable=False)
# eur_jun = db.Column(db.Integer, nullable=False)
# eur_jul = db.Column(db.Integer, nullable=False)
# eur_aug = db.Column(db.Integer, nullable=False)
# eur_sep = db.Column(db.Integer, nullable=False)
# eur_oct = db.Column(db.Integer, nullable=False)
# eur_nov = db.Column(db.Integer, nullable=False)
# eur_dec = db.Column(db.Integer, nullable=False)

# total_revenue = db.Column(db.Float, nullable=False)
# total_cost = db.Column(db.Float, nullable=False)
# cm = db.Column(db.Float, nullable=False)
# resource_wise_cm_percet = db.Column(db.Float, nullable=False)

#     def __iter__(self):
#         values = vars(self)
#         for attr in self.__mapper__.columns.keys():
#             if attr in values:
#                 yield attr, values[attr]

#     def __repr__(self):
#         return f"""CommitBookingForecast('{self.project_id}','
#                                         {self.project_name}','
#                                         {self.practice}','
#                                         {self.slt_owner}','
#                                         {self.practice_owner}','
#                                         {self.quarter}','
#                                         {self.sales_stage}','
#                                         {self.project_type}','
#                                         {self.region}','
#                                         {self.country}','
#                                         {self.win_prob}','
#                                         {self.status}','
#                                         {self.currency}','
#                                         {self.deal_value}','
#                                         {self.start_date_deal}','
#                                         {self.end_date_deal}','
#                                         {self.resource}','
#                                         {self.region}','
#                                         {self.adrc}','
#                                         {self.cor}','
#                                         {self.onshore_offshore}','
#                                         {self.resource_start_date}','
#                                         {self.resource_end_date}
#                                         {self.days_jan}','
#                                         {self.days_feb}','
#                                         {self.days_mar}','
#                                         {self.days_apr}','
#                                         {self.days_may}','
#                                         {self.days_jun}','
#                                         {self.days_jul}','
#                                         {self.days_aug}','
#                                         {self.days_sep}','
#                                         {self.days_oct}','
#                                         {self.days_nov}','
#                                         {self.days_dec}','
#                                         {self.total_days}','
#                                         {self.eur_jan}','
#                                         {self.eur_feb}','
#                                         {self.eur_mar}','
#                                         {self.eur_apr}','
#                                         {self.eur_may}','
#                                         {self.eur_jun}','
#                                         {self.eur_jul}','
#                                         {self.eur_aug}','
#                                         {self.eur_sep}','
#                                         {self.eur_oct}','
#                                         {self.eur_nov}','
#                                         {self.eur_dec}','
#                                         {self.total_revenue}','
#                                         {self.total_cost}','
#                                         {self.cm}','
#                                         {self.resource_wise_cm_percet})"""


# BookingForecast(
#     project_id=12,
#     project_name="project_name",
#     practice="practice",
#     slt_owner="slt_owner",
#     practice_owner="practice_owner",
#     quarter="Q1",
#     sales_stage="sales_stage",
#     project_type="project_type",
#     region="region",
#     country="country",
#     win_prob=90,
#     status="status",deal_value_eur=23,
#     currency="eur",
#     deal_value=657,
#     start_date_deal=val1,
#     end_date_deal=val2,
# )


#  designation, region, adrc, cor, onshore_offshore, resource_start_date, resource_end_date, days_feb', 'days_mar', 'days_apr', 'days_may', 'days_jun', 'days_jul',
#        'days_aug', 'days_sep', 'days_oct', 'days_nov', 'days_dec',
#        'total_days', 'eur_jan', 'eur_feb', 'eur_mar', 'eur_apr', 'eur_may',
#        'eur_jun', 'eur_jul', 'eur_aug', 'eur_sep', 'eur_oct', 'eur_nov',
#        'eur_dec', 'total_revenue', 'total_cost', cm, resource_wise_cm_percet



