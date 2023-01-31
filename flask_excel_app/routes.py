from itertools import count
import json
import os
import secrets
from flask import render_template, url_for, flash, redirect, request, abort
from flask_excel_app import app, db, bcrypt
from flask_excel_app.forms import (
    Commit_filter,
    RegistrationForm,
    LoginForm,
    Resource_Master_form,
    Resource_Update,
    UpdateAccountForm,
    BookingForecastForm,
    BookingForecastProjectIdForm,
    CommitForm,
    WonDealsForm,
    DemandForm,
    InterviewForm,
    BookingForecastSummaryForm,
    CommitSummaryForm,
    WonDealsSummaryForm,
    BookingForecastUpdateForm,
    DemandSummaryForm,
    leaves_form,
    InterviewSummaryForm,
    Wondeals_filter,
    Booking_forecast_filter
)
from flask_excel_app.models import (
    Leaves,
    User,
    BookingForecast,
    Commit,
    WonDeals,
    Demand,
    Interview,
    ResourceMaster,
    
)
from flask_login import login_user, current_user, logout_user, login_required
from openpyxl import load_workbook

from flask import session
from sqlalchemy.sql import func

import pandas as pd
import numpy as np
from datetime import datetime, timedelta,date
from dateutil import rrule


class Flask_Project_data:
    holidays_list = {
        "US": [
            "30-May-23",
            "04-Jul-23",
            "05-Sep-23",
            "24-Nov-23",
            "25-Nov-23",
            "26-Dec-23",
        ],
        "GB": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "UK": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "Ne": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "ZA": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "SG": [
            "01-Jan-23",
            "01-Feb-23",
            "02-Feb-23",
            "15-Apr-23",
            "01-May-23",
            "02-May-23",
            "03-May-23",
            "15-May-23",
            "16-May-23",
            "10-Jul-23",
            "11-Jul-23",
            "09-Aug-23",
            "24-Oct-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "PH": [
            "01-Jan-23",
            "01-Feb-23",
            "25-Feb-23",
            "09-Apr-23",
            "14-Apr-23",
            "15-Apr-23",
            "16-Apr-23",
            "01-May-23",
            "12-Jun-23",
            "21-Aug-23",
            "29-Aug-23",
            "01-Nov-23",
            "30-Nov-23",
            "08-Dec-23",
            "25-Dec-23",
            "30-Dec-23",
        ],
        "NL": [
            "01-Jan-23",
            "15-Apr-23",
            "17-Apr-23",
            "18-Apr-23",
            "27-Apr-23",
            "26-May-23",
            "05-Jun-23",
            "06-Jun-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "IN": [
            "26-Jan-23",
            "21-Apr-23",
            "15-Aug-23",
            "02-Oct-23",
            "24-Oct-23",
            "25-Dec-23",
        ],
        "CA": [
            "21-Feb-23",
            "15-Apr-23",
            "23-May-23",
            "01-Jul-23",
            "01-Aug-23",
            "05-Sep-23",
            "10-Oct-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "AU": [
            "03-Jan-23",
            "26-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "25-Apr-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "HK": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "AE": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "MY": [
            "18-Apr-23",
            "25-Apr-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "TW": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "SA": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "CH": [
            "25-Dec-23",
            "26-Dec-23",
        ],
    }

    adrc_dict = {
        "IN_IN": {
            "SA": 21,
            "SE": 25,
            "SSE": 30,
            "AC": 43,
            "C": 62,
            "SC": 92,
            "M": 123,
            "SM": 165,
            "PM": 219,
            "D": 256,
            "SD": 298,
            "VP": 569,
            "EVP": 569,
        },
        "NA_US": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 327,
            "C": 429,
            "SC": 535,
            "M": 603,
            "SM": 713,
            "PM": 815,
            "D": 925,
            "SD": 1265,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_US_LTT/STT": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 365,
            "C": 390,
            "SC": 424,
            "M": 475,
            "SM": 560,
            "PM": 637,
            "D": 739,
            "SD": 908,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_US_NEW_STT/I_gate_landed ": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 365,
            "C": 390,
            "SC": 424,
            "M": 475,
            "SM": 560,
            "PM": 637,
            "D": 739,
            "SD": 908,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_CA_Local": {
            "SA": 230,
            "SE": 236,
            "SSE": 243,
            "AC": 257,
            "C": 277,
            "SC": 331,
            "M": 385,
            "SM": 473,
            "PM": 615,
            "D": 730,
            "SD": 885,
            "VP": 1399,
            "EVP": 1399,
        },
        "NA_CA_Landed": {
            "SA": 230,
            "SE": 236,
            "SSE": 243,
            "AC": 284,
            "C": 297,
            "SC": 318,
            "M": 351,
            "SM": 392,
            "PM": 439,
            "D": 527,
            "SD": 824,
            "VP": 1399,
            "EVP": 1399,
        },
        "UK_GB": {
            "SA": 216,
            "SE": 216,
            "SSE": 216,
            "AC": 234,
            "C": 275,
            "SC": 378,
            "M": 505,
            "SM": 640,
            "PM": 743,
            "D": 865,
            "SD": 1106,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_GB_LTT/STT": {
            "SA": 216,
            "SE": 216,
            "SSE": 239,
            "AC": 281,
            "C": 289,
            "SC": 303,
            "M": 356,
            "SM": 419,
            "PM": 498,
            "D": 654,
            "SD": 823,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_Nearshore": {
            "SA": 216,
            "SE": 216,
            "SSE": 216,
            "AC": 234,
            "C": 275,
            "SC": 378,
            "M": 505,
            "SM": 640,
            "PM": 743,
            "D": 865,
            "SD": 1106,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_ZA": {
            "SA": 100,
            "SE": 108,
            "SSE": 109,
            "AC": 110,
            "C": 119,
            "SC": 169,
            "M": 207,
            "SM": 368,
            "PM": 663,
            "D": 447,
            "SD": 447,
            "VP": 553,
            "EVP": 553,
        },
        "APAC_HK": {
            "SA": 103,
            "SE": 103,
            "SSE": 103,
            "AC": 166,
            "C": 230,
            "SC": 297,
            "M": 370,
            "SM": 444,
            "PM": 578,
            "D": 638,
            "SD": 867,
            "VP": 987,
            "EVP": 987,
        },
        "APAC_SG": {
            "SA": 157,
            "SE": 157,
            "SSE": 170,
            "AC": 195,
            "C": 245,
            "SC": 302,
            "M": 346,
            "SM": 440,
            "PM": 491,
            "D": 623,
            "SD": 868,
            "VP": 1591,
            "EVP": 1591,
        },
        "APAC_AE": {
            "SA": 165,
            "SE": 165,
            "SSE": 177,
            "AC": 216,
            "C": 258,
            "SC": 316,
            "M": 381,
            "SM": 486,
            "PM": 488,
            "D": 598,
            "SD": 786,
            "VP": 1656,
            "EVP": 1656,
        },
        "APAC_MY": {
            "SA": 64,
            "SE": 64,
            "SSE": 64,
            "AC": 86,
            "C": 129,
            "SC": 166,
            "M": 201,
            "SM": 261,
            "PM": 390,
            "D": 462,
            "SD": 472,
            "VP": 483,
            "EVP": 483,
        },
        "APAC_TW": {
            "SA": 78,
            "SE": 78,
            "SSE": 78,
            "AC": 121,
            "C": 156,
            "SC": 217,
            "M": 217,
            "SM": 333,
            "PM": 350,
            "D": 355,
            "SD": 385,
            "VP": 409,
            "EVP": 409,
        },
        "APAC_SA": {
            "SA": 203,
            "SE": 203,
            "SSE": 241,
            "AC": 292,
            "C": 390,
            "SC": 408,
            "M": 565,
            "SM": 667,
            "PM": 1014,
            "D": 1014,
            "SD": 1100,
            "VP": 1683,
            "EVP": 1683,
        },
        "DC_CH": {
            "SA": 67,
            "SE": 79,
            "SSE": 90,
            "AC": 111,
            "C": 147,
            "SC": 208,
            "M": 300,
            "SM": 343,
            "PM": 419,
            "D": 431,
            "SD": 431,
            "VP": 733,
            "EVP": 733,
        },
        "DC_PH": {
            "SA": 41,
            "SE": 47,
            "SSE": 52,
            "AC": 66,
            "C": 88,
            "SC": 133,
            "M": 188,
            "SM": 221,
            "PM": 307,
            "D": 455,
            "SD": 455,
            "VP": 511,
            "EVP": 511,
        },
    }
    currency_rate_dict = {
        "PHP": 0.02,
        "AUD": 0.63,
        "USD": 0.85,
        "SGD": 0.63,
        "MYR": 0.21,
        "EUR": 1,
    }
slt_dict={'AU':'Deepak SathyaPrasad',
'IN':'Shailesh Rao',
'HK':'Shailesh Rao',
'SG':'Shailesh Rao',
'AE':'Shailesh Rao',
'MY':'Shailesh Rao',
'TW':'Shailesh Rao',
'SA':'Shailesh Rao',
'CH':'Unkown',
'PH':'Unkown',
 'NA_CA_Landed':'Jashmir Wadia',
 'NA_CA_Local':'Jashmir Wadia',
 'NA_US_LTT/STT':'Jashmir Wadia',
 'UK_GB':"Vikas Tiwari",
 'UK_GB_LTT/STT':'Vikas Tiwari',
 'US':'Jashmir Wadia',
 'UK_Nearshore':'Jashmir Wadia'
 }
designation_dict={'Associate Consultant':'AC',
 'Consultant':'C',
 'Director':'D',
 'Manager':'M',
 'Portfolio Manager':'PM',
 'Senior Consultant':'SC',
 'Senior Director':'SD',
 'Senior Manager':'SM',
 'Senior Software Engineer':'SSE',
 'Software Engineer':'SE'}
adrc_dict_resource = {
        "IN": {
            "SA": 21,
            "SE": 25,
            "SSE": 30,
            "AC": 43,
            "C": 62,
            "SC": 92,
            "M": 123,
            "SM": 165,
            "PM": 219,
            "D": 256,
            "SD": 298,
            "VP": 569,
            "EVP": 569,
        },
        "US": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 327,
            "C": 429,
            "SC": 535,
            "M": 603,
            "SM": 713,
            "PM": 815,
            "D": 925,
            "SD": 1265,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_US_LTT/STT": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 365,
            "C": 390,
            "SC": 424,
            "M": 475,
            "SM": 560,
            "PM": 637,
            "D": 739,
            "SD": 908,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_US_NEW_STT/I_gate_landed ": {
            "SA": 225,
            "SE": 293,
            "SSE": 293,
            "AC": 365,
            "C": 390,
            "SC": 424,
            "M": 475,
            "SM": 560,
            "PM": 637,
            "D": 739,
            "SD": 908,
            "VP": 2267,
            "EVP": 2267,
        },
        "NA_CA_Local": {
            "SA": 230,
            "SE": 236,
            "SSE": 243,
            "AC": 257,
            "C": 277,
            "SC": 331,
            "M": 385,
            "SM": 473,
            "PM": 615,
            "D": 730,
            "SD": 885,
            "VP": 1399,
            "EVP": 1399,
        },
        "NA_CA_Landed": {
            "SA": 230,
            "SE": 236,
            "SSE": 243,
            "AC": 284,
            "C": 297,
            "SC": 318,
            "M": 351,
            "SM": 392,
            "PM": 439,
            "D": 527,
            "SD": 824,
            "VP": 1399,
            "EVP": 1399,
        },
        "UK_GB": {
            "SA": 216,
            "SE": 216,
            "SSE": 216,
            "AC": 234,
            "C": 275,
            "SC": 378,
            "M": 505,
            "SM": 640,
            "PM": 743,
            "D": 865,
            "SD": 1106,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_GB_LTT/STT": {
            "SA": 216,
            "SE": 216,
            "SSE": 239,
            "AC": 281,
            "C": 289,
            "SC": 303,
            "M": 356,
            "SM": 419,
            "PM": 498,
            "D": 654,
            "SD": 823,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_Nearshore": {
            "SA": 216,
            "SE": 216,
            "SSE": 216,
            "AC": 234,
            "C": 275,
            "SC": 378,
            "M": 505,
            "SM": 640,
            "PM": 743,
            "D": 865,
            "SD": 1106,
            "VP": 2018,
            "EVP": 2018,
        },
        "UK_ZA": {
            "SA": 100,
            "SE": 108,
            "SSE": 109,
            "AC": 110,
            "C": 119,
            "SC": 169,
            "M": 207,
            "SM": 368,
            "PM": 663,
            "D": 447,
            "SD": 447,
            "VP": 553,
            "EVP": 553,
        },
        "HK": {
            "SA": 103,
            "SE": 103,
            "SSE": 103,
            "AC": 166,
            "C": 230,
            "SC": 297,
            "M": 370,
            "SM": 444,
            "PM": 578,
            "D": 638,
            "SD": 867,
            "VP": 987,
            "EVP": 987,
        },
        "SG": {
            "SA": 157,
            "SE": 157,
            "SSE": 170,
            "AC": 195,
            "C": 245,
            "SC": 302,
            "M": 346,
            "SM": 440,
            "PM": 491,
            "D": 623,
            "SD": 868,
            "VP": 1591,
            "EVP": 1591,
        },
        "AE": {
            "SA": 165,
            "SE": 165,
            "SSE": 177,
            "AC": 216,
            "C": 258,
            "SC": 316,
            "M": 381,
            "SM": 486,
            "PM": 488,
            "D": 598,
            "SD": 786,
            "VP": 1656,
            "EVP": 1656,
        },
        "MY": {
            "SA": 64,
            "SE": 64,
            "SSE": 64,
            "AC": 86,
            "C": 129,
            "SC": 166,
            "M": 201,
            "SM": 261,
            "PM": 390,
            "D": 462,
            "SD": 472,
            "VP": 483,
            "EVP": 483,
        },
        "TW": {
            "SA": 78,
            "SE": 78,
            "SSE": 78,
            "AC": 121,
            "C": 156,
            "SC": 217,
            "M": 217,
            "SM": 333,
            "PM": 350,
            "D": 355,
            "SD": 385,
            "VP": 409,
            "EVP": 409,
        },
        "SA": {
            "SA": 203,
            "SE": 203,
            "SSE": 241,
            "AC": 292,
            "C": 390,
            "SC": 408,
            "M": 565,
            "SM": 667,
            "PM": 1014,
            "D": 1014,
            "SD": 1100,
            "VP": 1683,
            "EVP": 1683,
        },
        "CH": {
            "SA": 67,
            "SE": 79,
            "SSE": 90,
            "AC": 111,
            "C": 147,
            "SC": 208,
            "M": 300,
            "SM": 343,
            "PM": 419,
            "D": 431,
            "SD": 431,
            "VP": 733,
            "EVP": 733,
        },
        "PH": {
            "SA": 41,
            "SE": 47,
            "SSE": 52,
            "AC": 66,
            "C": 88,
            "SC": 133,
            "M": 188,
            "SM": 221,
            "PM": 307,
            "D": 455,
            "SD": 455,
            "VP": 511,
            "EVP": 511,
        },
    }

@staticmethod
def Commit_data_calculate(x, leaves=None):
        """x -->  [cor, ADRC, country, Start date, end date]"""

        # start_date = datetime.strptime(x[-2], "%Y-%m-%d")
        # end_date = datetime.strptime(x[-1], "%Y-%m-%d")
        start_date = x[-2]
        end_date = x[-1]
        input_dt = start_date.replace(day=1)

        input_dt = input_dt + timedelta(days=32)

        res = input_dt.replace(day=1)
        list1 = []
        for dt in rrule.rrule(rrule.MONTHLY, dtstart=res, until=end_date):
            list1.append(dt)

        # for dt in rrule.rrule(rrule.MONTHLY, dtstart=res, until=end_date.to_pydatetime()):
        #     list1.append(dt)

        # list1.insert(0, start_date.to_pydatetime())
        # list1.insert(len(list1), end_date.to_pydatetime() + timedelta(days=1))

        list1.insert(0, start_date)
        list1.insert(len(list1), end_date + timedelta(days=1))

        # country_holidays_path = "public hoildays"
        country_ = x[2]
        print(country_)
        holidays_ = Flask_Project_data.holidays_list.get(country_, None)
        hoildays_list = []
        if holidays_ is not None:
            for i in holidays_:
                hoildays_list.append(datetime.strptime(i, "%d-%b-%y").date())
            print(hoildays_list)
        # if country_ == "au":
        #     country_holidays_path += r"\au.csv"
        # elif country_ == "ca":
        #     country_holidays_path += r"\ca.csv"
        # elif country_ == "in":
        #     country_holidays_path += r"\in.csv"
        # elif country_ == "nl":
        #     country_holidays_path += r"\nl.csv"
        # elif country_ == "ph":
        #     country_holidays_path += r"\ph.csv"
        # elif country_ == "sg":
        #     country_holidays_path += r"\sg.csv"
        # elif country_ == "uk":
        #     country_holidays_path += r"\uk.csv"
        # elif country_ == "us":
        #     country_holidays_path += r"\us.csv"
        # else:
        #     check_country = False
        # if check_country:
        # public_holidays_df = pd.read_csv(
        #     "C:/Users/zusankal/Downloads/extract/A/public hoildays/au.csv"
        # )
        # hoildays_list_ = public_holidays_df["Date"].astype("datetime64[D]").to_list()
        # print(hoildays_list_)
        leaves_list=list()
        workefforts_month = dict()
        workefforts_list = list()
        if hoildays_list:
            for i in range(1, len(list1)):
                workefforts_month[list1[i - 1].strftime("%B")[:3]] = np.busday_count(
                    list1[i - 1].strftime("%Y-%m-%d"),
                    list1[i].strftime("%Y-%m-%d"),
                    holidays=hoildays_list,
                )
        else:
            for i in range(1, len(list1)):
                workefforts_month[list1[i - 1].strftime("%B")[:3]] = np.busday_count(
                    list1[i - 1].strftime("%Y-%m-%d"), list1[i].strftime("%Y-%m-%d")
                )
        months = {
            "Jan": 1,
            "Feb": 2,
            "Mar": 3,
            "Apr": 4,
            "May": 5,
            "Jun": 6,
            "Jul": 7,
            "Aug": 8,
            "Sep": 9,
            "Oct": 10,
            "Nov": 11,
            "Dec": 12,
        }

        keys_list = list(workefforts_month.keys())
        values_list = list(workefforts_month.values())
        append_at_start = int(months[keys_list[0]] - months["Jan"])
        append_at_end = int(months["Dec"] - months[keys_list[-1]])
        for i in range(append_at_start):
            workefforts_list.append(0)
        for i in values_list:
            workefforts_list.append(i)
        for i in range(append_at_end):
            workefforts_list.append(0)

        bill_rate = int(x[0])
        ADRC = int(x[1])
        bill_rate_list = list()
        for i in workefforts_list:
            bill_rate_list.append(i * bill_rate)
        Total_days = sum(workefforts_list)
        Total_Revenue = sum(bill_rate_list)
        Total_Cost = sum(workefforts_list) * ADRC
        CM = Total_Revenue - Total_Cost
        CM_percentage = [(CM / Total_Revenue) * 100]
        Total_days = [Total_days]
        Total_Revenue = [Total_Revenue]
        Total_Cost = [Total_Cost]
        CM = [CM]
        commit_data_dict = {
            "workefforts_list": workefforts_list,
            "total_days": Total_days,
            "bill_rate_list": bill_rate_list,
            "total_revenue": Total_Revenue,
            "total_cost": Total_Cost,
            "cm": CM,
            "cm_percentage": CM_percentage,
        }
        return commit_data_dict


@app.route("/")
@app.route("/home")
def home():
    # book = load_workbook("flask_excel_app/temp.xlsx")
    # sheet = book.active
    # BookingForecast
    # (B2) PASS INTO HTML TEMPLATE
    return render_template("home.html", BookingForecast=BookingForecast)
    # return render_template("home.html", sheet=sheet)


@app.route("/commit_display")
def commit_display():
    return render_template("commit_display.html", Commit=Commit)


@app.route("/wondeals_display")
def wondeals_display():
    return render_template("wondeals_display.html", WonDeals=WonDeals)


@app.route("/interview_display", methods=["POST", "GET"])
def interview_display():
    return render_template("interview_display.html", Interview=Interview)


@app.route("/demand_display", methods=["POST", "GET"])
def demand_display():
    return render_template("demand_display.html", Demand=Demand)

@app.route("/resouce_master_display", methods=["POST", "GET"])
def resource_master_display():
    return render_template("resource_master_display.html", ResourceMaster=ResourceMaster)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in", "success")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated!", "success")
        return redirect(url_for("account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template("account.html", title="Account", form=form)


@app.route("/bookingforecast_insert", methods=["GET", "POST"])
@login_required
def bookingforecast_insert():
    form = BookingForecastForm()
    if form.validate_on_submit():
        form_data_dict = form.data
        del form_data_dict["submit"]
        del form_data_dict["csrf_token"]

        deal_value_eur_ = form_data_dict[
            "deal_value"
        ] * Flask_Project_data.currency_rate_dict.get(form_data_dict["currency"])

        if form_data_dict["win_prob"] >= 50 and form_data_dict["win_prob"] < 100:
            status_ = "Commit"
        elif form_data_dict["win_prob"] < 50 and form_data_dict["win_prob"] > 0:
            status_ = "Pipeline"
        else:
            status_ = "Won"

        if form_data_dict["win_prob"] == 100:

            form_data_dict["sales_stage"] = "6. Won"

        elif form_data_dict["win_prob"] >= 50 and form_data_dict["win_prob"] < 100:

            form_data_dict["sales_stage"] = "3. Proposal Submitted"

        row1 = BookingForecast(
            # project_id=form_data_dict["project_id"],
            project_name=form_data_dict["project_name"],
            practice=form_data_dict["practice"],
            slt_owner=form_data_dict["slt_owner"],
            practice_owner=form_data_dict["practice_owner"],
            quarter=form_data_dict["quarter"],
            sales_stage=form_data_dict["sales_stage"],
            project_type=form_data_dict["project_type"],
            region=form_data_dict["region"],
            country=form_data_dict["country"],
            win_prob=form_data_dict["win_prob"],
            currency=form_data_dict["currency"],
            deal_value=round(form_data_dict["deal_value"],2),
            deal_value_eur=round(deal_value_eur_,2),
            status=status_,
            last_updated_by=current_user.username,
            updated_date_time=datetime.now(),
        )
        db.session.add(row1)
        db.session.commit()
        flash("Your entry has been added!", "success")

        if form_data_dict["win_prob"] >= 50.0 and form_data_dict["win_prob"] < 100.0:
            return redirect(url_for("commit_insert", **form_data_dict))
        if form_data_dict["win_prob"] == 100.0:
            return redirect(url_for("wondeals_insert", **form_data_dict))

    return render_template(
        "bookingforecast.html", title="insertdata-bookingforecast", form=form
    )


@app.route("/wondeals_insert", methods=["POST", "GET"])
@login_required
def wondeals_insert():
    form = WonDealsForm()
    if form.validate_on_submit():

       
        commit_cal_ = Flask_Project_data.Commit_data_calculate(
            [
                form.revenue_daily_rate.data,
                Flask_Project_data.adrc_dict[form.resource_country.data][
                    form.resource_level.data
                ],
                form.project_country.data[3:5],
                form.start_date_wondeals.data,
                form.end_date_wondeals.data,
            ]
        )

        str_lilrid = f" Select FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "
        for i in commit_cal_["workefforts_list"]:
            print(type(int(i)))
            print(type(i))
        row1 = WonDeals(
            project_id=form.project_id.data,
            carryforward=form.carryforward.data,
            project_name=form.project_name.data,
            slt_owner=form.slt_owner.data,
            practice=form.practice.data,
            quarter=form.quarter.data,
            project_manager=form.project_manager.data,
            project_type=form.project_type.data,
            resource_name=form.resource_name.data,
            resource_country=form.resource_country.data,
            resource_level=form.resource_level.data,
            onshore_offshore=form.onshore_offshore.data,
            fte=form.fte.data,
            start_date_wondeals=form.start_date_wondeals.data,
            end_date_wondeals=form.end_date_wondeals.data,
            revenue_daily_rate=round(form.revenue_daily_rate.data,2),
            adrc=Flask_Project_data.adrc_dict[form.resource_country.data][
                form.resource_level.data
            ],
            practice_owner=form.practice_owner.data,
            email_id=form.email_id.data,
            project_country=form.project_country.data,
            days_jan=int(commit_cal_["workefforts_list"][0]),
            days_feb=int(commit_cal_["workefforts_list"][1]),
            days_mar=int(commit_cal_["workefforts_list"][2]),
            days_apr=int(commit_cal_["workefforts_list"][3]),
            days_may=int(commit_cal_["workefforts_list"][4]),
            days_jun=int(commit_cal_["workefforts_list"][5]),
            days_jul=int(commit_cal_["workefforts_list"][6]),
            days_aug=int(commit_cal_["workefforts_list"][7]),
            days_sep=int(commit_cal_["workefforts_list"][8]),
            days_oct=int(commit_cal_["workefforts_list"][9]),
            days_nov=int(commit_cal_["workefforts_list"][10]),
            days_dec=int(commit_cal_["workefforts_list"][11]),
            total_days=int(commit_cal_["total_days"][0]),
            eur_jan=round(int(commit_cal_["bill_rate_list"][0]),2),
            eur_feb=round(int(commit_cal_["bill_rate_list"][1]),2),
            eur_mar=round(int(commit_cal_["bill_rate_list"][2]),2),
            eur_apr=round(int(commit_cal_["bill_rate_list"][3]),2),
            eur_may=round(int(commit_cal_["bill_rate_list"][4]),2),
            eur_jun=round(int(commit_cal_["bill_rate_list"][5]),2),
            eur_jul=round(int(commit_cal_["bill_rate_list"][6]),2),
            eur_aug=round(int(commit_cal_["bill_rate_list"][7]),2),
            eur_sep=round(int(commit_cal_["bill_rate_list"][8]),2),
            eur_oct=round(int(commit_cal_["bill_rate_list"][9]),2),
            eur_nov=round(int(commit_cal_["bill_rate_list"][10]),2),
            eur_dec=round(int(commit_cal_["bill_rate_list"][11]),2),
            total_revenue=round(commit_cal_["total_revenue"][0],2),
            total_cost=round(commit_cal_["total_cost"][0],2),
            cm=round(commit_cal_["cm"][0],2),
            resource_wise_cm_percet=round(commit_cal_["cm_percentage"][0],2),
            last_updated_by=current_user.username,
            updated_date_time=datetime.now(),
            #li_lr_id= from resource master with the email id 
        )
        db.session.add(row1)
        db.session.commit()
        if form.project_type.data=="FP":flash("Review COR as per IMPACT Sheet","secondary")
        flash("Your entry has been added!", "success")
        form_dict=form.data

        return redirect(url_for("demand_insert",**form_dict))


    elif request.method == "GET":
        form_dict = request.args.to_dict()
        form.project_name.data = form_dict.get("project_name")
        form.slt_owner.data = form_dict.get("slt_owner")
        form.practice.data = form_dict.get("practice")
        form.quarter.data = form_dict.get("quarter")

    return render_template("wondeals_insert.html", title="wondeals-insert", form=form)


@app.route("/wondeals/<int:wondeals_id>/update", methods=["GET", "POST"])
@login_required
def wondeals_update(wondeals_id):
    wondeals = WonDeals.query.get_or_404(wondeals_id)
    form = WonDealsForm()
    if form.validate_on_submit():
        commit_cal_ = Flask_Project_data.Commit_data_calculate(
            [
                form.revenue_daily_rate.data,
                Flask_Project_data.adrc_dict[form.resource_country.data][
                    form.resource_level.data
                ],
                form.project_country.data[3:5],
                form.start_date_wondeals.data,
                form.end_date_wondeals.data,
            ]
        )
        wondeals.project_id = form.project_id.data
        wondeals.carryforward = form.carryforward.data
        wondeals.project_name = form.project_name.data
        wondeals.slt_owner = form.slt_owner.data
        wondeals.practice = form.practice.data
        wondeals.quarter = form.quarter.data
        wondeals.project_manager = form.project_manager.data
        wondeals.project_type = form.project_type.data
        wondeals.resource_name = form.resource_name.data
        wondeals.resource_country = form.resource_country.data
        wondeals.resource_level = form.resource_level.data
        wondeals.onshore_offshore = form.onshore_offshore.data
        wondeals.fte = form.fte.data
        wondeals.start_date_wondeals = form.start_date_wondeals.data
        wondeals.end_date_wondeals = form.end_date_wondeals.data
        wondeals.revenue_daily_rate = round(form.revenue_daily_rate.data,2)
        wondeals.adrc = Flask_Project_data.adrc_dict[form.resource_country.data][
            form.resource_level.data
        ]
        wondeals.practice_owner = form.practice_owner.data
        wondeals.email_id = form.email_id.data
        wondeals.project_country = form.project_country.data

        wondeals.days_jan = int(commit_cal_["workefforts_list"][0])
        wondeals.days_feb = int(commit_cal_["workefforts_list"][1])
        wondeals.days_mar = int(commit_cal_["workefforts_list"][2])
        wondeals.days_apr = int(commit_cal_["workefforts_list"][3])
        wondeals.days_may = int(commit_cal_["workefforts_list"][4])
        wondeals.days_jun = int(commit_cal_["workefforts_list"][5])
        wondeals.days_jul = int(commit_cal_["workefforts_list"][6])
        wondeals.days_aug = int(commit_cal_["workefforts_list"][7])
        wondeals.days_sep = int(commit_cal_["workefforts_list"][8])
        wondeals.days_oct = int(commit_cal_["workefforts_list"][9])
        wondeals.days_nov = int(commit_cal_["workefforts_list"][10])
        wondeals.days_dec = int(commit_cal_["workefforts_list"][11])

        wondeals.total_days = int(commit_cal_["total_days"][0])

        wondeals.eur_jan = round(int(commit_cal_["bill_rate_list"][0]),2)
        wondeals.eur_feb = round(int(commit_cal_["bill_rate_list"][1]),2)
        wondeals.eur_mar = round(int(commit_cal_["bill_rate_list"][2]),2)
        wondeals.eur_apr = round(int(commit_cal_["bill_rate_list"][3]),2)
        wondeals.eur_may = round(int(commit_cal_["bill_rate_list"][4]),2)
        wondeals.eur_jun = round(int(commit_cal_["bill_rate_list"][5]),2)
        wondeals.eur_jul = round(int(commit_cal_["bill_rate_list"][6]),2)
        wondeals.eur_aug = round(int(commit_cal_["bill_rate_list"][7]),2)
        wondeals.eur_sep = round(int(commit_cal_["bill_rate_list"][8]),2)
        wondeals.eur_oct = round(int(commit_cal_["bill_rate_list"][9]),2)
        wondeals.eur_nov = round(int(commit_cal_["bill_rate_list"][10]),2)
        wondeals.eur_dec = round(int(commit_cal_["bill_rate_list"][11]),2)

        wondeals.total_revenue = round(commit_cal_["total_revenue"][0],2)
        wondeals.total_cost = round(commit_cal_["total_cost"][0],2)
        wondeals.cm = round(commit_cal_["cm"][0],2)
        wondeals.resource_wise_cm_percet =round(commit_cal_["cm_percentage"][0],2)
        wondeals.last_updated_by = current_user.username
        wondeals.updated_date_time = datetime.now()
        db.session.commit()
        flash("Your resource has been updated!", "success")
        return redirect(url_for("wondeals_display"))
    elif request.method == "GET":
        form.project_id.data = wondeals.project_id
        form.carryforward.data = wondeals.carryforward
        form.project_name.data = wondeals.project_name
        form.slt_owner.data = wondeals.slt_owner
        form.practice.data = wondeals.practice
        form.quarter.data = wondeals.quarter
        form.project_manager.data = wondeals.project_manager
        form.project_type.data = wondeals.project_type
        form.resource_name.data = wondeals.resource_name
        form.resource_country.data = wondeals.resource_country
        form.resource_level.data = wondeals.resource_level
        form.onshore_offshore.data = wondeals.onshore_offshore
        form.fte.data = wondeals.fte
        form.start_date_wondeals.data = wondeals.start_date_wondeals
        form.end_date_wondeals.data = wondeals.end_date_wondeals
        form.revenue_daily_rate.data = wondeals.revenue_daily_rate
        form.practice_owner.data = wondeals.practice_owner
        form.email_id.data = wondeals.email_id
        form.project_country.data = wondeals.project_country

    return render_template("wondeals_insert.html", title="update-wondeals", form=form)

@app.route("/commit_insert", methods=["POST", "GET"])
@login_required
def commit_insert():
    print("IN commit method =======================================================================")
    form = CommitForm()

    # booking_commit_dict =session['booking_to_commit']
    # inverview_to_commit=session['interview_to_commit']
    # hist=booking_commit_dict.get('history')
    # inverview_to_commit_status = inverview_to_commit.get('flag')
    
    # session['commit_count']={'count':1}
    # commit_count=session['commit_count']
    # check_dict = session["interview"]
    # print(check_dict['flag'])
    # if (check_dict.get("flag")=='True'):
        
    #     commit_dict = session["commit_data"]
    #     form.project_name.data = commit_dict.get("project_name")
    #     form.slt_owner.data = commit_dict.get("slt_owner")
    #     form.practice.data = commit_dict.get("practice")
    #     form.quarter.data = commit_dict.get("quarter")
    #     form.project_manager.data = commit_dict.get("project_manager")
    #     form.resource_name.data = commit_dict.get("resource_name")
    #     form.resource_country.data = commit_dict.get("resource_country")
    #     form.resource_level.data = commit_dict.get("resource_level")
    #     form.onshore_offshore.data = commit_dict.get("onshore_offshore")
    #     form.fte.data = commit_dict.get("fte")
    #     form.start_date_commit.data = commit_dict.get("start_date_commit")
    #     form.end_date_commit.data = commit_dict.get("end_date_commit")
    #     form.revenue_daily_rate.data = commit_dict.get("revenue_daily_rate")

    #     history_page = commit_dict.get("history", "interview")
    #     session["commit_to_demand"]["history"] = "interview"


    if form.validate_on_submit():

        # "workefforts_list"
        # "total_days"
        # "bill_rate_list"
        # "total_revenue"
        # "total_cost"
        # "cm"
        # "cm_percentage"
        print(" I am HERE"*3)
        if isinstance(form.start_date_commit.data, str):
            print("inside if ")
            form.start_date_commit.data=datetime.strptime(form.start_date_commit.data, "%Y-%m-%d")
            #form.start_date_commit.data=datetime.strptime(str(form.start_date_commit.data("start_date_commit")),'%Y-%m-%d')
        if isinstance(form.end_date_commit.data, str):
            form.end_date_commit.data=datetime.strptime(form.end_date_commit.data, "%Y-%m-%d")
            #form.start_date_commit.data=datetime.strptime(form.start_date_commit.data, "%d-%b-%Y").date()
            #form.end_date_commit.data=datetime.strptime(str(form.end_date_commit.data("end_date_commit")),'%Y-%m-%d')

            #form.start_date_commit.data=datetime.strptime(str(form_dict.get("start_date_commit")),'%Y-%m-%d')

        commit_cal_ = Flask_Project_data.Commit_data_calculate(
            [
                form.revenue_daily_rate.data,
                Flask_Project_data.adrc_dict[form.resource_country.data][
                    form.resource_level.data
                ],
                form.resource_country.data[3:5],
                form.start_date_commit.data,
                form.end_date_commit.data,
            ]
        )
        # for i in commit_cal_["workefforts_list"]:
        #     print(type(int(i)))
        #     print(type(i))
        row1 = Commit(
            project_name=form.project_name.data,
            slt_owner=form.slt_owner.data,
            practice=form.practice.data,
            quarter=form.quarter.data,
            project_manager=form.project_manager.data,
            resource_name=form.resource_name.data,
            resource_country=form.resource_country.data,
            resource_level=form.resource_level.data,
            onshore_offshore=form.onshore_offshore.data,
            fte=form.fte.data,
            start_date_commit=form.start_date_commit.data,
            end_date_commit=form.end_date_commit.data,
            revenue_daily_rate=round(form.revenue_daily_rate.data,2),
            adrc=Flask_Project_data.adrc_dict[form.resource_country.data][
                form.resource_level.data
            ],
            days_jan=int(commit_cal_["workefforts_list"][0]),
            days_feb=int(commit_cal_["workefforts_list"][1]),
            days_mar=int(commit_cal_["workefforts_list"][2]),
            days_apr=int(commit_cal_["workefforts_list"][3]),
            days_may=int(commit_cal_["workefforts_list"][4]),
            days_jun=int(commit_cal_["workefforts_list"][5]),
            days_jul=int(commit_cal_["workefforts_list"][6]),
            days_aug=int(commit_cal_["workefforts_list"][7]),
            days_sep=int(commit_cal_["workefforts_list"][8]),
            days_oct=int(commit_cal_["workefforts_list"][9]),
            days_nov=int(commit_cal_["workefforts_list"][10]),
            days_dec=int(commit_cal_["workefforts_list"][11]),
            total_days=int(commit_cal_["total_days"][0]),
            eur_jan=round(int(commit_cal_["bill_rate_list"][0]),2),
            eur_feb=round(int(commit_cal_["bill_rate_list"][1]),2),
            eur_mar=round(int(commit_cal_["bill_rate_list"][2]),2),
            eur_apr=round(int(commit_cal_["bill_rate_list"][3]),2),
            eur_may=round(int(commit_cal_["bill_rate_list"][4]),2),
            eur_jun=round(int(commit_cal_["bill_rate_list"][5]),2),
            eur_jul=round(int(commit_cal_["bill_rate_list"][6]),2),
            eur_aug=round(int(commit_cal_["bill_rate_list"][7]),2),
            eur_sep=round(int(commit_cal_["bill_rate_list"][8]),2),
            eur_oct=round(int(commit_cal_["bill_rate_list"][9]),2),
            eur_nov=round(int(commit_cal_["bill_rate_list"][10]),2),
            eur_dec=round(int(commit_cal_["bill_rate_list"][11]),2),
            total_revenue=round(commit_cal_["total_revenue"][0],2),
            total_cost=round(commit_cal_["total_cost"][0],2),
            cm=round(commit_cal_["cm"][0],2),
            resource_wise_cm_percet=round(commit_cal_["cm_percentage"][0],2),
            last_updated_by=current_user.username,
            updated_date_time=datetime.now(),
        )
        db.session.add(row1)
        db.session.commit()
        #get_dict_commit=request.args.to_dict()
        #print("heree")
        #print(get_dict_commit)
        form_dict=form.data
       
        flash("Your entry has been added!", "success")
        return redirect(url_for("demand_insert",**form_dict))
    elif request.method == "GET":

        print("#########################################################")

        form_dict = request.args.to_dict()

        print(form_dict)
        form.project_name.data=form_dict.get("project_name")
        form.slt_owner.data=form_dict.get("slt_owner")
        form.practice.data=form_dict.get("practice")
        form.quarter.data=form_dict.get("quarter")
        form.project_manager.data=form_dict.get("project_manager")
        form.resource_name.data=form_dict.get("resource_name")
        form.resource_country.data=form_dict.get("resource_country")
        form.resource_level.data=form_dict.get("resource_level")
        form.onshore_offshore.data=form_dict.get("onshore_offshore")
        form.fte.data=form_dict.get("fte")
        form.revenue_daily_rate.data=form_dict.get('revenue_daily_rate')
        if isinstance(form_dict.get("start_date_commit"), str):
            print("inside if ")
            form.start_date_commit.data=datetime.strptime(form_dict.get("start_date_commit"), "%Y-%m-%d")
        else:
            form.start_date_commit.data=form_dict.get("start_date_commit")
            #form.start_date_commit.data=datetime.strptime(str(form.start_date_commit.data("start_date_commit")),'%Y-%m-%d')
        if isinstance(form_dict.get("end_date_commit"), str):
            form.end_date_commit.data=datetime.strptime(form_dict.get("end_date_commit"), "%Y-%m-%d")
        else:
            form.end_date_commit.data=form_dict.get("end_date_commit")
        

    return render_template("commit_insert.html", title="commit-insert", form=form)



@app.route("/commit/<int:commit_id>/update", methods=["GET", "POST"])
@login_required
def commit_update(commit_id):
    commit = Commit.query.get_or_404(commit_id)
    form = CommitForm()
    if form.validate_on_submit():
        commit_cal_ = Flask_Project_data.Commit_data_calculate(
            [
                form.revenue_daily_rate.data,
                Flask_Project_data.adrc_dict[form.resource_country.data][
                    form.resource_level.data
                ],
                form.resource_country.data[3:5],
                form.start_date_commit.data,
                form.end_date_commit.data,
            ]
        )
        commit.project_name = form.project_name.data
        commit.slt_owner = form.slt_owner.data
        commit.practice = form.practice.data
        commit.quarter = form.quarter.data
        commit.project_manager = form.project_manager.data
        commit.resource_name = form.resource_name.data
        commit.resource_country = form.resource_country.data
        commit.resource_level = form.resource_level.data
        commit.onshore_offshore = form.onshore_offshore.data
        commit.fte = form.fte.data
        commit.start_date_commit = form.start_date_commit.data
        commit.end_date_commit = form.end_date_commit.data
        commit.revenue_daily_rate = round(form.revenue_daily_rate.data,2)
        commit.adrc = Flask_Project_data.adrc_dict[form.resource_country.data][
            form.resource_level.data
        ]

        commit.days_jan = int(commit_cal_["workefforts_list"][0])
        commit.days_feb = int(commit_cal_["workefforts_list"][1])
        commit.days_mar = int(commit_cal_["workefforts_list"][2])
        commit.days_apr = int(commit_cal_["workefforts_list"][3])
        commit.days_may = int(commit_cal_["workefforts_list"][4])
        commit.days_jun = int(commit_cal_["workefforts_list"][5])
        commit.days_jul = int(commit_cal_["workefforts_list"][6])
        commit.days_aug = int(commit_cal_["workefforts_list"][7])
        commit.days_sep = int(commit_cal_["workefforts_list"][8])
        commit.days_oct = int(commit_cal_["workefforts_list"][9])
        commit.days_nov = int(commit_cal_["workefforts_list"][10])
        commit.days_dec = int(commit_cal_["workefforts_list"][11])

        commit.total_days = int(commit_cal_["total_days"][0])

        commit.eur_jan = round(int(commit_cal_["bill_rate_list"][0]),2)
        commit.eur_feb = round(int(commit_cal_["bill_rate_list"][1]),2)
        commit.eur_mar = round(int(commit_cal_["bill_rate_list"][2]),2)
        commit.eur_apr = round(int(commit_cal_["bill_rate_list"][3]),2)
        commit.eur_may = round(int(commit_cal_["bill_rate_list"][4]),2)
        commit.eur_jun = round(int(commit_cal_["bill_rate_list"][5]),2)
        commit.eur_jul = round(int(commit_cal_["bill_rate_list"][6]),2)
        commit.eur_aug = round(int(commit_cal_["bill_rate_list"][7]),2)
        commit.eur_sep = round(int(commit_cal_["bill_rate_list"][8]),2)
        commit.eur_oct = round(int(commit_cal_["bill_rate_list"][9]),2)
        commit.eur_nov = round(int(commit_cal_["bill_rate_list"][10]),2)
        commit.eur_dec = round(int(commit_cal_["bill_rate_list"][11]),2)

        commit.total_revenue = round(commit_cal_["total_revenue"][0],2)
        commit.total_cost =  round(commit_cal_["total_cost"][0],2)
        commit.cm =  round(commit_cal_["cm"][0],2)
        commit.resource_wise_cm_percet =  round(commit_cal_["cm_percentage"][0],2)
        commit.last_updated_by = current_user.username
        commit.updated_date_time = datetime.now()
        db.session.commit()
        flash("Your resource has been updated!", "success")
        return redirect(url_for("commit_display"))
    elif request.method == "GET":
        form.project_name.data = commit.project_name
        form.slt_owner.data = commit.slt_owner
        form.practice.data = commit.practice
        form.quarter.data = commit.quarter
        form.project_manager.data = commit.project_manager
        form.resource_name.data = commit.resource_name
        form.resource_country.data = commit.resource_country
        form.resource_level.data = commit.resource_level
        form.onshore_offshore.data = commit.onshore_offshore
        form.fte.data = commit.fte
        form.start_date_commit.data = commit.start_date_commit
        form.end_date_commit.data = commit.end_date_commit
        form.revenue_daily_rate.data = commit.revenue_daily_rate

    return render_template("commit_insert.html", title="update-commit", form=form)


@app.route("/selectbookingforecast", methods=["GET", "POST"])
@login_required
def selectbookingforecast():
    form = BookingForecastProjectIdForm()
    if form.validate_on_submit():
        # str_ = form.project_name.data
        # search = "%{}%".format(str_)
        # bookingforecast = BookingForecast.query.filter(
        #     BookingForecast.project_name.like(search)
        # ).first()
        bookingforecast = BookingForecast.query.get_or_404(form.project_name.data)
        return redirect(
            url_for(
                "bookingforecast_update",
                bookingforecast_id=bookingforecast.project_name,
            )
        )
    return render_template(
        "selectbookingforecast.html",
        title="selectbookingforecast",
        BookingForecast=BookingForecast,
        form=form,
    )


@app.route(
    "/bookingforecast/<string:bookingforecast_id>/update", methods=["GET", "POST"]
)
@login_required
def bookingforecast_update(bookingforecast_id):
    bookingforecast = BookingForecast.query.get_or_404(bookingforecast_id)
    form = BookingForecastUpdateForm()
    if form.validate_on_submit():
        deal_value_eur_ = (
            form.deal_value.data
            * Flask_Project_data.currency_rate_dict.get(form.currency.data)
        )
        print(form.win_prob.data)
        if form.win_prob.data >= 50.0 and form.win_prob.data < 100.0:
            status_ = "Commit"
        elif form.win_prob.data < 50.0 and form.win_prob.data > 0:
            status_ = "Pipeline"
        elif form.win_prob.data == 0.0:
            status_ = "Lost"
        else:
            status_ = "Won"

        if form.win_prob.data == 100:
            sales_stage_ = "6. Won"
        else:
            sales_stage_ = form.sales_stage.data
        winprob_before_update = bookingforecast.win_prob
        bookingforecast.project_name = form.project_name.data
        bookingforecast.practice = form.practice.data
        bookingforecast.slt_owner = form.slt_owner.data
        bookingforecast.practice_owner = form.practice_owner.data
        bookingforecast.sales_stage = sales_stage_
        bookingforecast.project_type = form.project_type.data
        bookingforecast.quarter = form.quarter.data
        bookingforecast.region = form.region.data
        bookingforecast.country = form.country.data
        bookingforecast.win_prob = form.win_prob.data
        bookingforecast.currency = form.currency.data
        bookingforecast.deal_value = round(form.deal_value.data,2)
        bookingforecast.deal_value_eur = round(deal_value_eur_,2)
        bookingforecast.status = status_
        bookingforecast.last_updated_by = current_user.username
        bookingforecast.updated_date_time = datetime.now()
        db.session.commit()

        if (
            form.win_prob.data >= 50.0 and form.win_prob.data < 100.0
        ) and winprob_before_update < 50.0:
            return redirect(url_for("commit_insert", **(form.data)))
        if (form.win_prob.data == 100.0) and winprob_before_update < 50.0:
            return redirect(url_for("wondeals_insert", **(form.data)))

        if form.win_prob.data == 100.0:
            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_commit, end_date_commit, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "
            commit_rows_del = db.session.execute(str_sel).fetchall()
            if len(commit_rows_del) != 0:
                str_del = f" DELETE FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "
                if len(commit_rows_del) > 1:
                    str_ = ""
                    # str_ = "("
                    for i in commit_rows_del:
                        str_ += f"{i},"
                    str_ = str_[: len(str_) - 1]
                    # str_ += ")"
                    print(str_)
                else:
                    str_ = ""
                    for i in commit_rows_del:
                        str_ += f"{i}"
                db.session.execute(str_del)
                db.session.commit()
                str_insert_wondeals = f"INSERT INTO wondeals_table ( project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_wondeals, end_date_wondeals, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet) VALUES "
                str_insert_wondeals = str_insert_wondeals + str_
                db.session.execute(str_insert_wondeals)
                db.session.commit()
        elif form.win_prob.data < 100.0 and form.win_prob.data >= 50.0:
            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_wondeals, end_date_wondeals, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "
            commit_rows_del = db.session.execute(str_sel).fetchall()
            if len(commit_rows_del) != 0:
                str_del = f" DELETE FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "
                if len(commit_rows_del) > 1:
                    str_ = ""
                    # str_ = "("
                    for i in commit_rows_del:
                        str_ += f"{i},"
                    str_ = str_[: len(str_) - 1]
                    # str_ += ")"
                    print(str_)
                else:
                    str_ = ""
                    for i in commit_rows_del:
                        str_ += f"{i}"
                db.session.execute(str_del)
                db.session.commit()
                str_insert_wondeals = f"INSERT INTO commit_table ( project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_commit, end_date_commit, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet) VALUES "
                str_insert_wondeals = str_insert_wondeals + str_
                db.session.execute(str_insert_wondeals)
                db.session.commit()
        elif form.win_prob.data < 50.0 and form.win_prob.data > 0.0:
            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_wondeals, end_date_wondeals, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "
            commit_rows_del = db.session.execute(str_sel).fetchall()
            if len(commit_rows_del) != 0:
                str_del = f" DELETE FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "
                db.session.execute(str_del)
                db.session.commit()
            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_commit, end_date_commit, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "
            commit_rows_del = db.session.execute(str_sel).fetchall()
            if len(commit_rows_del) != 0:
                str_del = f" DELETE FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "
                db.session.execute(str_del)
                db.session.commit()
        elif form.win_prob.data == 0.0:

            str_sel = f"UPDATE Demand SET res_status = 'Closed' WHERE Demand.project_name = '{form.project_name.data}' "

            db.session.execute(str_sel)

            db.session.commit()

            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_wondeals, end_date_wondeals, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "

            commit_rows_del = db.session.execute(str_sel).fetchall()

            if len(commit_rows_del) != 0:

                str_del = f" DELETE FROM wondeals_table WHERE wondeals_table.project_name = '{form.project_name.data}' "

                db.session.execute(str_del)

                db.session.commit()

            str_sel = f"SELECT project_name, slt_owner, practice, quarter, project_manager, resource_name, resource_country, resource_level, onshore_offshore, fte, revenue_daily_rate, adrc, start_date_commit, end_date_commit, days_jan, days_feb, days_mar, days_apr, days_may, days_jun, days_jul, days_aug, days_sep, days_oct, days_nov, days_dec, total_days, eur_jan, eur_feb, eur_mar, eur_apr, eur_may, eur_jun, eur_jul, eur_aug, eur_sep, eur_oct, eur_nov, eur_dec, total_revenue, total_cost, cm, resource_wise_cm_percet FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "

            commit_rows_del = db.session.execute(str_sel).fetchall()

            if len(commit_rows_del) != 0:

                str_del = f" DELETE FROM commit_table WHERE commit_table.project_name = '{form.project_name.data}' "

                db.session.execute(str_del)

                db.session.commit()

        str_commit = """ UPDATE commit_table SET project_name = booking_forecast.project_name, practice = booking_forecast.practice, slt_owner = booking_forecast.slt_owner, quarter = booking_forecast.quarter FROM booking_forecast WHERE booking_forecast.project_name = commit_table.project_name"""
        db.session.execute(str_commit)
        db.session.commit()
        str_wondeals = """ UPDATE wondeals_table SET project_name = booking_forecast.project_name, practice = booking_forecast.practice, slt_owner = booking_forecast.slt_owner, quarter = booking_forecast.quarter, practice_owner = booking_forecast.practice_owner FROM booking_forecast WHERE booking_forecast.project_name = wondeals_table.project_name"""
        db.session.execute(str_wondeals)
        db.session.commit()

        flash("Your booking has been updated!", "success")
        return redirect(url_for("home"))
    elif request.method == "GET":
        form.project_name.data = bookingforecast.project_name
        form.practice.data = bookingforecast.practice
        form.slt_owner.data = bookingforecast.slt_owner
        form.practice_owner.data = bookingforecast.practice_owner
        form.sales_stage.data = bookingforecast.sales_stage
        form.project_type.data = bookingforecast.project_type
        form.region.data = bookingforecast.region
        form.quarter.data = bookingforecast.quarter
        form.country.data = bookingforecast.country
        form.win_prob.data = bookingforecast.win_prob
        form.currency.data = bookingforecast.currency
        form.deal_value.data = bookingforecast.deal_value
    return render_template(
        "bookingforecast.html", title="update button bookingforecast", form=form
    )


@app.route("/display_filter/bookingforecast", methods=["POST", "GET"])
def bookingforecast_filter():
    if request.method == "POST":
        conditions = []
        filter_by_slt = request.form.get("slt_owner")
        filter_by_quater = request.form.get("quarter")
        filter_by_sales_stage = request.form.get("sales_stage")
        filter_by_region = request.form.get("region")
        filter_by_country = request.form.get("country")
        filter_by_status = request.form.get("status")
        filter_by_practice = request.form.get("practice")
        keys = [
            "slt_owner",
            "quarter",
            "sales_stage",
            "region",
            "country",
            "status",
            "practice",
            "practice",
        ]
        str_ = """SELECT * FROM booking_forecast WHERE """
        conditions.append(filter_by_slt)
        conditions.append(filter_by_quater)
        conditions.append(filter_by_sales_stage)
        conditions.append(filter_by_region)
        conditions.append(filter_by_country)
        conditions.append(filter_by_status)
        conditions.append(filter_by_practice)
        for i, j in zip(keys, conditions):
            if j != "":
                str_ += f"""{i}="{j}" AND """
        str_ = str_.rstrip(" AND ")
        str_ = str_.rstrip(" WHERE ")
        # print(str_)
        result = db.session.execute(str_)
        rows = dict()
        for index, row in enumerate(result, start=1):
            temp_list = []
            row_index = f"row{index}"
            for row_data in row:
                temp_list.append(row_data)
                rows[row_index] = temp_list
        # print(rows)
        # Access by positional index
        #     print(r['my_column']) # Access by column name as a string
        #     r_dict = dict(r.items())
        # print(r_dict)
        # with engine.connect() as con:

        #     rs = con.execute('SELECT * FROM book WHERE slt_owner=slt_owner')

        #     for row in rs:
        #         print row
        # brows = BookingForecast.query.filter_by(slt_owner=filter_by_slt).all()
        columns = BookingForecast.__table__.columns.keys()
        # rows = dict()
        # for index, row in enumerate(brows, start=1):
        #     temp_list = []
        #     row_index = f"row{index}"
        #     for row_data in row:
        #         temp_list.append(row_data[1])
        #     rows[row_index] = temp_list
        session["table_data_bookingforecast_filter"] = {
            "table_name": str(BookingForecast.__table__) + " sltowner_filter",
            "columns": columns,
            "rows": rows,
        }
        return redirect(url_for("booking_display"))
    return render_template(
        "bookingforecastfilter.html", title="bookingforecast-filter-sltowner"
    )


@app.route("/booking_display", methods=["POST", "GET"])
def booking_display():
    table_data = session["table_data_bookingforecast_filter"]
    return render_template("bookingfilterdisplay.html", table_data=table_data)



@app.route("/demand_insert", methods=["POST", "GET"])
@login_required
def demand_insert():
    form = DemandForm()
    get_dict_commit={}
    # commit_to_demand_dict = session["commit_to_demand"]
    # print(session["commit_to_demand"])
    # form.project_name.data = commit_to_demand_dict.get("project_name")
    # form.slt_owner.data = commit_to_demand_dict.get("slt_owner")
    # history_page = commit_to_demand_dict.get("history", "demand")
    # session["commit_to_demand"]["history"] = "demand"
    if form.validate_on_submit():
        form_data_dict = form.data
        row2 = Demand(
            project_name=form.project_name.data,
            practice=form.practice.data,
            slt_owner=form.slt_owner.data,
            owner=form.owner.data,
            dsr_id=form.dsr_id.data,
            acc=form_data_dict["acc"],
            practice_owner=form_data_dict["practice_owner"],
            hire_type=form_data_dict["hire_type"],
            new_hire=form_data_dict["new_hire"],
            rep_email=form_data_dict["rep_email"],
            skill=form_data_dict["skill"],
            # other_skill=form_data_dict["other_skill"],
            head_count=form_data_dict["head_count"],
            loc=form_data_dict["loc"],
            # other_loc=form_data_dict["other_loc"],
            emp_grade=form_data_dict["emp_grade"],
            res_status=form_data_dict["res_status"],
            # join_date=form_data_dict["join_date"],
            action_pending=form_data_dict["action_pending"],
            
            ext_int=form_data_dict["ext_int"],
            dor=form_data_dict["dor"],

            age=int((form_data_dict["dor"]-date.today()).days),
            Resource_name=form_data_dict["Resource_name"],
            Resource_emp_id=form_data_dict["Resource_emp_id"],
            no_of_resumes=form_data_dict["no_of_resumes"],
            screen_selects=form_data_dict["screen_selects"],
            updated_date_time=datetime.now(),
            
            last_updated_by=current_user.username,
        )
        db.session.add(row2)
        db.session.commit()
        if form.go_to_commit.data:
            get_dict_commit = request.args.to_dict()
            str_ = f"SELECT win_prob FROM booking_forecast WHERE project_name ='{form.project_name.data}' "
            win_prob_selected = db.session.execute(str_).fetchone()
            if win_prob_selected[0] == 100:
                return redirect(url_for("wondeals_insert", **get_dict_commit))
            elif win_prob_selected[0] >= 50 and win_prob_selected[0] < 100:
                return redirect(url_for("commit_insert", **get_dict_commit))
        flash("Your entry has been added!", "success")
        print("*"*100)
        get_dict_commit=request.args.to_dict()
        for i in get_dict_commit:
            print(i,get_dict_commit[i])
        print("*"*100)
        if not(form.ext_int.data=="Internal" or  form.ext_int.data=="External" and (form.res_status.data =="Allocated" or form.res_status.data =="Cancelled" or form.res_status.data =="Closed" or form.res_status.data =="Hold")):
            
            print("#@#@#@@###################################################################HeRE")
            print(form.ext_int.data, form.res_status.data,type(form.res_status.data))
            return redirect(url_for("interview_insert",**get_dict_commit))
       


    if request.method=="GET":
        form_dict=request.args.to_dict()
        print(form_dict)
        form.project_name.data=form_dict.get("project_name")
        form.slt_owner.data=form_dict.get("slt_owner")
        get_dict_commit=dict(form_dict)


    return render_template(
        "demand_insert.html",
        title="demand-insert",
        form=form,**get_dict_commit
    )


@app.route("/interview_insert", methods=["POST", "GET"])
@login_required
def interview_insert():
   
    session['interview_to_commit']={'flag':'True'}
    form = InterviewForm()
    get_dict_commit=dict()
   
    if form.validate_on_submit():

       
        row1 = Interview(
        res_name=form.res_name.data,
        dsr_id=form.dsr_id.data,
        
        loc=form.loc.data,
        skill=form.skill.data,
        project_name=form.project_name.data,
        ext_int=form.ext_int.data,
        r1_panel=form.r1_panel.data,
        r1_date=form.r1_date.data,
        r1_status=form.r1_status.data,
        r2_panel=form.r2_panel.data,
        r2_date=form.r2_date.data,
        r2_status=form.r2_status.data,
        current_status=form.current_status.data,
        final_select=form.final_select.data,
        act_pending=form.act_pending.data,
        ops_action=form.ops_action.data,
        due_date=form.due_date.data,
        remarks=form.remarks.data,
        active_inactive=form.active_inactive.data,
        updated_date_time=datetime.now(),
        last_updated_by=current_user.username,
        )
        db.session.add(row1)
        db.session.commit()
        flash("Your entry has been added!", "success")
        if form.go_to_commit.data:
            get_dict_commit = request.args.to_dict()
            str_ = f"SELECT win_prob FROM booking_forecast WHERE project_name ='{form.project_name.data}' "
            win_prob_selected = db.session.execute(str_).fetchone()
            if win_prob_selected[0] == 100:
                return redirect(url_for("wondeals_insert", **get_dict_commit))
            elif win_prob_selected[0] >= 50 and win_prob_selected[0] < 100:
                return redirect(url_for("commit_insert", **get_dict_commit))
    
    if request.method=="GET":
        get_dict_commit=request.args.to_dict()
        form.project_name.data=get_dict_commit.get("project_name")
        form.res_name.data=get_dict_commit.get("resource_name")
        #interview_status['flag']='True'
    return render_template("interview_insert.html", title="interview-insert", form=form,**get_dict_commit)


@app.route("/interview/<int:interview_id>/update", methods=["GET", "POST"])
@login_required
def interview_update(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    form = InterviewForm()
    if form.validate_on_submit():

        interview.res_name = form.project_name.data
        interview.loc = form.loc.data
        interview.skill = form.skill.data
        interview.project_name = form.project_name.data
        interview.ext_int = form.ext_int.data
        interview.r1_panel = form.r1_panel.data
        interview.r1_date = form.r1_date.data
        interview.r1_status = form.r1_status.data
        interview.r2_panel = form.r2_panel.data
        interview.r2_date = form.r2_date.data
        interview.r2_status = form.r2_status.data
        interview.current_status = form.current_status.data
        interview.final_select = form.final_select.data
        interview.ops_action = form.ops_action.data
        interview.due_date = form.due_date.data
        interview.remarks = form.remarks.data
        interview.dsr_id = form.dsr_id.data
        interview.active_inactive = form.active_inactive.data
        interview.final_select = form.final_select.data
        interview.updated_date_time = (datetime.now(),)
        interview.last_updated_by = (current_user.username,)

        db.session.commit()
        flash("Your resource has been updated!", "success")
        return redirect(url_for("interview_display"))
    elif request.method == "GET":
        form.res_name.data = interview.res_name
        form.loc.data = interview.loc
        form.skill.data = interview.skill
        form.project_name.data = interview.project_name
        form.ext_int.data = interview.ext_int
        form.r1_panel.data = interview.r1_panel
        form.r1_date.data = interview.r1_date
        form.r1_status.data = interview.r1_status
        form.r2_panel.data = interview.r2_panel
        form.r2_date.data = interview.r2_date
        form.r2_status.data = interview.r2_status
        form.current_status.data = interview.current_status
        form.ops_action.data = interview.ops_action
        form.due_date.data = interview.due_date
        form.remarks.data = interview.remarks
        form.dsr_id.data = interview.dsr_id
        form.active_inactive.data = interview.active_inactive
        form.final_select.data = interview.final_select

    return render_template("interview_insert.html", title="interview-update", form=form)


@app.route("/interview/<int:interview_id>/delete", methods=["GET", "POST"])
@login_required
def interview_delete(interview_id):
    interview = Interview.query.get_or_404(interview_id)
    db.session.delete(interview)
    db.session.commit()
    return redirect(url_for("interview_display"))


@app.route("/booking_dashboard_select", methods=["POST", "GET"])
def booking_dashboard_select():
    if request.method == "POST":
        summary_name = request.form.get("summary_name")
        return redirect(url_for("booking_display_summary", summary_name=summary_name))
    return render_template("booking_dashboard_select.html")


@app.route("/booking_display_summary", methods=["POST", "GET"])
def booking_display_summary():
    df_booking = pd.read_sql_table("booking_forecast", db.session.get_bind())
    print(df_booking)
    form = BookingForecastSummaryForm()
    slt_owner_list = db.session.execute(
        "SELECT DISTINCT slt_owner FROM booking_forecast"
    ).fetchall()
    choices_slt_owner = [("", "--select--")]
    for i in slt_owner_list:
        choices_slt_owner.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.slt_owner.choices = choices_slt_owner
    # quarter_list = db.session.execute(
    #     "SELECT DISTINCT quarter FROM booking_forecast"
    # ).fetchall()
    choices_quarter = [
        ("", "--select--"),
        ("Q1", "Q1"),
        ("Q2", "Q2"),
        ("Q3", "Q3"),
        ("Q4", "Q4"),
    ]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))
    form.quarter.choices = choices_quarter

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        slt_owner_str = form.slt_owner.data
        quarter = form.quarter.data

        if summary_name == "booking_display_summary-1":
            if slt_owner_str != "":
                df_booking_pivot = df_booking.loc[
                    (df_booking["slt_owner"] == f"{slt_owner_str}"), :
                ].pivot_table(
                    index=["practice", "sales_stage"],
                    columns=["quarter"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            else:
                df_booking_pivot = df_booking.pivot_table(
                    index=["practice", "sales_stage"],
                    columns=["quarter"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )

        elif summary_name == "booking_display_summary-2":
            if slt_owner_str != "" and quarter != "":
                df_booking_pivot = df_booking.loc[
                    (
                        (df_booking["slt_owner"] == f"{slt_owner_str}")
                        & (df_booking["quarter"] == f"{quarter}")
                    ),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["sales_stage"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            elif slt_owner_str != "" and quarter == "":
                df_booking_pivot = df_booking.loc[
                    ((df_booking["slt_owner"] == f"{slt_owner_str}")),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["sales_stage"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            elif slt_owner_str == "" and quarter != "":
                df_booking_pivot = df_booking.loc[
                    ((df_booking["quarter"] == f"{quarter}")),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["sales_stage"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            else:
                df_booking_pivot = df_booking.pivot_table(
                    index=["practice"],
                    columns=["sales_stage"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
        elif summary_name == "booking_display_summary-3":
            if slt_owner_str != "" and quarter != "":
                df_booking_pivot = df_booking.loc[
                    (
                        (df_booking["slt_owner"] == f"{slt_owner_str}")
                        & (df_booking["quarter"] == f"{quarter}")
                    ),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["status"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            elif slt_owner_str != "" and quarter == "":
                df_booking_pivot = df_booking.loc[
                    ((df_booking["slt_owner"] == f"{slt_owner_str}")),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["status"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            elif slt_owner_str == "" and quarter != "":
                df_booking_pivot = df_booking.loc[
                    ((df_booking["quarter"] == f"{quarter}")),
                    :,
                ].pivot_table(
                    index=["practice"],
                    columns=["status"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )
            else:
                df_booking_pivot = df_booking.pivot_table(
                    index=["practice"],
                    columns=["status"],
                    values=["deal_value_eur"],
                    aggfunc=np.sum,
                )

        df_booking_pivot = df_booking_pivot.fillna(0)
        # if len(df_booking_pivot.columns) > 1:
        total_list = df_booking_pivot.apply(lambda x: sum(x), axis=1).tolist()
        # else:
        #     series_col = []
        #     for col_name in df_booking_pivot.columns:
        #         series_col.append(df_booking_pivot[col_name])
        # total_list = series_col.tolist()
        df_booking_pivot["total"] = total_list
        grand_total_list = []
        for col in df_booking_pivot:
            grand_total_list.append(sum(df_booking_pivot[col]))
        if summary_name == "booking_display_summary-1":
            df_booking_pivot.loc[("Grand Total", ""), :] = grand_total_list
        else:
            df_booking_pivot.loc[("Grand Total"), :] = grand_total_list

        if summary_name == "booking_display_summary-1":
            # MultiIndex([('deal_value_eur',   ''),
            #             ('deal_value_eur', 'Q1'),
            #             ('deal_value_eur', 'Q2'),
            #             ('deal_value_eur', 'Q3'),
            #             (         'total',   '')],
            #            names=[None, 'quarter'])
            columns_list = []
            for i in df_booking_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_booking_pivot[i] = df_booking_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )

            # df_booking_pivot[("deal_value_eur", "")] = df_booking_pivot[
            #     ("deal_value_eur", "")
            # ].apply(lambda x: "€{:,.2f}".format(x))
            # df_booking_pivot[("deal_value_eur", "Q1")] = df_booking_pivot[
            #     ("deal_value_eur", "Q1")
            # ].apply(lambda x: "€{:,.2f}".format(x))
            # df_booking_pivot[("deal_value_eur", "Q2")] = df_booking_pivot[
            #     ("deal_value_eur", "Q2")
            # ].apply(lambda x: "€{:,.2f}".format(x))
            # df_booking_pivot[("deal_value_eur", "Q3")] = df_booking_pivot[
            #     ("deal_value_eur", "Q3")
            # ].apply(lambda x: "€{:,.2f}".format(x))
            # df_booking_pivot[("total", "")] = df_booking_pivot[("total", "")].apply(
            #     lambda x: "€{:,.2f}".format(x)
            # )
        elif summary_name == "booking_display_summary-2":
            # MultiIndex([('deal_value_eur',     '1. Initiation stage'),
            #             ('deal_value_eur',   '2.Customer Discussion'),
            #             ('deal_value_eur',   '3. Proposal Submitted'),
            #             ('deal_value_eur', '4. Contract Negotiation'),
            #             ('deal_value_eur',          '5. Won-Pending'),
            #             ('deal_value_eur',                  '6. Won'),
            #             (         'total',                        '')],
            #            names=[None, 'sales_stage'])
            columns_list = []
            for i in df_booking_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_booking_pivot[i] = df_booking_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
        elif summary_name == "booking_display_summary-3":
            # MultiIndex([('deal_value_eur',   'Commit'),
            #             ('deal_value_eur', 'Pipeline'),
            #             ('deal_value_eur',      'Won'),
            #             (         'total',         '')],
            #            names=[None, 'status'])
            columns_list = []
            for i in df_booking_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_booking_pivot[i] = df_booking_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )

        print("\n================================")
        print(df_booking_pivot)
        print("\n================================")
        print(df_booking_pivot.columns.values)
        return render_template(
            "bookingforecast_display_summary.html",
            tables=[
                df_booking_pivot.to_html(
                    classes="pivot", sparsify="false", header="true"
                )
            ],
            title=summary_name,
            form=form,
        )
    return render_template(
        "bookingforecast_display_summary.html", title=summary_name, form=form
    )


@app.route("/demand/<int:demand_id>/update", methods=["GET", "POST"])
@login_required
def demand_update(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    form = DemandForm()
    if form.validate_on_submit():
        demand.project_name = form.project_name.data
        demand.practice = form.practice.data
        demand.slt_owner = form.slt_owner.data
        demand.owner = form.owner.data
        demand.dsr_id = form.dsr_id.data
        demand.acc = form.acc.data
        demand.practice_owner = form.practice_owner.data
        demand.hire_type = form.hire_type.data
        demand.new_hire = form.new_hire.data
        demand.rep_email = form.rep_email.data
        demand.skill = form.skill.data
        demand.head_count = form.head_count.data
        demand.loc = form.loc.data
        demand.emp_grade = form.emp_grade.data
        demand.res_status = form.res_status.data
        demand.action_pending = form.action_pending.data
        demand.ext_int = form.ext_int.data
        demand.dor = form.dor.data
        demand.age=int((date.today()-demand.dor).days)
        demand.Resource_name= form.Resource_name.data
        demand.Resource_emp_id= form.Resource_emp_id.data
        demand.no_of_resumes= form.no_of_resumes.data
        demand.screen_selects= form.screen_selects.data
        demand.updated_date_time = datetime.now()
        demand.last_updated_by = current_user.username
        db.session.commit()
        # db.session.execute(f"UPDATE commit_table SET resource_name ={form.re} FROM booking_forecast WHERE booking_forecast.project_name = commit_table.project_name")
        str_wondeals = """ UPDATE wondeals_table SET resource_name = Demand.Resource_name FROM Demand WHERE Demand.project_name = wondeals_table.project_name AND Demand.emp_grade = wondeals_table.resource_level """
        db.session.execute(str_wondeals)
        db.session.commit()

        
        
        flash("Your resource has been updated!", "success")
        return redirect(url_for("demand_display"))
    elif request.method == "GET":
        form.project_name.data = demand.project_name
        form.practice.data = demand.practice
        form.slt_owner.data = demand.slt_owner
        form.owner.data = demand.owner
        form.dsr_id.data = demand.dsr_id
        form.acc.data = demand.acc
        form.practice_owner.data = demand.practice_owner
        form.hire_type.data = demand.hire_type
        form.new_hire.data = demand.new_hire
        form.rep_email.data = demand.rep_email
        form.skill.data = demand.skill
        form.head_count.data = demand.head_count
        form.loc.data = demand.loc
        form.emp_grade.data = demand.emp_grade
        form.res_status.data = demand.res_status
        form.action_pending.data = demand.action_pending
        form.ext_int.data = demand.ext_int
        form.dor.data = demand.dor
        form.Resource_name.data = demand.Resource_name
        form.Resource_emp_id.data = demand.Resource_emp_id
        form.no_of_resumes.data = demand.no_of_resumes
        form.screen_selects.data = demand.screen_selects
       # form.

    return render_template("demand_insert.html", title="demand-update", form=form)


# @app.route("/booking_display_summary", methods=["POST", "GET"])
# def booking_display_summary():
#     table_data = {
#         "table_name": "",
#         "columns": [],
#         "rows": [],
#     }
#     if request.method == "POST":
#         slt_owner_str = request.form.get("slt_owner")
#         columns_str = "quarter, project_name, sales_stage, deal_value_eur"
#         result_group_by = db.session.execute(
#             f"SELECT {columns_str} FROM booking_forecast GROUP BY quarter,project_name,sales_stage HAVING slt_owner = '{slt_owner_str}' ORDER BY quarter,sales_stage "
#         ).fetchall()
#         print(slt_owner_str)
#         sum_group_by = db.session.execute(
#             f"SELECT sum(deal_value_eur),quarter FROM (SELECT * FROM booking_forecast WHERE slt_owner = '{slt_owner_str}') GROUP BY quarter "
#         ).fetchall()
#         print(sum_group_by)
#         total_sum_group_by = db.session.e
#             f"SELECT sum(deal_value_eur) FROM booking_forecast WHERE slt_owner = '{slt_owner_str}' "
#         ).fetchall()
#         print(total_sum_group_by)
#         if result_group_by:
#             count = 0
#             print(len(sum_group_by))
#             templist = []
#             for i in range(0, len(result_group_by) - 1):
#                 print(count)
#                 if result_group_by[i][0] != result_group_by[i + 1][0]:
#                     # print(list1[i])
#                     str_ = f"{result_group_by[i][0]} Total"
#                     # print(list2[count][0])
#                     templist.append((str_, "", "", sum_group_by[count][0]))
#                     count = count + 1
#                 else:
#                     # print(list1[i])
#                     templist.append(result_group_by[i])
#             str_ = f"{result_group_by[-1][0]} Total"
#             templist.append((str_, "", "", sum_group_by[count][0]))
#             str_ = "Total"
#             templist.append((str_, "", "", total_sum_group_by[0][0]))
#             print(templist)
#         else:
#             templist = []
#         table_data["table_name"] = "Summary of " + slt_owner_str
#         table_data["columns"] = [
#             "quarter",
#             "project_name",
#             "sales_stage",
#             "deal_value_eur",
#         ]
#         table_data["rows"] = templist
#         for row_data in table_data["rows"]:
#             print(row_data)
#     return render_template(
#         "bookingforecast_display_summary.html", table_data=table_data
#     )


@app.route("/wondeals/<int:wondeals_id>/delete", methods=["GET", "POST"])
@login_required
def wondeals_delete(wondeals_id):
    wondeals = WonDeals.query.get_or_404(wondeals_id)
    db.session.delete(wondeals)
    db.session.commit()
    return redirect(url_for("wondeals_display"))


@app.route("/commit/<int:commit_id>/delete", methods=["GET", "POST"])
@login_required
def commit_delete(commit_id):
    commit = Commit.query.get_or_404(commit_id)
    db.session.delete(commit)
    db.session.commit()
    return redirect(url_for("commit_display"))


@app.route(
    "/bookingforecast/<string:bookingforecast_id>/delete", methods=["GET", "POST"]
)
@login_required
def bookingforecast_delete(bookingforecast_id):
    bookingforecast = BookingForecast.query.get_or_404(bookingforecast_id)
    db.session.delete(bookingforecast)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/excel_upload", methods=["GET", "POST"])
def excel_upload():

    if request.method == "POST":
        file_upload = request.files["file_upload"]
        table_name = request.form.get("table_name")
        if table_name != "":
            if file_upload.filename == "Interview.xlsx" or file_upload.filename == "Demand.xlsx":
                df = pd.read_excel(file_upload)
            else:
                df = pd.read_excel(file_upload, na_filter=False)
            df_col_types=[]
            print("*"*50)
            print(df.dtypes)
            for i in df.dtypes:
                df_col_types.append(i)
            # print(df_col_types)
            print("*"*50)
            table_keys = None
            table_col_type_list=[]
            if table_name == "Demand":
                table_keys = Demand.__table__.columns.keys()
                table_col_types=Demand.__table__.columns
                for i in table_col_types:
                    table_col_type_list.append(i.type)
            elif table_name == "Interview":
                table_keys = Interview.__table__.columns.keys()
                table_col_types=Interview.__table__.columns
                for i in table_col_types:
                    table_col_type_list.append(i.type)
            elif table_name == "booking_forecast":
                table_keys = BookingForecast.__table__.columns.keys()
                table_col_types=BookingForecast.__table__.columns
                for i in table_col_types:
                    table_col_type_list.append(i.type)
            elif table_name == "commit_table":
                table_keys = Commit.__table__.columns.keys()
                table_col_types=Commit.__table__.columns
                for i in table_col_types:
                    table_col_type_list.append(i.type)
            elif table_name == "wondeals_table":
                table_keys = WonDeals.__table__.columns.keys()
                table_col_types=WonDeals.__table__.columns
                for i in table_col_types:
                    table_col_type_list.append(i.type)
            print(table_col_type_list)

            if table_keys == list(df.columns):
                df.to_sql(
                    table_name,
                    con=db.session.get_bind(),
                    if_exists="append",
                    index=False,
                )
                flash("Your data has been uploaded!", "success")
            else:
                flash("Your data has not been uploaded!", "danger")
    return render_template("excel_upload.html")


# v
@app.route("/display_filter/demand_filter", methods=["POST", "GET"])
def demand_filter():
    if request.method == "POST":
        conditions = []
        filter_by_dsrid = request.form.get("dsr_id")
        filter_by_new_hire = request.form.get("new_hire")
        # filter_by_project_name = request.form.get("project_name")

        filter_by_slt_owner = request.form.get("slt_owner")
        filter_by_acc = request.form.get("acc")
        filter_by_skill = request.form.get("skill")
        filter_by_loc = request.form.get("loc")
        filter_by_emp_grade = request.form.get("emp_grade")
        # filter_by_owner = request.form.get("owner")

        # filter_by_practice_owner = request.form.get("practice_owner")
        # filter_by_hire_type = request.form.get("hire_type")

        # filter_by_rep_email = request.form.get("rep_email")
        # filter_by_skill = request.form.get("skill")
        # filter_by_loc = request.form.get("loc")
        # filter_by_emp_grade = request.form.get("emp_grade")
        # filter_by_res_status = request.form.get("res_status")

        # keys = [
        #     "dsr_id",
        #     "project_name",
        #     "slt_owner",
        #     "acc",
        #     "hire_type",
        #     "new_hire",
        #     "rep_email",
        #     "skill",
        #     "loc",
        #     "emp_grade",
        #     "res_status"
        # ]
        keys = ["dsr_id", "new_hire", "slt_owner", "acc", "skill", "loc", "emp_grade"]
        str_ = """SELECT * FROM Demand WHERE """
        conditions.append(filter_by_dsrid)
        # conditions.append(filter_by_project_name)
        conditions.append(filter_by_new_hire)
        conditions.append(filter_by_slt_owner)
        # conditions.append(filter_by_owner)
        conditions.append(filter_by_acc)
        conditions.append(filter_by_skill)
        conditions.append(filter_by_loc)
        conditions.append(filter_by_emp_grade)
        # conditions.append(filter_by_practice_owner)
        # conditions.append(filter_by_hire_type)

        # conditions.append(filter_by_rep_email)
        # c
        # conditions.append(filter_by_loc)
        # conditions.append(filter_by_emp_grade)
        # conditions.append(filter_by_res_status)
        for i, j in zip(keys, conditions):
            print(i, j)
        for i, j in zip(keys, conditions):
            if j != "":
                str_ += f"""{i}="{j}" AND """
        str_ = str_.rstrip(" AND ")
        str_ = str_.rstrip(" WHERE ")
        print(str_)
        result = db.session.execute(str_)
        rows = dict()
        for index, row in enumerate(result, start=1):
            temp_list = []
            row_index = f"row{index}"
            for row_data in row:
                temp_list.append(row_data)
                rows[row_index] = temp_list
        columns = Demand.__table__.columns.keys()
        session["table_data_demand_filter"] = {
            "table_name": str(Demand.__table__) ,
            "columns": columns,
            "rows": rows,
        }
        return redirect(url_for("demand_filter_display"))
    return render_template("demandfilter.html", title="demand-filter")


# v
@app.route("/demand_filter_display", methods=["POST", "GET"])
def demand_filter_display():
    table_data = session["table_data_demand_filter"]
    # print(table_data)
    return render_template("demandfilter_display.html", table_data=table_data)


# @app.route("/updatebookingforecastdata/delete", methods=["GET", "POST"])
# @login_required
# def delete_bookingforecast(post_id):
#     post = Post.query.get_or_404(post_id)
#     if post.author != current_user:
#         abort(403)
#     db.session.delete(post)
#     db.session.commit()
#     flash("Your post has been deleted!", "success")
#     return redirect(url_for("main.home"))


# @app.route("/updatebookingforecastdata", methods=["GET", "POST"])
# @login_required
# def updatebookingforecastdata():
#     form = BookingForecastForm()
#     if request.method == "GET":
#         d = request.args.to_dict()
#         form.project_name.data = d.get("bookingforecast_id")
#         # search = "%{}%".format(str_)
#         # bookingforecast = BookingForecast.query.filter(
#         #     BookingForecast.project_name.like(search)
#         # ).first()
#         bookingforecast = BookingForecast.query.get_or_404(d.get("bookingforecast_id"))
#         form.practice.data = bookingforecast.practice
#         form.slt_owner.data = bookingforecast.slt_owner
#         form.sales_stage.data = bookingforecast.sales_stage
#         form.project_type.data = bookingforecast.project_type
#         form.region.data = bookingforecast.region
#         form.country.data = bookingforecast.country
#         form.win_prob.data = bookingforecast.win_prob
#         form.currency.data = bookingforecast.currency
#         form.deal_value.data = bookingforecast.deal_value
#         print(bookingforecast)
#         # form.start_date_deal.data = bookingforecast.start_date_deal
#         # form.end_date_deal.data = bookingforecast.end_date_deal

#     if form.validate_on_submit():
#         # bookingforecast = BookingForecast.query.filter(
#         #     BookingForecast.project_name.like(search)
#         # ).first()
#         bookingforecast = BookingForecast.query.get_or_404(form.project_name.data)

#         deal_value_eur_ = (
#             form.deal_value.data
#             * Flask_Project_data.currency_rate_dict.get(form.currency.data)
#         )
#         print(form.win_prob.data)
#         if form.win_prob.data > 0.5 and form.win_prob.data < 1.0:
#             status_ = "Commit"
#         elif form.win_prob.data < 0.5 and form.win_prob.data > 0:
#             status_ = "Pipeline"
#         else:
#             status_ = "Won"

#         bookingforecast.project_name = form.project_name.data
#         bookingforecast.practice = form.practice.data
#         bookingforecast.slt_owner = form.slt_owner.data
#         bookingforecast.sales_stage = form.sales_stage.data
#         bookingforecast.project_type = form.project_type.data
#         bookingforecast.region = form.region.data
#         bookingforecast.country = form.country.data
#         bookingforecast.win_prob = form.win_prob.data
#         bookingforecast.currency = form.currency.data
#         bookingforecast.deal_value = form.deal_value.data
#         # bookingforecast.start_date_deal = form.start_date_deal.data
#         # bookingforecast.end_date_deal = form.end_date_deal.data
#         bookingforecast.deal_value_eur = deal_value_eur_
#         bookingforecast.status = status_
#         print("hello")
#         print(bookingforecast)
#         db.session.commit()
#         flash("Your record has been Updated!", "success")
#         return redirect(url_for("home"))
#     return render_template(
#         "bookingforecast.html", title="Update BookingForecast data", form=form
#     )


# @app.route("/updatedata", methods=["GET", "POST"])
# @login_required
# def updatedata():
#     form = UpdataDataForm()
#     if form.validate_on_submit():
#         df = pd.read_excel("flask_excel_app/temp.xlsx")
#         form_data_dict = form.data
#         del form_data_dict["submit"]
#         del form_data_dict["csrf_token"]
#         form_data_dict["Project_id"] = form_data_dict.pop("project_id")
#         form_data_dict["Project_Name"] = form_data_dict.pop("project_name")
#         form_data_dict["Practice"] = form_data_dict.pop("practice")
#         form_data_dict["SLT"] = form_data_dict.pop("slt")
#         form_data_dict["Practice Owner"] = form_data_dict.pop("practice_owner")
#         form_data_dict["Quarter"] = form_data_dict.pop("quarter")
#         form_data_dict["Sales Stage"] = form_data_dict.pop("sales_stage")
#         form_data_dict["Project Type"] = form_data_dict.pop("project_type")
#         form_data_dict["Region"] = form_data_dict.pop("region")
#         form_data_dict["Country"] = form_data_dict.pop("country")
#         form_data_dict["Deal value"] = form_data_dict.pop("deal_value")
#         form_data_dict["Start_Date®"] = form_data_dict.pop("start_date")
#         form_data_dict["End_Date(R)"] = form_data_dict.pop("end_date")
#         form_data_dict["ORC"] = form_data_dict.pop("cor")
#         projcet_selected = form_data_dict["Project_Name"]
#         for i in form_data_dict.keys():
#             df.loc[df["Project_Name"] == projcet_selected, i] = form_data_dict[i]
#         with pd.ExcelWriter(
#             "C:/Users/zusankal/Desktop/newflaskapp/flask_excel_app/temp.xlsx",
#             mode="w",
#             engine="openpyxl",
#             if_sheet_exists="replace",
#         ) as writer:
#             df.to_excel(writer, sheet_name="Sheet1", index=False, header=True)
#     #     return redirect(next_page) if next_page else redirect(url_for("home"))
#     # else:
#     #     flash("", "danger")
#     return render_template("updatedata.html", title="UpdateData", form=form)


@app.route("/display_filter/commit", methods=["POST", "GET"])
def commit_filter():
    if request.method == "POST":
        conditions = []

        filter_by_project_name = request.form.get("project_name")
        filter_by_slt = request.form.get("slt_owner")
        filter_by_project_manager = request.form.get("project_manager")
        filter_by_resource_level = request.form.get("resource_level")
        filter_by_quarter = request.form.get("quarter")
        filter_by_onshore_offshore = request.form.get("onshore_offshore")
        filter_by_practice = request.form.get("practice")

        keys = [
            "project_name",
            "slt_owner",
            "project_manager",
            "resource_level",
            "quarter",
            "onshore_offshore",
            "practice",
        ]
        str_ = """SELECT * FROM commit_table WHERE """

        conditions.append(filter_by_project_name)
        conditions.append(filter_by_slt)
        conditions.append(filter_by_project_manager)
        conditions.append(filter_by_resource_level)
        conditions.append(filter_by_quarter)
        conditions.append(filter_by_onshore_offshore)
        conditions.append(filter_by_practice)

        for i, j in zip(keys, conditions):
            if j != "":
                str_ += f"{i}='{j}' AND "
        str_ = str_.rstrip(" AND ")
        # print(str_)
        result = db.session.execute(str_)
        rows = dict()
        for index, row in enumerate(result, start=1):
            temp_list = []
            row_index = f"row{index}"
            for row_data in row:
                temp_list.append(row_data)
                rows[row_index] = temp_list

        columns = Commit.__table__.columns.keys()

        session["table_data_commit_filter"] = {
            "table_name": str(Commit.__table__),
            "columns": columns,
            "rows": rows,
        }
        return redirect(url_for("commit_filter_display"))
    return render_template("commitfilter.html", title="commit-filter")


@app.route("/commit_filter_display", methods=["POST", "GET"])
def commit_filter_display():
    table_data = session["table_data_commit_filter"]
    return render_template("commitfilterdisplay.html", table_data=table_data)


@app.route("/display_filter/wondeals", methods=["POST", "GET"])
def wondeals_filter():
    if request.method == "POST":
        conditions = []
        filter_by_project_id = request.form.get("project_id")
        filter_by_project_name = request.form.get("project_name")
        filter_by_slt = request.form.get("slt_owner")
        filter_by_practice_owner = request.form.get("practice_owner")
        filter_by_practice = request.form.get("practice")
        filter_by_quarter = request.form.get("quarter")
        filter_by_project_manager = request.form.get("project_manager")
        filter_by_resource_level = request.form.get("resource_level")
        filter_by_onshore_offshore = request.form.get("onshore_offshore")
        filter_by_project_country = request.form.get("project_country")

        keys = [
            "project_id",
            "project_name",
            "slt_owner",
            "practice_owner",
            "practice",
            "quarter",
            "project_manager",
            "resource_level",
            "onshore_offshore",
            "project_country",
        ]
        str_ = """SELECT * FROM wondeals_table WHERE """
        conditions.append(filter_by_project_id)
        conditions.append(filter_by_project_name)
        conditions.append(filter_by_slt)
        conditions.append(filter_by_practice_owner)
        conditions.append(filter_by_practice)
        conditions.append(filter_by_quarter)
        conditions.append(filter_by_project_manager)
        conditions.append(filter_by_resource_level)
        conditions.append(filter_by_onshore_offshore)
        conditions.append(filter_by_project_country)
        for i, j in zip(keys, conditions):
            if j != "":
                str_ += f"{i}='{j}' AND "
        str_ = str_.rstrip(" AND ")
        # print(str_)
        result = db.session.execute(str_)
        rows = dict()
        for index, row in enumerate(result, start=1):
            temp_list = []
            row_index = f"row{index}"
            for row_data in row:
                temp_list.append(row_data)
                rows[row_index] = temp_list
        # print(rows)
        # Access by positional index
        #     print(r['my_column']) # Access by column name as a string
        #     r_dict = dict(r.items())
        # print(r_dict)
        # with engine.connect() as con:

        #     rs = con.execute('SELECT * FROM book WHERE slt_owner=slt_owner')

        #     for row in rs:
        #         print row
        # brows = BookingForecast.query.filter_by(slt_owner=filter_by_slt).all()
        columns = WonDeals.__table__.columns.keys()
        # rows = dict()
        # for index, row in enumerate(brows, start=1):
        #     temp_list = []
        #     row_index = f"row{index}"
        #     for row_data in row:
        #         temp_list.append(row_data[1])
        #     rows[row_index] = temp_list
        
        session["table_data_wondeals_filter"] = {
            "table_name": str(WonDeals.__table__) + "Filter",
            "columns": columns,
            "rows": rows,
        }
        return redirect(url_for("won_display"))
    return render_template("wondealsfilter.html", title="wondeals-filter")


@app.route("/won_display", methods=["POST", "GET"])
def won_display():
    table_data = session["table_data_wondeals_filter"]
    return render_template("wondealsfilterdisplay.html", table_data=table_data)

######################################################################################################
####################################### Commit Dashboard ###########################################################
'''
@app.route("/commit_display_summary", methods=["POST", "GET"])
def commit_display_summary():
    df_commit = pd.read_sql_table("commit_table", db.session.get_bind())
    print(df_commit)
    form = CommitSummaryForm()
    practice_list = db.session.execute(
        "SELECT DISTINCT practice FROM commit_table"
    ).fetchall()
    choices_practice = [("", "--select--")]
    for i in practice_list:
        choices_practice.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.practice.choices = choices_practice
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        practice_str = form.practice.data
        
        if practice_str != "":
            df_commit_pivot = df_commit.loc[
                (df_commit["practice"] == f"{practice_str}"), :
            ].pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
            )
        else:
            df_commit_pivot = df_commit.pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
                )

        
        df_commit_pivot = df_commit_pivot.fillna(0)
        # if len(df_booking_pivot.columns) > 1:
        total_list = df_commit_pivot.apply(lambda x: sum(x), axis=1).tolist()
        # else:
        #     series_col = []
        #     for col_name in df_booking_pivot.columns:
        #         series_col.append(df_booking_pivot[col_name])
        # total_list = series_col.tolist()
        df_commit_pivot["total"] = total_list
        df_commit_pivot = df_commit_pivot[["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec","total"]]

       
        grand_total_list = []
        for col in df_commit_pivot:
            grand_total_list.append(sum(df_commit_pivot[col]))
        if summary_name == "commit_display_summary-1":
            df_commit_pivot.loc[("Grand Total", ""), :] = grand_total_list
            columns_list = []
            for i in df_commit_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_commit_pivot[i] = df_commit_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
        else:
            df_commit_pivot.loc[("Grand Total"), :] = grand_total_list
            columns_list = []
            for i in df_commit_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_commit_pivot[i] = df_commit_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
        print("\n================================")
        print(df_commit_pivot)
        print("\n================================")
        print(df_commit_pivot.columns.values)
        return render_template(
            "commit_display_summary.html",
            tables=[
                df_commit_pivot.to_html(
                    classes="pivot", sparsify="false", header="true"
                )
            ],
            title=summary_name,
            form=form,
        )
    return render_template(
        "commit_display_summary.html", title=summary_name, form=form
    )

'''
#####################################################################################################
################################## Won Deals Dashboard ###################################################



@app.route("/wondeals_display_summary", methods=["POST", "GET"])
def wondeals_display_summary():
    df_wondeals = pd.read_sql_table("wondeals_table", db.session.get_bind())
    print(df_wondeals)
    form = WonDealsSummaryForm()
    practice_list = db.session.execute(
        "SELECT DISTINCT practice FROM wondeals_table"
    ).fetchall()
    choices_practice = [("", "--select--")]
    for i in practice_list:
        choices_practice.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.practice.choices = choices_practice
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        practice_str = form.practice.data
        
        if practice_str != "":
            df_wondeals_pivot = df_wondeals.loc[
                (df_wondeals["practice"] == f"{practice_str}"), :
            ].pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
            )
           
        else:
            df_wondeals_pivot = df_wondeals.pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
                )

        
        df_wondeals_pivot = df_wondeals_pivot.fillna(0)
        # if len(df_booking_pivot.columns) > 1:
        total_list = df_wondeals_pivot.apply(lambda x: sum(x), axis=1).tolist()
        # else:
        #     series_col = []
        #     for col_name in df_booking_pivot.columns:
        #         series_col.append(df_booking_pivot[col_name])
        # total_list = series_col.tolist()
        df_wondeals_pivot["total"] = total_list
        df_wondeals_pivot = df_wondeals_pivot[["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec","total"]]


        grand_total_list = []
        for col in df_wondeals_pivot:
            grand_total_list.append(sum(df_wondeals_pivot[col]))
            
           
        
        if summary_name == "wondeals_display_summary-1":
            
            df_wondeals_pivot.loc[("Grand Total"), :] = grand_total_list
            columns_list = []
            for i in df_wondeals_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_wondeals_pivot[i] = df_wondeals_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
           
        else:
            
            df_wondeals_pivot.loc[("Grand Total"), :] = grand_total_list
            columns_list = []
            for i in df_wondeals_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_wondeals_pivot[i] = df_wondeals_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
            
        print("\n================================")
        print(df_wondeals_pivot)
        print("\n================================")
        print(df_wondeals_pivot.columns.values)
        return render_template(
            "wondeals_display_summary.html",
            tables=[
                df_wondeals_pivot.to_html(
                    classes="pivot", sparsify="false", header="true"
                )
            ],
            title=summary_name,
            form=form,
        )
    return render_template(
        "wondeals_display_summary.html", title=summary_name, form=form
    )


@app.route("/demand/<int:demand_id>/delete", methods=["GET", "POST"])
@login_required
def demand_delete(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    db.session.delete(demand)
    db.session.commit()
    return redirect(url_for("demand_display"))


@app.route("/demand_display_summary", methods=["POST", "GET"])
def demand_display_summary():

    df_demand = pd.read_sql_table("Demand", db.session.get_bind())
    df_demand = df_demand.iloc[:, :-2]
    form = DemandSummaryForm()

    practice = db.session.execute("SELECT DISTINCT practice FROM Demand").fetchall()
    choices_practice = [("", "--select--")]
    for i in practice:
        choices_practice.append((i[0], i[0]))

    list_ = db.session.execute("SELECT DISTINCT res_status FROM Demand").fetchall()
    res_status_list = ["slt_owner", "acc"]
    for i in list_:
        res_status_list.append(i[0])

    form.practice.choices = choices_practice
    if request.method == "POST":
        practice_str = form.practice.data
        new_cols = list(df_demand["res_status"].unique())
        if practice_str != "":
            df_demand = df_demand.loc[(df_demand["practice"] == f"{practice_str}"), :]
            df_demand.reset_index(drop=True, inplace=True)
        df_demand.reset_index(drop=True, inplace=True)
        for i in new_cols:
            df_demand[i] = 0

        c = -1
        for i in df_demand["res_status"]:
            c = c + 1
            df_demand.loc[c, i] = 1

        df_demand.dropna(subset=["dsr_id"], axis=0, inplace=True)
        data1 = df_demand.loc[:, res_status_list]
        data = data1.groupby(["acc", "slt_owner"]).sum()
        data.loc[("Grand Total", ""), :] = data.apply(lambda x: sum(x))
        data.loc[:, "Total"] = data.apply(lambda x: sum(x), axis=1)

        columns_list=[]
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: int(x)
                    ) 

        return render_template(
            "demand_display_summary.html",
            tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
            title="demand-dashboard",
            form=form,
        )
    return render_template(
        "demand_display_summary.html", title="demand-dashboard", form=form
    )



@app.route("/display_filter/interview", methods=["POST", "GET"])
def interview_filter():
    if request.method == "POST":
        conditions = []
        filter_by_project_name = request.form.get("project_name")
        filter_by_skill = request.form.get("skill")
        filter_by_res_name = request.form.get("res_name")
        
        keys = [
            "project_name",
            "skill",
            "res_name",
            
        ]
        str_ = """SELECT * FROM Interview WHERE """
        conditions.append(filter_by_project_name)
        conditions.append(filter_by_skill)
        conditions.append(filter_by_res_name)
       
        for i, j in zip(keys, conditions):
            if j != "":
                str_ += f"""{i}="{j}" AND """
        str_ = str_.rstrip(" AND ")
        # print(str_)
        result = db.session.execute(str_)
        rows = dict()
        for index, row in enumerate(result, start=1):
            temp_list = []
            row_index = f"row{index}"
            for row_data in row:
                temp_list.append(row_data)
                rows[row_index] = temp_list
        
        columns = Interview.__table__.columns.keys()
       
        session["table_data_interview_filter"] = {
            "table_name": str(Interview.__table__) ,
            "columns": columns,
            "rows": rows,
        }
        return redirect(url_for("interview_filter_display"))
    return render_template(
        "interviewfilter.html", title="interview-filter"
    )

@app.route("/interview_filter_display", methods=["POST", "GET"])
def interview_filter_display():
    table_data = session["table_data_interview_filter"]
    # print(table_data)
    return render_template("interviewfilterdisplay.html", table_data=table_data)


    
@app.route("/wondeals/<string:email_id>/<int:project_id>/leaves", methods=["POST", "GET"])
def wondeals_leaves(email_id,project_id):
    form=leaves_form()
    form.project_id.data=project_id
    form.email_id.data=email_id
    if form.validate_on_submit():
        start_date=form.start_date.data
        end_date=form.end_date.data
        row1 = Leaves(
            project_id=project_id,
            email_id=email_id,
            start_date=start_date,
            end_date=end_date
        )
        db.session.add(row1)
        db.session.commit()
        st=f"SELECT start_date,end_date from leaves where email_id='{email_id}';"
        res=db.session.execute(st).fetchall()
        pro_dates=dict()
        list1,list2=[],[]
        for i,j in res:
            list1.append(i)
            list2.append(j)
        st=f"SELECT start_date_wondeals,end_date_wondeals,project_id,resource_country from wondeals_table where email_id='{email_id}';"
        res=db.session.execute(st).fetchall()
        for i,j,k,con in res:
            print(i.split(' ')[0],j.split(' ')[0])
            pro_dates[k]=functions().get_dates_list(list1,list2,datetime.strptime(i.split(' ')[0], '%Y-%m-%d'),datetime.strptime(j.split(' ')[0], '%Y-%m-%d'),con.split('_')[0])
        print(pro_dates)
        months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
        months_leaves={x:0 for x in months}
        pro_months_dates=dict()
        for i,j in pro_dates.items():
            months_leaves={x:0 for x in months}
            for k in j:
                months_leaves[months[k.month-1]]+=1
            pro_months_dates[i]=months_leaves
        print("--------------------------")
        print(pro_months_dates)
        st="SELECT project_id"
        for i,j in pro_months_dates.items():
            for k,l in j.items():
                st=st+',days_'+k
            st=st+f" from wondeals_table where project_id={i} and email_id='{email_id}';"
            print(st)
            init_days=list(*db.session.execute(st).fetchall())[1:]
            after_leaves=[]
            print('---------------------before leave days -----------------')
            print(init_days)
            print('-------------------after leave days---------------------')
            for q,w in zip(init_days,pro_months_dates[i].values()):
                after_leaves.append(q-w)
            print(after_leaves)
            st=f"SELECT revenue_daily_rate,adrc from wondeals_table where project_id={i} and email_id='{email_id}';"
            print(st)
            li=list(*db.session.execute(st).fetchall())
            print(li)
            revenue_daily_rate,adrc=li[0],li[1]
            print("revenue daily rate = ",revenue_daily_rate)
            print("ADRC = ",adrc)
            eurs=[]
            for days in after_leaves:
                eurs.append(days*revenue_daily_rate)
            total_renvenue=sum(eurs)
            total_days=sum(after_leaves)
            total_cost=total_days*adrc
            cm=total_renvenue-total_cost
            cm_percent=(cm/total_renvenue)*100
            st=f'UPDATE wondeals_table SET cm={cm},total_cost={total_cost},total_revenue={total_renvenue},total_days={total_days},resource_wise_cm_percet={cm_percent}'
            for mon in range(len(after_leaves)):
                st=st+f',days_{months[mon]}={after_leaves[mon]},eur_{months[mon]}={eurs[mon]}'
            st=st+f" where project_id={i} and email_id='{email_id}'"
            print('---------------final update statement----------------')
            print(st)
            db.session.execute(st)
            db.session.commit()
            return redirect(url_for("wondeals_display"))
    return render_template('leaves.html',form=form)
    




@app.route("/commit_display_summary", methods=["POST", "GET"])
def commit_display_summary():
    df_commit = pd.read_sql_table("commit_table", db.session.get_bind())
    print(df_commit)
    form = CommitSummaryForm()
    practice_list = db.session.execute(
        "SELECT DISTINCT practice FROM commit_table"
    ).fetchall()
    choices_practice = [("", "--select--")]
    for i in practice_list:
        choices_practice.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.practice.choices = choices_practice
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        practice_str = form.practice.data
        
        if practice_str != "":
            df_commit_pivot = df_commit.loc[
                (df_commit["practice"] == f"{practice_str}"), :
            ].pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
            )
        else:
            df_commit_pivot = df_commit.pivot_table(
                index=["practice"],
                columns=[],
                values=["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec"],
                aggfunc=np.sum,
                )

        
        df_commit_pivot = df_commit_pivot.fillna(0)
        # if len(df_booking_pivot.columns) > 1:
        total_list = df_commit_pivot.apply(lambda x: sum(x), axis=1).tolist()
        # else:
        #     series_col = []
        #     for col_name in df_booking_pivot.columns:
        #         series_col.append(df_booking_pivot[col_name])
        # total_list = series_col.tolist()
        df_commit_pivot["total"] = total_list
        df_commit_pivot = df_commit_pivot[["eur_jan","eur_feb","eur_mar","eur_apr","eur_may","eur_jun","eur_jul","eur_aug","eur_sep","eur_oct","eur_nov","eur_dec","total"]]

       
        grand_total_list = []
        for col in df_commit_pivot:
            grand_total_list.append(sum(df_commit_pivot[col]))
        if summary_name == "commit_display_summary-1":
            df_commit_pivot.loc[("Grand Total"), :] = grand_total_list
            columns_list = []
            for i in df_commit_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_commit_pivot[i] = df_commit_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
        else:
            df_commit_pivot.loc[("Grand Total"), :] = grand_total_list
            columns_list = []
            for i in df_commit_pivot.columns.values.tolist():
                columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    df_commit_pivot[i] = df_commit_pivot[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    )
        print("\n================================")
        print(df_commit_pivot)
        print("\n================================")
        print(df_commit_pivot.columns.values)
        return render_template(
            "commit_display_summary.html",
            tables=[
                df_commit_pivot.to_html(
                    classes="pivot", sparsify="false", header="true"
                )
            ],
            title=summary_name,
            form=form,
        )
    return render_template(
        "commit_display_summary.html", title=summary_name, form=form
    )


@app.route("/commit_dashboard_select", methods=["POST", "GET"])
def commit_dashboard_select():
    if request.method == "POST":
        summary_name = request.form.get("summary_name")
        if(summary_name == "commit_display_summary-1"):
            return redirect(url_for("commit_display_summary", summary_name=summary_name))
        else:
             return redirect(url_for("commit_display_summary1", summary_name=summary_name))
    return render_template("commit_dashboard_select.html")


@app.route("/commit_display_summary1", methods=["POST", "GET"])
def commit_display_summary1():
    df_commit = pd.read_sql_table("commit_table", db.session.get_bind())
    print(df_commit)
    form = CommitSummaryForm()
    quarter_list = db.session.execute(
        "SELECT DISTINCT quarter FROM commit_table"
    ).fetchall()
    choices_quarter = [("", "--select--")]
    for i in quarter_list:
        choices_quarter.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.quarter.choices = choices_quarter
    res_status_list = ["slt_owner", "project_name","total_revenue"]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        quarter_str = form.quarter.data
        
        if quarter_str != "":
            df_commit = df_commit.loc[
                (df_commit["quarter"] == f"{quarter_str}"), :]
            df_commit.reset_index(drop=True, inplace=True)
        df_commit.reset_index(drop=True, inplace=True)
        data1 = df_commit.loc[:, res_status_list]
        data = data1.groupby(["slt_owner","project_name"]).sum()  
        
        data.loc[("Grand Total",""),:] = data.apply(lambda x: sum(x))
        
      
       
        return render_template(
            "commit_display_summary1.html",tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
                title="commit-dashboard",
                form=form,
                summary_name=summary_name
        )
    return render_template(
        "commit_display_summary1.html", title="commit-dashboard", form=form,summary_name=summary_name
    )


@app.route("/wondeals_display_summary1", methods=["POST", "GET"])
def wondeals_display_summary1():
    df_wondeals = pd.read_sql_table("wondeals_table", db.session.get_bind())
    print(df_wondeals)
    form = WonDealsSummaryForm()
    project_country_list = db.session.execute(
        "SELECT DISTINCT project_country FROM wondeals_table"
    ).fetchall()
    choices_project_country= [("", "--select--")]
    for i in project_country_list:
        choices_project_country.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.project_country.choices = choices_project_country
    res_status_list = ["slt_owner","project_name","total_days","total_revenue","resource_wise_cm_percet"]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        project_country_str = form.project_country.data
        
        if project_country_str != "":
            df_wondeals = df_wondeals.loc[
                (df_wondeals["project_country"] == f"{project_country_str}"), :]
            df_wondeals.reset_index(drop=True, inplace=True)
        df_wondeals.reset_index(drop=True, inplace=True)
        data1 = df_wondeals.loc[:, res_status_list]
        data = data1.groupby(["slt_owner","project_name"]).sum()  
        
        data.loc[("Grand Total",""),:] = data.apply(lambda x: sum(x))
        
        '''columns_list = []
        
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    ) '''
           
       
        return render_template(
            "wondeals_display_summary1.html",tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
                title="wondeals-dashboard",
                form=form,
                summary_name=summary_name
        )
    return render_template(
        "wondeals_display_summary1.html", title="wondeals-dashboard", form=form,summary_name=summary_name
    )



@app.route("/wondeals_display_summary2", methods=["POST", "GET"])
def wondeals_display_summary2():
    df_wondeals = pd.read_sql_table("wondeals_table", db.session.get_bind())
    print(df_wondeals)
    form = WonDealsSummaryForm()
    slt_owner_list = db.session.execute(
        "SELECT DISTINCT slt_owner FROM wondeals_table"
    ).fetchall()
    choices_slt_owner= [("", "--select--")]
    for i in slt_owner_list:
        choices_slt_owner.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.slt_owner.choices = choices_slt_owner
    res_status_list = ["email_id","resource_level","project_name","total_days","total_revenue"]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        slt_owner_str = form.slt_owner.data
        
        if slt_owner_str != "":
            df_wondeals = df_wondeals.loc[
                (df_wondeals["slt_owner"] == f"{slt_owner_str}"), :]
            df_wondeals.reset_index(drop=True, inplace=True)
        df_wondeals.reset_index(drop=True, inplace=True)
        data1 = df_wondeals.loc[:, res_status_list]
        data = data1.groupby(["email_id","resource_level","project_name"]).sum() 
        
        
        data.loc[("Grand Total","",""),:] = data.apply(lambda x: sum(x))
        columns_list = []
        
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: "€{:,.2f}".format(x)
                    ) 
        
       
        return render_template(
            "wondeals_display_summary2.html",tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
                title="wondeals-dashboard",
                form=form,
                summary_name=summary_name
        )
    return render_template(
        "wondeals_display_summary2.html", title="wondeals-dashboard", form=form,summary_name=summary_name
    )



@app.route("/wondeals_dashboard_select", methods=["POST", "GET"])
def wondeals_dashboard_select():
    if request.method == "POST":
        summary_name = request.form.get("summary_name")
        if(summary_name == "wondeals_display_summary-1"):
            return redirect(url_for("wondeals_display_summary", summary_name=summary_name))
        elif(summary_name == "wondeals_display_summary-3"):
            return redirect(url_for("wondeals_display_summary2", summary_name=summary_name))
        else:
            return redirect(url_for("wondeals_display_summary1", summary_name=summary_name))
    return render_template("wondeals_dashboard_select.html")



@app.route("/demand_display_summary2", methods=["POST", "GET"])
def demand_display_summary2():
    df_demand = pd.read_sql_table("Demand", db.session.get_bind())
    print(df_demand)
    form = DemandSummaryForm()
    slt_owner_list = db.session.execute(
        "SELECT DISTINCT slt_owner FROM Demand"
    ).fetchall()
    choices_slt_owner= [("", "--select--")]
    for i in slt_owner_list:
        choices_slt_owner.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.slt_owner.choices = choices_slt_owner
    res_status_list = ["acc","dsr_id","no_of_resumes","screen_selects"]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        slt_owner_str = form.slt_owner.data
        
        if slt_owner_str != "":
            df_demand = df_demand.loc[
                (df_demand["slt_owner"] == f"{slt_owner_str}"), :]
            df_demand.reset_index(drop=True, inplace=True)
        df_demand.reset_index(drop=True, inplace=True)
        data1 = df_demand.loc[:, res_status_list]
        data = data1.groupby(["acc","dsr_id"]).sum()  
        
        data.loc[("Grand Total",""),:] = data.apply(lambda x: sum(x))
        
        columns_list=[]
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: int(x)
                    ) 
       
        return render_template(
            "demand_display_summary2.html",tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
                title="demand-dashboard",
                form=form,
                summary_name=summary_name
        )
    return render_template(
        "demand_display_summary2.html", title="demand-dashboard", form=form,summary_name=summary_name
    )


@app.route("/demand_display_summary1", methods=["POST", "GET"])
def demand_display_summary1():
    df_demand = pd.read_sql_table("Demand", db.session.get_bind())
    print(df_demand)
    form = DemandSummaryForm()
    practice_list = db.session.execute(
        "SELECT DISTINCT practice FROM Demand"
    ).fetchall()
    choices_practice= [("", "--select--")]
    for i in practice_list:
        choices_practice.append((i[0], i[0]))
    # choices_slt_owner = []
    # for i in BookingForecast.query.distinct(BookingForecast.slt_owner):
    #     choices_slt_owner.append((i.slt_owner, i.slt_owner))
    form.practice.choices = choices_practice
    res_status_list = ["slt_owner","acc","no_of_resumes","screen_selects"]
    # for i in quarter_list:
    #     choices_quarter.append((i[0], i[0]))
    # # choices_quarter = []
    # for i in BookingForecast.query.distinct(BookingForecast.quarter):
    #     choices_quarter.append((i.quarter, i.quarter))

    summary_name = request.args.to_dict().get("summary_name")

    if request.method == "POST":
        practice_str = form.practice.data
        
        if practice_str != "":
            df_demand = df_demand.loc[
                (df_demand["practice"] == f"{practice_str}"), :]
            df_demand.reset_index(drop=True, inplace=True)
        df_demand.reset_index(drop=True, inplace=True)
        data1 = df_demand.loc[:, res_status_list]
        data = data1.groupby(["slt_owner","acc"]).sum()  
        
        data.loc[("Grand Total",""),:] = data.apply(lambda x: sum(x))
        
        columns_list=[]
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: int(x)
                    ) 
       
        return render_template(
            "demand_display_summary1.html",tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
                title="demand-dashboard",
                form=form,
                summary_name=summary_name
        )
    return render_template(
        "demand_display_summary1.html", title="demand-dashboard", form=form,summary_name=summary_name
    )


@app.route("/demand_dashboard_select", methods=["POST", "GET"])
def demand_dashboard_select():
    if request.method == "POST":
        summary_name = request.form.get("summary_name")
        if(summary_name == "demand_display_summary-1"):
            return redirect(url_for("demand_display_summary", summary_name=summary_name))
        elif(summary_name == "demand_display_summary-3"):
            return redirect(url_for("demand_display_summary2", summary_name=summary_name))
        else:
            return redirect(url_for("demand_display_summary1", summary_name=summary_name))
    return render_template("demand_dashboard_select.html")


@app.route("/interview_display_summary1", methods=["POST", "GET"])
def interview_display_summary1():

    df_interview = pd.read_sql_table("interview", db.session.get_bind())
    df_interview = df_interview.iloc[:, :-2]
    form = InterviewSummaryForm()

    project_name = db.session.execute("SELECT DISTINCT project_name FROM Interview").fetchall()
    choices_project_name = [("", "--select--")]
    for i in project_name:
        choices_project_name.append((i[0], i[0]))

    list_ = db.session.execute("SELECT DISTINCT current_status FROM Interview").fetchall()
    current_status_list = ["project_name"]
    for i in list_:
        current_status_list.append(i[0])

    form.project_name.choices = choices_project_name
    if request.method == "POST":
        project_name_str = form.project_name.data
        new_cols = list(df_interview["current_status"].unique())
        if project_name_str != "":
            df_interview = df_interview.loc[(df_interview["project_name"] == f"{project_name_str}"), :]
            df_interview.reset_index(drop=True, inplace=True)
        df_interview.reset_index(drop=True, inplace=True)
        for i in new_cols:
            df_interview[i] = 0

        c = -1
        for i in df_interview["current_status"]:
            c = c + 1
            df_interview.loc[c, i] = 1

        #df_interview.dropna(subset=["dsr_id"], axis=0, inplace=True)
        data1 = df_interview.loc[:, current_status_list]
        data = data1.groupby(["project_name"]).sum()
        print(data)
        
        data.loc[("Grand Total"), :] = data.apply(lambda x: int(sum(x)))
        data.loc[:, "Total"] = data.apply(lambda x: int(sum(x)), axis=1)
        columns_list=[]
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: int(x)
                    )

        return render_template(
            "interview_display_summary1.html",
            tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
            title="interview-dashboard",
            form=form,
        )
    return render_template(
        "interview_display_summary1.html", title="interview-dashboard", form=form
    )



@app.route("/interview_display_summary", methods=["POST", "GET"])
def interview_display_summary():

    df_interview = pd.read_sql_table("interview", db.session.get_bind())
    df_interview = df_interview.iloc[:, :-2]
    form = InterviewSummaryForm()

    project_name = db.session.execute("SELECT DISTINCT project_name FROM Interview").fetchall()
    choices_project_name = [("", "--select--")]
    for i in project_name:
        choices_project_name.append((i[0], i[0]))

    
    current_status_list = ["skill","current_status"]
    '''for i in current_status_list:
        current_status_list.append('total')'''
    print(current_status_list)
   
    form.project_name.choices = choices_project_name
    if request.method == "POST":
        project_name_str = form.project_name.data
       # new_cols = list(df_interview["current_status"].unique())
        if project_name_str != "":
            df_interview = df_interview.loc[(df_interview["project_name"] == f"{project_name_str}"), :]
            df_interview.reset_index(drop=True, inplace=True)
        df_interview.reset_index(drop=True, inplace=True)
        '''for i in new_cols:
            df_interview[i] = 0

        c = -1
        for i in df_interview["current_status"]:
            c = c + 1
            df_interview.loc[c, i] = 1'''

        #df_interview.dropna(subset=["dsr_id"], axis=0, inplace=True)
        data1 = df_interview.loc[:, current_status_list]
        #data1=data1.loc[:,1:2]
        data1['Total']=''
        print(data1)

        data = data1.groupby(["skill","current_status"]).count()
        print(data)
        
       
        data.loc[("Grand Total",""), :] = data.apply(lambda x: int(sum(x)))
        #data.loc[:, "Total"] = data.apply(lambda x: int(sum(x)), axis=1)
        columns_list=[]
        for i in data.columns.values.tolist():
            columns_list.append(i)
            if len(columns_list) > 1:
                for i in columns_list:
                    data[i] = data[i].apply(
                        lambda x: int(x)
                    ) 

        return render_template(
            "interview_display_summary.html",
            tables=[data.to_html(classes="pivot", sparsify="false", header="true")],
            title="interview-dashboard",
            form=form,
        )
    return render_template(
        "interview_display_summary.html", title="interview-dashboard", form=form
    )

@app.route("/interview_dashboard_select", methods=["POST", "GET"])
def interview_dashboard_select():
    if request.method == "POST":
        summary_name = request.form.get("summary_name")
        if(summary_name == "interview_display_summary-1"):
            return redirect(url_for("interview_display_summary", summary_name=summary_name))
       
        else:
            return redirect(url_for("interview_display_summary1", summary_name=summary_name))
    return render_template("interview_dashboard_select.html")

@app.route("/resource_master_insert", methods=["POST", "GET"])
def resource_insert():
    form=Resource_Master_form()
    base_location=['DALLAS TX',
 'McKinley HillManila',
 'Mumbai - SEZ - Airoli - Gigaplex I',
 'Mumbai - SEZ - Airoli - Gigaplex II',
 'GURGAON-SEZ- Blg-1st',
 'ATLANTA GA',
 'SAN DIEGO CA',
 'Holborn',
 'Pune - Talwade Unit 2',
 'NEW YORK NY',
 'Pune - SEZ - Hinjewadi - IV',
 'Mumbai - SEZ - Airoli - CKP - I',
 'CHICAGO IL',
 'Toronto ON',
 '81 Bay Street Toronto Ontario',
 '12 Marina Boulevard Financial Center Tower 3',
 'London',
 'Hyderabad - SEZ - Phoenix Infocity - 5 flr to 6th',
 'Hyderabad - STPI - Gachibowli IT Park',
 'MISSISSAUGA-TECH ON',
 'Jalan Tun RazakKuala Lumpur',
 'Delhi - STPI â€“ Neelkanth Sant Nagar',
 'Bangalore - SEZ - Divyashree - Block 5',
 '11F No. 2 Section 5 Xin-Yi Road',
 'COLUMBIA SC',
 'Bangalore - SEZ - 6B - G flr to 3 flr',
 'Bangalore - SEZ - Divyasree - Incubation II',
 'Pune - Hinjewadi',
 'Noida - SEZ - IV',
 'Bangalore - STPI - PSN',
 'Mumbai - SEZ - Airoli Knowledge Park II',
 'SAN FRANCISCO CA',
 'London City',
 'Bangalore - STPI - EPIP - Phase II']
    start_date,roll_off='unallocated','unallocated'
    print("VIVEK -----------",form.status_project.data,form.validate_on_submit())
    if form.validate_on_submit():
        print("inside")
        region=form.region.data
        designation=form.designation.data
        adrc_1=adrc_dict_resource[region][designation_dict[designation]]
        slt_1=slt_dict[region]
        if request.form.get('status_project')!='unallocated':
            print("inside if ")
            start_date=str(form.project_start_date.data)
            roll_off=str(form.project_rolloff_date.data)
        row1=ResourceMaster(
        li_lr_id=form.li_lr_id.data ,
        region=form.region.data,
        first_name=form.first_name.data,
        middle_name=form.middle_name.data,
        last_name=form.last_name.data,
        nt_login_id=form.nt_login_id.data,
        global_date_joining=form.global_date_joining.data,
        local_date_joining=form.local_date_joining.data,
        email_id=form.email_id.data,
        project_start_date=start_date,
        project_rolloff_date=roll_off,
        sub_practice=form.sub_practice.data,
        organization=form.organization.data,
        designation=form.designation.data,
        base_location=request.form.get('base_location'),
        local_grade=form.local_grade.data,
        people_manager_name=form.people_manager_name.data,
        account_name=form.account_name.data,
        project_number=form.project_number.data,
        billability =form.billability.data,
        last_project_code=form.last_project_code.data,
        adrc=adrc_1,
        slt_owners=slt_1,
        next_assignment=form.next_assignment.data,
        remarks=form.remarks.data,
        last_working_date=form.last_working_date.data
    )
        print(form.data)
        db.session.add(row1)
        db.session.commit()
        flash("Your entry has been added!", "success")
    elif request.method == "GET":
        form_dict=request.args.to_dict()
        print(form_dict)
        form.account_name.data=form_dict.get("acc")
        form.local_grade.data=form_dict.get("emp_grade")

    return render_template('resource_insert.html',form=form,base_location=base_location)

@app.route("/<string:li_lr_id>/<string:nt_login_id>/<string:email_id>/resource_update", methods=["POST", "GET"])
def resource_update(li_lr_id,nt_login_id,email_id):
    form=Resource_Update()
    base_location=['DALLAS TX',
 'McKinley HillManila',
 'Mumbai - SEZ - Airoli - Gigaplex I',
 'Mumbai - SEZ - Airoli - Gigaplex II',
 'GURGAON-SEZ- Blg-1st',
 'ATLANTA GA',
 'SAN DIEGO CA',
 'Holborn',
 'Pune - Talwade Unit 2',
 'NEW YORK NY',
 'Pune - SEZ - Hinjewadi - IV',
 'Mumbai - SEZ - Airoli - CKP - I',
 'CHICAGO IL',
 'Toronto ON',
 '81 Bay Street Toronto Ontario',
 '12 Marina Boulevard Financial Center Tower 3',
 'London',
 'Hyderabad - SEZ - Phoenix Infocity - 5 flr to 6th',
 'Hyderabad - STPI - Gachibowli IT Park',
 'MISSISSAUGA-TECH ON',
 'Jalan Tun RazakKuala Lumpur',
 'Delhi - STPI â€“ Neelkanth Sant Nagar',
 'Bangalore - SEZ - Divyashree - Block 5',
 '11F No. 2 Section 5 Xin-Yi Road',
 'COLUMBIA SC',
 'Bangalore - SEZ - 6B - G flr to 3 flr',
 'Bangalore - SEZ - Divyasree - Incubation II',
 'Pune - Hinjewadi',
 'Noida - SEZ - IV',
 'Bangalore - STPI - PSN',
 'Mumbai - SEZ - Airoli Knowledge Park II',
 'SAN FRANCISCO CA',
 'London City',
 'Bangalore - STPI - EPIP - Phase II']
    row1 = ResourceMaster.query.get_or_404(email_id)
    form.email_id.data=email_id
    form.nt_login_id.data=nt_login_id
    form.li_lr_id.data=li_lr_id
    region=form.region.data
    designation=form.designation.data
    form.li_lr_id.render_kw = {'disabled': 'disabled'}
    form.nt_login_id.render_kw = {'disabled': 'disabled'}
    form.email_id.render_kw = {'disabled': 'disabled'}
    if form.validate_on_submit():
        adrc_1=adrc_dict_resource[region][designation_dict[designation]]
        slt_1=slt_dict[region]
        row1.first_name=form.first_name.data 
        row1.middle_name=form.middle_name.data 
        row1.last_name=form.last_name.data 
        row1.global_date_joining=form.global_date_joining.data 
        row1.local_date_joining=form.local_date_joining.data 
        row1.sub_practice=form.sub_practice.data 
        row1.organization=form.organization.data 
        row1.designation=form.designation.data 
        row1.base_location=request.form.get('base_location')
        row1.local_grade=form.local_grade.data 
        row1.people_manager_name=form.people_manager_name.data 
        row1.account_name=form.account_name.data 
        row1.project_number=form.project_number.data 
        if request.form.get('status_project')!='unallocated':
            row1.project_start_date=str(form.project_start_date.data)
            row1.project_rolloff_date=str(form.project_rolloff_date.data)
        else:
            row1.project_start_date='unallocated'
            row1.project_rolloff_date='unallocated'
        row1.billability=form.billability.data 
        row1.last_project_code=form.last_project_code.data 
        row1.adrc=adrc_1
        row1.slt_owners=slt_1
        row1.next_assignment=form.next_assignment.data
        row1.remarks=form.remarks.data 
        row1.resign_date=form.resign_date.data 
        row1.last_working_date=form.resign_date.data + timedelta(days = 90)
        db.session.commit()
        
        if form.resign_date != None:
            ids=f"select id from wondeals_table where wondeals_table.email_id =='{email_id}'"
            won_session=db.session.execute(ids).fetchall()
            for i in won_session:
                for won_id in i:
                    end_date=f"select end_date_wondeals from wondeals_table where wondeals_table.id=='{won_id}' and wondeals_table.email_id =='{email_id}'"
                    date_session=db.session.execute(end_date).fetchall()
                    date=date_session[0][0]
                    date=date.split()[0]
                    datetime_object=datetime.strptime(date,"%Y-%m-%d")
                    datetime_object=datetime_object.date()
                    lwd=form.resign_date.data+timedelta(days=90)
                    if datetime_object>lwd:
                        print(form.resign_date.data)
                        print(lwd)

                        st=f"SELECT start_date_wondeals,end_date_wondeals from wondeals_table where wondeals_table.id =='{won_id}' and wondeals_table.email_id =='{email_id}'"
                        res=db.session.execute(st).fetchall()
                        pro_dates=dict()
                        list1,list2=[],[]
                        for i,j in res:
                            list1.append(i)
                            list2.append(j)
                        update_date=f"update wondeals_table set end_date_wondeals='{lwd}' where wondeals_table.id =='{won_id}' and wondeals_table.email_id =='{email_id}'"
                        db.session.execute(update_date)
                        db.session.commit()

                        st=f"SELECT start_date_wondeals,end_date_wondeals,id,resource_country from wondeals_table where wondeals_table.id=='{won_id}' and wondeals_table.email_id =='{email_id}' "
                        res=db.session.execute(st).fetchall()
                        for i,j,k,con in res:
                            pro_dates[won_id]=functions().get_dates_list(list1,list2,datetime.strptime(i.split(' ')[0], '%Y-%m-%d'),datetime.strptime(j.split(' ')[0], '%Y-%m-%d'),con.split('_')[0])
                        months=['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
                        months_work={x:0 for x in months}
                        pro_months_dates=dict()
                        for i,j in pro_dates.items():
                            months_work={x:0 for x in months}
                            for k in j:
                                months_work[months[k.month-1]]+=1
                            pro_months_dates[i]=months_work
                        print(pro_months_dates)
                        work_hours=[]
                        for z in pro_months_dates[i].values():
                            work_hours.append(z)
                        print(work_hours)

                        st=f"SELECT revenue_daily_rate,adrc from wondeals_table where id={i} and email_id='{email_id}';"
                        print(st)
                        li=list(*db.session.execute(st).fetchall())
                        print(li)
                        revenue_daily_rate,adrc=li[0],li[1]
                        revenue_daily_rate=round(revenue_daily_rate,2)
                        adrc=round(adrc,2)
                        print("revenue daily rate = ",revenue_daily_rate)
                        print("ADRC = ",adrc)
                        eurs=[]
                        for days in work_hours:
                            eurs.append(days*revenue_daily_rate)
                        total_renvenue=sum(eurs)
                        total_renvenue=round(total_renvenue,2)
                        total_days=sum(work_hours)
                        total_cost=total_days*adrc
                        total_cost=round(total_cost,2)
                        cm=total_renvenue-total_cost
                        cm=round(cm,2)
                        cm_percent=(cm/total_renvenue)*100
                        cm_percent=round(cm_percent,2)
                        st=f'UPDATE wondeals_table SET cm={cm},total_cost={total_cost},total_revenue={total_renvenue},total_days={total_days},resource_wise_cm_percet={cm_percent}'
                        for mon in range(len(work_hours)):
                            st=st+f',days_{months[mon]}={work_hours[mon]},eur_{months[mon]}={eurs[mon]}'
                        st=st+f" where id={i} and email_id='{email_id}'"
                        db.session.execute(st)
                        db.session.commit()
       
                        
        flash("Your entry has been Updated!", "success")
    elif request.method == "GET":
        form.first_name.data = row1.first_name
        form.middle_name.data = row1.middle_name
        form.last_name.data = row1.last_name
        form.global_date_joining.data = row1.global_date_joining
        form.local_date_joining.data =row1.local_date_joining
        form.sub_practice.data = row1.sub_practice
        form.organization.data = row1.organization
        form.designation.data = row1.designation
        request.form.get('base_location') == row1.base_location
        form.local_grade.data = row1.local_grade
        form.people_manager_name.data = row1.people_manager_name
        form.account_name.data = row1.account_name
        form.project_number.data = row1.project_number
        print(row1.project_start_date=='unallocated')
        if row1.project_start_date=='unallocated' or row1.project_start_date=='Unallocated':
            print("inside date")
        else:
            form.project_start_date.data=datetime.strptime(row1.project_start_date.split(' ')[0],'%Y-%m-%d').date()
            form.project_rolloff_date.data=datetime.strptime(row1.project_rolloff_date.split(' ')[0],'%Y-%m-%d').date()
            print(request.form.get('status_project'))
        form.billability.data =row1.billability
        form.last_project_code.data=row1.last_project_code 
        form.next_assignment.data=row1.next_assignment
        form.remarks.data =row1.remarks
        form.resign_date.data=row1.resign_date 


    

        

    
    return render_template('resource_update.html',form=form,base_location=base_location)

class functions:
  def get_dates_list(self,list1,list2,start_date,end_date,con):
    holidays_list = {
        "US": [
            "30-May-23",
            "04-Jul-23",
            "05-Sep-23",
            "24-Nov-23",
            "25-Nov-23",
            "26-Dec-23",
        ],
        "GB": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "UK": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "Ne": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "ZA": [
            "03-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "02-May-23",
            "02-Jun-23",
            "03-Jun-23",
            "29-Aug-23",
            "19-Sep-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "SG": [
            "01-Jan-23",
            "01-Feb-23",
            "02-Feb-23",
            "15-Apr-23",
            "01-May-23",
            "02-May-23",
            "03-May-23",
            "15-May-23",
            "16-May-23",
            "10-Jul-23",
            "11-Jul-23",
            "09-Aug-23",
            "24-Oct-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "PH": [
            "01-Jan-23",
            "01-Feb-23",
            "25-Feb-23",
            "09-Apr-23",
            "14-Apr-23",
            "15-Apr-23",
            "16-Apr-23",
            "01-May-23",
            "12-Jun-23",
            "21-Aug-23",
            "29-Aug-23",
            "01-Nov-23",
            "30-Nov-23",
            "08-Dec-23",
            "25-Dec-23",
            "30-Dec-23",
        ],
        "NL": [
            "01-Jan-23",
            "15-Apr-23",
            "17-Apr-23",
            "18-Apr-23",
            "27-Apr-23",
            "26-May-23",
            "05-Jun-23",
            "06-Jun-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "IN": [
            "26-Jan-23",
            "21-Apr-23",
            "15-Aug-23",
            "02-Oct-23",
            "24-Oct-23",
            "25-Dec-23",
        ],
        "CA": [
            "21-Feb-23",
            "15-Apr-23",
            "23-May-23",
            "01-Jul-23",
            "01-Aug-23",
            "05-Sep-23",
            "10-Oct-23",
            "26-Dec-23",
            "27-Dec-23",
        ],
        "AU": [
            "03-Jan-23",
            "26-Jan-23",
            "15-Apr-23",
            "18-Apr-23",
            "25-Apr-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "HK": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "AE": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "MY": [
            "18-Apr-23",
            "25-Apr-23",
            "25-Dec-23",
            "26-Dec-23",
        ],
        "TW": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "SA": [
            "25-Dec-23",
            "26-Dec-23",
        ],
        "CH": [
            "25-Dec-23",
            "26-Dec-23",
        ],
    }
    holi=[]
    for i in holidays_list[con]:
        holi.append(datetime.strptime(i, '%d-%b-%y').date())
    lists=[]
    for i,j in zip(list1,list2):
        for k in pd.date_range(i,j):
            if k.date()  not in lists and k.date().weekday()<5 and k.date()>=start_date.date() and k.date()<=end_date.date() and k.date() not in holi:
                lists.append(k.date())
    return set(lists)

from sqlalchemy import create_engine
import pandas as pd 
import plotly 
import plotly.express as px
from plotly.subplots import make_subplots
@app.route("/resource_dashboard", methods=["POST", "GET"])
def resource_dashboard():
    unallocated=db.session.execute('select count(*) from resource_master where project_number="Unallocated";').fetchall()[0][0]
    allocated=db.session.execute('select count(*) from resource_master;').fetchall()[0][0]-unallocated
    fig1=px.bar(x=['unallocated','allocated'],y=[unallocated,allocated],labels=dict(x='Status',y='Count'),title='Allocated Vs Unallocated')
    graph1JSON=json.dumps(fig1,cls=plotly.utils.PlotlyJSONEncoder)
    grades_db=db.session.execute('select local_grade,count(*) from resource_master group by local_grade ;').fetchall()
    grades={i:j for i,j in grades_db}
    if 'select a value ' in grades.keys():
        del grades['select a value ']
    grades=sorted(grades.items(), key=lambda x:x[1])
    grades={i:j for i,j in grades}
    print(grades)
    fig2=px.funnel(y=grades.keys(),x=grades.values(),color=grades.keys(),orientation='h',text=grades.keys(),color_discrete_sequence=[
                 "violet", "indigo", "blue", "green", "yellow", "orange","red","pink", "hotpink", "purple", "brown"])
    #fig2.update_traces(marker_colorbar_ticklabelposition="inside", selector=dict(type='funnel'))
    fig2.update_traces(marker_opacity=1, selector=dict(type='funnel'))
    fig2.update_yaxes(tickfont_family="Arial Black")
    fig2.update_traces(insidetextfont_size=100000000)
    graph2JSON=json.dumps(fig2,cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('resource_dashboard.html', graph1JSON=graph1JSON,graph2JSON=graph2JSON,allocated=allocated,unallocated=unallocated,grades=grades)

@app.route('/get_resource_csv', methods=["POST", "GET"])
def getcsv_resource():
    data = pd.read_sql_table("resource_master", db.session.get_bind())
    data.to_excel('file.xlsx',index=False)

    print(data)
    return redirect('resource_master_display')
