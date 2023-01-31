import datetime
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    BooleanField,
    TextAreaField,
    FloatField,
    DateField,
    SelectField,
    IntegerField,
    RadioField
)
from wtforms.validators import (
    DataRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from flask_excel_app import db,app
from flask_excel_app.models import User

app.app_context().push()
class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    # picture = FileField(
    #     "Update Profile Picture", validators=[FileAllowed(["jpg", "png"])]
    # )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    "That username is taken. Please choose a different one."
                )

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    "That email is taken. Please choose a different one."
                )


# class PostForm(FlaskForm):
#     title = StringField("Title", validators=[DataRequired()])
#     content = TextAreaField("Content", validators=[DataRequired()])
#     submit = SubmitField("Post")


class BookingForecastForm(FlaskForm):
    # project_id = StringField("Project_Id", validators=[DataRequired()])
    project_name = StringField("Project_Name", validators=[DataRequired()])
    practice = SelectField(
        "Practice",
        choices=[("", "--select value--"),("R&F", "R&F"), ("Compliance", "Compliance")],
        validators=[DataRequired()],
    )
    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    practice_owner = SelectField(
        "Practice_Owner",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Manoj Adhikari", "Manoj Adhikari"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    quarter = SelectField(
        "Quarter",
        choices=[("", "--select value--"),("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4")],
        validators=[DataRequired()],
    )
    sales_stage = SelectField(
        "Sales_Stage",
        choices=[
            ("", "--select value--"),
            ("1. Initiation stage", "1. Initiation stage"),
            ("2.Customer Discussion", "2.Customer Discussion"),
            ("3. Proposal Submitted", "Proposal Submitted"),
            ("4. Contract Negotiation", "4. Contract Negotiation"),
            ("5. Won-Pending", "5. Won-Pending"),
            ("6. Won", "6. Won"),
        ],
        validators=[DataRequired()],
    )
    project_type = SelectField(
        "Project_Type",
        choices=[
            ("", "--select value--"),
            ("FP", "FP"),
            ("T&M", "T&M"),
            ("FC", "FC"),
            ("TM", "TM"),
        ],
        validators=[DataRequired()],
    )
    region = SelectField(
        "Region",
        choices=[
            ("", "--select value--"),
            ("APAC", "APAC"),
            ("NA", "NA"),
            ("US", "US"),
            ("Europe", "Europe"),
            ("UAE", "UAE"),
            ("AU/NZ", "AU/NZ"),
            ("SG", "SG"),
            ("PH", "PH"),
        ],
        validators=[DataRequired()],
    )
    country = SelectField(
        "Country",
        choices=[
            ("", "--select value--"),
            ("AU", "Australia"),
            ("CA", "Canada"),
            ("IN", "India"),
            ("PH", "Philippines"),
            ("UK", "UK"),
            ("USA", "USA"),
            ("NL", "Netherlands"),
            ("SG", "Singapore"),
        ],
        validators=[DataRequired()],
    )
    win_prob = FloatField(
        "Win_Prob", validators=[DataRequired(), NumberRange(min=0.0, max=100.0)]
    )
    currency = SelectField(
        "Currency",
        choices=[
            ("", "--select value--"),
            ("PHP", "PHP"),
            ("AUD", "AUD"),
            ("USD", "USD"),
            ("SGD", "SGD"),
            ("MYR", "MYR"),
        ],
        validators=[DataRequired()],
    )
    deal_value = FloatField("Deal_value", validators=[DataRequired()])
    # start_date_deal = DateField(
    #     "Start_Date", format="%Y-%m-%d", validators=[DataRequired()]
    # )
    # end_date_deal = DateField(
    #     "End_Date", format="%Y-%m-%d", validators=[DataRequired()]
    # )
    submit = SubmitField("submit")


class BookingForecastUpdateForm(FlaskForm):
    # project_id = StringField("Project_Id", validators=[DataRequired()])
    project_name = StringField("Project_Name", validators=[DataRequired()])
    practice = SelectField(
        "Practice",
        choices=[("", "--select value--"),("R&F", "R&F"), ("Compliance", "Compliance")],
        validators=[DataRequired()],
    )
    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    practice_owner = SelectField(
        "Practice_Owner",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Manoj Adhikari", "Manoj Adhikari"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    quarter = SelectField(
        "Quarter",
        choices=[("", "--select value--"),("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4")],
        validators=[DataRequired()],
    )
    sales_stage = SelectField(
        "Sales_Stage",
        choices=[
            ("", "--select value--"),
            ("1. Initiation stage", "1. Initiation stage"),
            ("2.Customer Discussion", "2.Customer Discussion"),
            ("3. Proposal Submitted", "Proposal Submitted"),
            ("4. Contract Negotiation", "4. Contract Negotiation"),
            ("5. Won-Pending", "5. Won-Pending"),
            ("6. Won", "6. Won"),
        ],
        validators=[DataRequired()],
    )
    project_type = SelectField(
        "Project_Type",
        choices=[
            ("", "--select value--"),
            ("FP", "FP"),
            ("T&M", "T&M"),
            ("FC", "FC"),
            ("TM", "TM"),
        ],
        validators=[DataRequired()],
    )
    region = SelectField(
        "Region",
        choices=[
            ("", "--select value--"),
            ("APAC", "APAC"),
            ("NA", "NA"),
            ("US", "US"),
            ("Europe", "Europe"),
            ("UAE", "UAE"),
            ("AU/NZ", "AU/NZ"),
            ("SG", "SG"),
            ("PH", "PH"),
        ],
        validators=[DataRequired()],
    )
    country = SelectField(
        "Country",
        choices=[
            ("", "--select value--"),
            ("AU", "Australia"),
            ("CA", "Canada"),
            ("IN", "India"),
            ("PH", "Philippines"),
            ("UK", "UK"),
            ("USA", "USA"),
            ("NL", "Netherlands"),
            ("SG", "Singapore"),
        ],
        validators=[DataRequired()],
    )
    win_prob = FloatField(
        "Win_Prob", validators=[ NumberRange(min=0.0, max=100.0)]
    )
    currency = SelectField(
        "Currency",
        choices=[
            ("", "--select value--"),
            ("PHP", "PHP"),
            ("AUD", "AUD"),
            ("USD", "USD"),
            ("SGD", "SGD"),
            ("MYR", "MYR"),
        ],
        validators=[DataRequired()],
    )
    deal_value = FloatField("Deal_value", validators=[DataRequired()])
    # start_date_deal = DateField(
    #     "Start_Date", format="%Y-%m-%d", validators=[DataRequired()]
    # )
    # end_date_deal = DateField(
    #     "End_Date", format="%Y-%m-%d", validators=[DataRequired()]
    # )
    submit = SubmitField("submit")



class CommitForm(FlaskForm):
    project_name = StringField("Project_Name", validators=[DataRequired()])
    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    practice = SelectField(
        "Practice",
        choices=[
            ("", "--select value--"),
            ("R&F", "R&F"),
            ("Compliance", "Compliance"),
            
        ],
        validators=[DataRequired()],
    )
    quarter = SelectField(
        "Quarter",
        choices=[("", "--select value--"),("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4")],
        validators=[DataRequired()],
    )
    project_manager = SelectField(
        "Project Manager",
        choices=[
            ("", "--select value--"),
            ("Balaji Chetana", "Balaji Chetana"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Sudarshan VS","Sudarshan VS"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerag Raveendran","Sreerag Raveendran"),
            ("Puneet Chandra","Puneet Chandra"),
            ("Manoj Adhikari","Manoj Adhikari"),
            ("Ashutosh Agarwal","Ashutosh Agarwal"),
            ("Vikas Tiwari","Vikas Tiwari"),
            ("Prachi Shah","Prachi Shah"),
        ],
        validators=[DataRequired()],
    )
    resource_name = StringField("Resource Name")
    resource_country = SelectField(
        "Country",
        choices=[
            ("", "--select value--"),
            ("IN_IN", "IN_IN"),
            ("NA_US", "NA_US"),
            ("NA_US_LTT/STT", "NA_US_LTT/STT"),
            #("NA_US_NEW_STT/I_gate_landed", "NA_US_NEW_STT/I_gate_landed"),
            ("NA_CA_Local", "NA_CA_Local"),
            ("NA_CA_Landed", "NA_CA_Landed"),
            ("UK_GB", "UK_GB"),
            ("UK_GB_LTT/STT", "UK_GB_LTT/STT"),
            ("UK_Nearshore", "UK_Nearshore"),
            ("UK_ZA", "UK_ZA"),
            ("APAC_HK", "APAC_HK"),
            ("APAC_SG", "APAC_SG"),
            ("APAC_AE", "APAC_AE"),
            ("APAC_MY", "APAC_MY"),
            ("APAC_TW", "APAC_TW"),
            ("APAC_SA", "APAC_SA"),
            ("DC_CH", "DC_CH"),
            ("DC_PH", "DC_PH"),
        ],
        validators=[DataRequired()],
    )
    resource_level = SelectField(
        "Level",
        choices=[
            ("", "--select value--"),
            ("SA", "Senior Analyst"),
            ("SE", "Software Engineer"),
            ("SSE", "Senior Software Engineer"),
            ("AC", "Assoc Consultant"),
            ("C", "Consultant"),
            ("SC", "Sr Consultant"),
            ("M", "Manager"),
            ("SM", "Sr Manager"),
            ("PM", "Portfolio Manager"),
            ("D", "Director"),
            ("SD", "Sr Director"),
            ("VP", "Vice President"),
            ("EVP", "Executive Vice President"),
        ],
        validators=[DataRequired()],
    )
    onshore_offshore = SelectField(
        "Onshore / Offshore",
        choices=[
            ("", "--select value--"),
            ("Onsite", "Onsite"),
            ("Offshore", "Offshore"),
        ],
        validators=[DataRequired()],
    )
    fte = IntegerField("FTE", validators=[DataRequired()])
    start_date_commit = DateField(
        "Start Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    end_date_commit = DateField(
        "End Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    revenue_daily_rate = FloatField("COR", validators=[DataRequired()])
    submit = SubmitField("Add resource")


class WonDealsForm(FlaskForm):
    email_id = StringField("Email", validators=[DataRequired(), Email()])
    project_name = StringField("Project_Name", validators=[DataRequired()])
    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
        validators=[DataRequired()],
    )
    practice_owner = SelectField(
        "Practice Owner",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
            ("Manoj Adhikari", "Manoj Adhikari"),
            ("Vikas Tiwari", "Vikas Tiwaris"),
        ],
        validators=[DataRequired()],
    )
    practice = SelectField(
        "Practice",
        choices=[
            ("", "--select value--"),
            ("R&F", "R&F"),
            ("Compliance", "Compliance"),
        ],
        validators=[DataRequired()],
    )
    quarter = SelectField(
        "Quarter",
        choices=[("", "--select value--"),("Q1", "Q1"), ("Q2", "Q2"), ("Q3", "Q3"), ("Q4", "Q4")],
        validators=[DataRequired()],
    )
    project_manager = SelectField(
        "Project Manager",
        choices=[
            ("", "--select value--"),
            ("Balaji Chetana", "Balaji Chetana"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Sudarshan VS","Sudarshan VS"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerag Raveendran","Sreerag Raveendran"),
            ("Puneet Chandra","Puneet Chandra"),
            ("Manoj Adhikari","Manoj Adhikari"),
            ("Ashutosh Agarwal","Ashutosh Agarwal"),
            ("Vikas Tiwari","Vikas Tiwari"),
            ("Prachi Shah","Prachi Shah"),
        ],
        validators=[DataRequired()],
    )
    resource_name = StringField("Resource Name")
    resource_country = SelectField(
        "Country",
        choices=[
            ("", "--select value--"),
            ("IN_IN", "IN_IN"),
            ("NA_US", "NA_US"),
            ("NA_US_LTT/STT", "NA_US_LTT/STT"),
            #("NA_US_NEW_STT/I_gate_landed", "NA_US_NEW_STT/I_gate_landed"),
            ("NA_CA_Local", "NA_CA_Local"),
            ("NA_CA_Landed", "NA_CA_Landed"),
            ("UK_GB", "UK_GB"),
            ("UK_GB_LTT/STT", "UK_GB_LTT/STT"),
            ("UK_Nearshore", "UK_Nearshore"),
            ("UK_ZA", "UK_ZA"),
            ("APAC_HK", "APAC_HK"),
            ("APAC_SG", "APAC_SG"),
            ("APAC_AE", "APAC_AE"),
            ("APAC_MY", "APAC_MY"),
            ("APAC_TW", "APAC_TW"),
            ("APAC_SA", "APAC_SA"),
            ("DC_CH", "DC_CH"),
            ("DC_PH", "DC_PH"),
        ],
        validators=[DataRequired()],
    )
    resource_level = SelectField(
        "Level",
        choices=[
            ("", "--select value--"),
            ("SA", "Senior Analyst"),
            ("SE", "Software Engineer"),
            ("SSE", "Senior Software Engineer"),
            ("AC", "Assoc Consultant"),
            ("C", "Consultant"),
            ("SC", "Sr Consultant"),
            ("M", "Manager"),
            ("SM", "Sr Manager"),
            ("PM", "Portfolio Manager"),
            ("D", "Director"),
            ("SD", "Sr Director"),
            ("VP", "Vice President"),
            ("EVP", "Executive Vice President"),
        ],
        validators=[DataRequired()],
    )
    onshore_offshore = SelectField(
        "Onshore / Offshore",
        choices=[
            ("", "--select value--"),
            ("Onsite", "Onsite"),
            ("Offshore", "Offshore"),
        ],
        validators=[DataRequired()],
    )
    project_country = SelectField(
        "Project Country",
        choices=[
            ("", "--select value--"),
            ("IN", "IN"),
            ("US", "US"),
            ("AU", "AU"),
            ("CA", "CA"),
            ("MY", "MY"),
            ("PH", "PH"),
            ("SG", "SG"),
            ("TH", "TH"),
            ("UK", "UK"),
            ("TW", "TW"),
        ],
        validators=[DataRequired()],
    )
    fte = IntegerField("FTE", validators=[DataRequired()])
    start_date_wondeals = DateField(
        "Start Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    end_date_wondeals = DateField(
        "End Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    revenue_daily_rate = FloatField("COR", validators=[DataRequired()])
    project_id = StringField("Project Id", validators=[DataRequired()])
    carryforward = SelectField(
        "Carry Forward/New/Ext",
        choices=[
            ("", "--select value--"),
            ("Carry Forward", "Carry Forward"),
            ("New", "New"),
            ("Ext", "Ext"),
        ],
        validators=[DataRequired()],
    )
    project_type = SelectField(
        "Project Type",
        choices=[
            ("", "--select value--"),
            ("T&M", "T&M"),
            ("FP", "FP"),
           
        ],
        validators=[DataRequired()],
    )

    submit = SubmitField("Add resource")


class BookingForecastProjectIdForm(FlaskForm):
    project_name = StringField("Project_Name", validators=[DataRequired()])
    submit = SubmitField("submit")


class DemandForm(FlaskForm):
    project_name = StringField(
        "Account /Project Name",
        validators=[DataRequired()],
    )

    practice = SelectField(
        "Practice",
        choices=[("", "--select value--"),("R&F", "R&F"), ("Compliance", "Compliance")],
        validators=[DataRequired()],
    )

    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
            ("Chetana Balaji", "Chetana Balaji"),
            ("Manoj Adikari", "Manoj Adikari"),
        ],
        validators=[DataRequired()],
    )
    owner = SelectField(
        "Owner",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Chetana Balaji", "Chetana Balaji"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
            ("Manoj Adikari", "Manoj Adikari"),
        ],
        validators=[DataRequired()],
    )

    dsr_id = StringField("My Hire Id/DSR Req Id", validators=[DataRequired()])

    acc = StringField(
        "Account",
        validators=[DataRequired()],
    )

    practice_owner = SelectField(
        "Practice Head",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
            ("Chetana Balaji", "Chetana Balaji"),
            ("Manoj Adikari", "Manoj Adikari"),
        ],
        validators=[DataRequired()],
    )

    hire_type = SelectField(
        "Hire Type",
        choices=[
            ("", "--select value--"),
            ("Proactive Hire", "Proactive Hire"),
            ("Account Hire", "Account Hire"),
        ],
        validators=[DataRequired()],
    )

    new_hire = SelectField(
        "Replacement/ New Hire",
        choices=[
            ("", "--select value--"),
            ("Replacement Hire", "Replacement Hire"),
            ("New Hire", "New Hire"),
        ],
        validators=[DataRequired()],
    )
    rep_email = StringField(
        "Replacement Personal Email",
        validators=[DataRequired()],
    )

    skill = StringField(
        "Skill",
        validators=[DataRequired()],
    )

    head_count = IntegerField(
        "Head Count",
        validators=[DataRequired()],
    )
    """deal_status = SelectField("Deal Status", 
    choices=[
            ("", "--select value--"),
            ("Won", "Won"),
            ("Closed", "Closed"),
            ("Hold", "Hold"),
            ("Pending", "Pending")
        ],
        validators=[DataRequired()])
   """

    loc = StringField("Location", validators=[DataRequired()])

    emp_grade = SelectField(
        "Employee Grade",
        choices=[
             ("", "--select value--"),
            ("SA", "Senior Analyst"),
            ("SE", "Software Engineer"),
            ("SSE", "Senior Software Engineer"),
            ("AC", "Assoc Consultant"),
            ("C", "Consultant"),
            ("SC", "Sr Consultant"),
            ("M", "Manager"),
            ("SM", "Sr Manager"),
            ("PM", "Portfolio Manager"),
            ("D", "Director"),
            ("SD", "Sr Director"),
            ("VP", "Vice President"),
            ("EVP", "Executive Vice President"),
        ],
        validators=[DataRequired()],
    )

    res_status = SelectField(
        "Resource Status",
        choices=[
            ("", "--select value--"),
            ("Closed", "Closed"),
            ("Pending Start", "Pending Start"),
            ("Hold", "Hold"),
            ("Joined", "Joined"),
            ("Profiles Screening", "Profiles Screening"),
            ("R-1-WIP", "R-1-WIP"),
            ("R-1-Select", "R-1-Select"),
            ("R-2-WIP", "R-2-WIP"),
            ("R-2-Select", "R-2-Select"),
            ("Client Interview-WIP", "Client Interview-WIP"),
            ("Client Select", "Client Select"),
            ("Offer WIP", "Offer WIP"),
            ("Fitment Pending", "Fitment Pending"),
            ("Offer approved", "Offer approved"),
            ("Allocated", "Allocated"),
            ("Cancelled", "Cancelled"),
        ],
        validators=[DataRequired()],
    )

    """join_date = DateField(
        "Joining Date", format="%Y-%m-%d", validators=[DataRequired()]
    )"""
    action_pending = SelectField(
        "Action Pending With",
        choices=[
            ("", "--select value--"),
            ("Ops", "Ops"),
            ("Candidate", "Candidate"),
            ("HR", "HR"),
            ("Panel", "Panel"),
            ("Account", "Account"),
            ("Practice Head", "Practice Head"),
        ],
        validators=[],
    )

    ext_int = SelectField(
        "External/ Internal",
        choices=[
            ("External", "External"),
            ("Internal", "Internal"),
        ],
        validators=[DataRequired()],
    )
    go_to_commit = SubmitField("Go to Commit / Wondeals")
    
    submit = SubmitField("Submit")
    

    dor = DateField("Date of Requisition", 
    format="%Y-%m-%d", 
    validators=[DataRequired()],

    )

    Resource_name = StringField("Resource Name")

    Resource_emp_id =  IntegerField("Resource Employee Id")
    no_of_resumes =  IntegerField("No. Of Resumes shared")
    screen_selects =  IntegerField("Screen Selects")


class InterviewForm(FlaskForm):
    res_name = StringField(
        "Resource Name",
        validators=[DataRequired()],
    )
    loc = StringField(
        "Location",
        validators=[DataRequired()],
    )
    skill = StringField(
        "Skill",
        validators=[DataRequired()],
    )
    dsr_id = StringField(
        "DSR ID",
        validators=[DataRequired()],
    )
    active_inactive = StringField(
        "Active/Inactive",
        validators=[DataRequired()],
    )
    final_select = StringField(
        "Final Select",
        validators=[DataRequired()],
    )
    project_name = StringField(
        "Account /Project Name",
        validators=[DataRequired()],
    )
    ext_int = SelectField(
        "External/ Internal",
        choices=[
            ("External", "External"),
            ("Internal", "Internal"),
        ],
        validators=[DataRequired()],
    )
    r1_panel = StringField(
        "R-1 Panel",
        validators=[DataRequired()],
    )
    r1_date = DateField("R-2 Date", format="%Y-%m-%d", validators=[DataRequired()])
    r1_status = StringField(
        "R-1 Status",
        validators=[DataRequired()],
    )
    r2_panel = StringField(
        "R-2 Panel",
        validators=[DataRequired()],
    )
    r2_date = DateField("R-2 Date", format="%Y-%m-%d", validators=[DataRequired()])
    r2_status = StringField(
        "R-2 Status",
        validators=[DataRequired()],
    )
    current_status = StringField(
        "Current Status",
        validators=[DataRequired()],
    )
    act_pending = StringField(
        "Action pending",
        validators=[DataRequired()],
    )
    ops_action = StringField(
        "Ops Action",
        validators=[DataRequired()],
    )
    due_date = DateField("Due Date", format="%Y-%m-%d", validators=[DataRequired()])
    remarks = StringField(
        "Remarks",
        validators=[DataRequired()],
    )

    submit = SubmitField("Submit")
    go_to_commit = SubmitField("Go to commit / wondeals")

class BookingForecastSummaryForm(FlaskForm):
    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerag Raveendran", "Sreerag Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
    )
    quarter = SelectField(
        "Quarter",
        choices=[
            ("", "--select value--"),
            ("Q1", "Q1"),
            ("Q2", "Q2"),
            ("Q3", "Q3"),
            ("Q4", "Q4"),
        ],
    )
    submit = SubmitField("submit")


class CommitSummaryForm(FlaskForm):
    practice = SelectField(
        "Practice",
        choices=[
            ("", "--select value--"),
            ("Risk & Finance", "Risk & Finance"),
            ("Compliance", "Compliance"),
        ],
    )

    quarter = SelectField(
        "Quarter",
        choices=[
            ("", "--select value--"),
            ("Q1", "Q1"),
            ("Q2", "Q2"),
            ("Q3", "Q3"),
            ("Q4", "Q4"),
        ],
    )

   

    submit = SubmitField("submit")


class WonDealsSummaryForm(FlaskForm):
    practice = SelectField(
        "Practice",
        choices=[
            ("", "--select value--"),
            ("R&F", "R&F"),
            ("Compliance", "Compliance"),
        ],
    )

    project_country= SelectField(
        "Project Country",
         choices=[
            ("", "--select value--"),
            ("IN", "IN"),
            ("US", "US"),
            ("AU", "AU"),
            ("CA", "CA"),
            ("MY", "MY"),
            ("PH", "PH"),
            ("SG", "SG"),
            ("TH", "TH"),
            ("UK", "UK"),
            ("TW", "TW"),
         ],
    )

    slt_owner = SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
       
    )

    
    submit = SubmitField("submit")

class DemandSummaryForm(FlaskForm):
    practice = SelectField(
        "Practice",
        choices=[
            ("", "--select value--"),
            ("R&F", "R&F"),
            ("Compliance", "Compliance"),
        ],
    )

    slt_owner=SelectField(
        "SLT",
        choices=[
            ("", "--select value--"),
            ("Shailesh Rao", "Shailesh Rao"),
            ("Prachi Shah", "Prachi Shah"),
            ("Mahesh Haridasan", "Mahesh Haridasan"),
            ("Jamshir Wadia", "Jamshir Wadia"),
            ("Sreerang Raveendran", "Sreerang Raveendran"),
            ("Deepak Satyaprasad", "Deepak Satyaprasad"),
            ("Ashutosh Agarwal", "Ashutosh Agarwal"),
        ],
       
    )

    

class leaves_form(FlaskForm):
    project_id=StringField("project_id",validators=[DataRequired()])
    email_id=StringField("email_id",validators=[DataRequired()])
    start_date=DateField("start_date")
    end_date=DateField("end_date")
    reason=TextAreaField('reason')
    submit = SubmitField("apply for leave")


class InterviewSummaryForm(FlaskForm):
    project_name=SelectField(
    "Project Name",
        choices=[
            ("", "--select value--"),
            
        ],
       
    )
class Booking_forecast_filter(FlaskForm):
    slt_owner = SelectField( "slt_owner", 
    choices=[], 
    validators=[DataRequired()], )

class Commit_filter(FlaskForm):
    slt_owner=SelectField("slt_owner",
    choices=[],
    validators=[DataRequired()])
    project_manager=SelectField("project_manager",
    choices=[],
    validators=[DataRequired()])
    others=StringField("slt_owner")

class Wondeals_filter(FlaskForm):
    project_id=StringField("project_id",validators=[DataRequired()])
    project_name=StringField("project_name",validators=[DataRequired()])
    slt=SelectField("slt_owner",
    choices=[])
    practice_owner=SelectField("practice_owner",
    choices=[])
    project_manager=SelectField("project_manager",
    choices=[])

class Resource_Master_form(FlaskForm):

    li_lr_id=StringField('li_lr_id',validators=[DataRequired()])
    region=SelectField('region',
    choices=
            [('IN', 'IN_IN'),
            ('US', 'NA_US'),
            ('NA_US_LTT/STT', 'NA_US_LTT/STT'),
            ('NA_US_NEW_STT/I_gate_landed ', 'NA_US_NEW_STT/I_gate_landed '),
            ('NA_CA_Local', 'NA_CA_Local'),
            ('NA_CA_Landed', 'NA_CA_Landed'),
            ('UK_GB', 'UK_GB'),
            ('UK_GB_LTT/STT', 'UK_GB_LTT/STT'),
            ('UK_Nearshore', 'UK_Nearshore'),
            ('UK_ZA', 'UK_ZA'),
            ('HK', 'APAC_HK'),
            ('SG', 'APAC_SG'),
            ('AE', 'APAC_AE'),
            ('MY', 'APAC_MY'),
            ('TW', 'APAC_TW'),
            ('SA', 'APAC_SA'),
            ('CH', 'DC_CH'),
            ('PH', 'DC_PH')],
            validators=[DataRequired()],
    )
    first_name=StringField('first_name',validators=[DataRequired()])
    middle_name=StringField('middle_name')
    last_name=StringField('last_name')
    nt_login_id=StringField('nt_login_id',validators=[DataRequired()])
    global_date_joining=DateField('global_date_joining',validators=[DataRequired()])
    local_date_joining=DateField('local_date_joining',validators=[DataRequired()])
    email_id = StringField('email_id',validators=[DataRequired()])
    sub_practice=SelectField('sub_practice',
            choices=[
                    ('Select the value','Select the value'),
                    ('GP-TRN-R&F', 'GP-TRN-R&F'),
                    ('GP-TRN-CMP', 'GP-TRN-CMP')],
                    validators=[DataRequired()])
    organization=StringField('organization',validators=[DataRequired()])
    designation = SelectField('designation',
    choices =[
        ('select a value ','select a value '),
        ('Associate Consultant', 'Associate Consultant'),
        ('Consultant', 'Consultant'),
        ('Director', 'Director'),
        ('Manager', 'Manager'),
        ('Portfolio Manager', 'Portfolio Manager'),
        ('Senior Consultant', 'Senior Consultant'),
        ('Senior Director', 'Senior Director'),
        ('Senior Manager', 'Senior Manager'),
        ('Senior Software Engineer', 'Senior Software Engineer'),
        ('Software Engineer', 'Software Engineer')] ,
        validators=[DataRequired()])
    local_grade=SelectField('local_grade',
    choices=[
            ('A4', 'A4'),
            ('A5', 'A5'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('C1', 'C1'),
            ('C2', 'C2'),
            ('D1', 'D1'),
            ('D2', 'D2'),
            ('E1', 'E1'),
            ('E2', 'E2'),
            ('U', 'U')],validators=[DataRequired()])
    status_project=RadioField('status_project',choices=[('allocated','allocated'),('unallocated','unallocated')])
    people_manager_name=StringField('people_manager_name',validators=[DataRequired()])
    account_name=StringField('account_name',validators=[DataRequired()])
    project_number = StringField('project_number',validators=[DataRequired()])
    project_start_date=DateField('project_start_date',default=datetime.datetime.strptime('9999-12-31','%Y-%m-%d').date())
    
    project_rolloff_date=DateField('project_rolloff_date',default=datetime.datetime.strptime('9999-12-31','%Y-%m-%d').date())
    billability=SelectField('billability',
    choices=[("","select a value"),("billable","billable"),
            ("non-billable","non-billable")],validators=[DataRequired()])
    last_project_code=StringField('last_project_code')
    next_assignment = SelectField('next_assignment',choices=[("","select a value"),
                                                            ('Extension','Extension'),
                                                            ('New Assignment','New Assignment'),
                                                            ('No Plan','No Plan')])
    remarks=TextAreaField('remarks')
    last_working_date=DateField('last_working_date')
    submit=SubmitField("submit to resource master")

class Resource_Update(FlaskForm):

    li_lr_id=StringField('li_lr_id',validators=[DataRequired()])
    region=SelectField('region',
    choices=
            [('IN', 'IN_IN'),
            ('US', 'NA_US'),
            ('NA_US_LTT/STT', 'NA_US_LTT/STT'),
            ('NA_US_NEW_STT/I_gate_landed ', 'NA_US_NEW_STT/I_gate_landed '),
            ('NA_CA_Local', 'NA_CA_Local'),
            ('NA_CA_Landed', 'NA_CA_Landed'),
            ('UK_GB', 'UK_GB'),
            ('UK_GB_LTT/STT', 'UK_GB_LTT/STT'),
            ('UK_Nearshore', 'UK_Nearshore'),
            ('UK_ZA', 'UK_ZA'),
            ('HK', 'APAC_HK'),
            ('SG', 'APAC_SG'),
            ('AE', 'APAC_AE'),
            ('MY', 'APAC_MY'),
            ('TW', 'APAC_TW'),
            ('SA', 'APAC_SA'),
            ('CH', 'DC_CH'),
            ('PH', 'DC_PH')],
            validators=[DataRequired()],
    )
    first_name=StringField('first_name',validators=[DataRequired()])
    middle_name=StringField('middle_name')
    last_name=StringField('last_name')
    nt_login_id=StringField('nt_login_id',validators=[DataRequired()])
    global_date_joining=DateField('global_date_joining',validators=[DataRequired()])
    local_date_joining=DateField('local_date_joining',validators=[DataRequired()])
    email_id = StringField('email_id',validators=[DataRequired()])
    sub_practice=SelectField('sub_practice',
            choices=[
                    ('Select the value','Select the value'),
                    ('GP-TRN-R&F', 'GP-TRN-R&F'),
                    ('GP-TRN-CMP', 'GP-TRN-CMP')],
                    validators=[DataRequired()])
    organization=StringField('organization',validators=[DataRequired()])
    designation = SelectField('designation',
    choices =[
        ('Associate Consultant', 'Associate Consultant'),
        ('Consultant', 'Consultant'),
        ('Director', 'Director'),
        ('Manager', 'Manager'),
        ('Portfolio Manager', 'Portfolio Manager'),
        ('Senior Consultant', 'Senior Consultant'),
        ('Senior Director', 'Senior Director'),
        ('Senior Manager', 'Senior Manager'),
        ('Senior Software Engineer', 'Senior Software Engineer'),
        ('Software Engineer', 'Software Engineer')] ,
        validators=[DataRequired()])
    status_project=RadioField('status_project',choices=[('allocated','allocated'),('unallocated','unallocated')])
    
    local_grade=SelectField('local_grade',
    choices=[
            ('A4', 'A4'),
            ('A5', 'A5'),
            ('B1', 'B1'),
            ('B2', 'B2'),
            ('C1', 'C1'),
            ('C2', 'C2'),
            ('D1', 'D1'),
            ('D2', 'D2'),
            ('E1', 'E1'),
            ('E2', 'E2'),
            ('U', 'U')],validators=[DataRequired()])
    people_manager_name=StringField('people_manager_name',validators=[DataRequired()])
    account_name=StringField('account_name',validators=[DataRequired()])
    project_number = StringField('project_number',validators=[DataRequired()])
    project_start_date=DateField('project_start_date')
    status_project=RadioField('status_project',choices=[('allocated','allocated'),('unallocated','unallocated')])
    project_rolloff_date=DateField('project_rolloff_date')
    billability=SelectField('billability',
    choices=[("","select a value"),("billable","billable"),
            ("non-billable","non-billable")],validators=[DataRequired()])
    last_project_code=StringField('last_project_code')
    next_assignment = SelectField('next_assignment',choices=[("","select a value"),
                                                            ('Extension','Extension'),
                                                            ('New Assignment','New Assignment'),
                                                            ('No Plan','No Plan')],validators=[DataRequired()])
    remarks=TextAreaField('remarks')
    resign_date=DateField('resign_date')
    submit=SubmitField("Update")