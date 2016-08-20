import smtplib
import datetime
import os
from collections import OrderedDict
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

COMMASPACE = ', '

def send_email(ichi_dict):
    msg = MIMEMultipart()
    msg['Subject'] = 'Ichimoku stock screener for {}'.format(datetime.datetime.now().isoformat().split("T")[0])
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    family = ['kacperadach@gmail.com', 'alec.d.long@gmail.com', 'tomdoppenheim@gmail.com']
    msg['From'] = 'kacperadach@gmail.com'
    msg['To'] = COMMASPACE.join(family)
    message_body = get_message_body(ichi_dict)
    msg.attach(message_body)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()
    s.login('kacperadach@gmail.com', 'onehalfofmullage')
    s.sendmail('kacperadach@gmail.com', family, msg.as_string())
    s.quit()

    write_daily_report(message_body)


def write_daily_report(message_body):
    daily_report_file = os.path.join(os.path.join(os.getcwd(), 'daily_reports'),
                                     (datetime.datetime.now().isoformat().split("T")[0] + "_report.txt"))
    daily_report = open(daily_report_file, 'a')
    daily_report.write(message_body._payload)

def get_message_body(ichi_dict):
    title_text = "Daily Time Frame Ichimoku screener for {}\n".format(datetime.datetime.now().isoformat().split("T")[0])
    html_message = """
        <html>
            <body>
                <h2>{}</h2>
                <br>
                <h3>{}</h3>
                <p>{}</p>
                {}
                <h3>{}</h3>
                <h4>{}</h4>
                <p>{}</p>
                <h4>{}</h4>
                <p>{}</p>
                <h4>{}</h4>
                <p>{}</p>
                {}
                <h3>{}</h3>
                <h4>{}</h4>
                <p>{}</p>
                <h4>{}</h4>
                <p>{}</p>
            </body>
        </html>
    """.format(title_text,
               "" if not ichi_dict['overlap'] else "TK cross and Bullish Cloud Fold:",
               "" if not ichi_dict['overlap'] else str(ichi_dict['overlap']).replace("(", "").replace(")", "").replace("set", "").replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['overlap'] else "<br>",
               "Tenkan-Kijun Crosses:",
               "" if not ichi_dict['cross_above'] else "Crosses above the cloud:",
               "" if not ichi_dict['cross_above'] else str(ichi_dict['cross_above']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cross_inside'] else "Crosses inside the cloud:",
               "" if not ichi_dict['cross_inside'] else str(ichi_dict['cross_inside']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cross_below'] else "Crosses below the cloud:",
               "" if not ichi_dict['cross_below'] else str(ichi_dict['cross_below']).replace("[", "").replace("]", "").replace("'", ""),
               "<br>",
               "Cloud Movement:",
               "" if not ichi_dict['price_leaving_cloud'] else "Bullish Price Action leaving the cloud:",
               "" if not ichi_dict['price_leaving_cloud'] else str(ichi_dict['price_leaving_cloud']).replace("[", "").replace("]", "").replace("'", ""),
               "" if not ichi_dict['cloud_fold'] else "Bullish Cloud Fold:",
               "" if not ichi_dict['cloud_fold'] else str(ichi_dict['cloud_fold']).replace("[", "").replace("]", "").replace("'", ""),
               )
    return MIMEText(html_message, 'html')


    # msg = "Daily Time Frame Ichimoku screener for {}\n".format(datetime.datetime.now().isoformat().split("T")[0])
    # msg += "\n\n\n"
    # if not not ichi_dict['overlap']:
    #     msg += "TK cross and Bullish Cloud Fold:\n\n"
    #     for ticker in ichi_dict['overlap']:
    #         msg += ticker + ", "
    # msg += "\n\nTenkan-Kijun Crosses:"
    # if not not ichi_dict['cross_above']:
    #     msg += "\n\nCrosses above the cloud:\n\n"
    #     for ticker in ichi_dict['cross_above']:
    #         msg += ticker + ", "
    # if not not ichi_dict['cross_inside']:
    #     msg += "\n\nCrosses inside the cloud:\n\n"
    #     for ticker in ichi_dict['cross_inside']:
    #         msg += ticker + ", "
    # if not not ichi_dict['cross_below']:
    #     msg += "\n\nCrosses below the cloud:\n\n"
    #     for ticker in ichi_dict['cross_below']:
    #         msg += ticker + ", "
    # if not not ichi_dict['price_leaving_cloud']:
    #     msg += "\n\n\nBullish Price Action leaving the cloud:\n\n"
    #     for ticker in ichi_dict['price_leaving_cloud']:
    #         msg += ticker + ", "
    # if not not ichi_dict['cloud_fold']:
    #     msg += "\n\nBullish Cloud Fold:\n\n"
    #     for ticker in ichi_dict['cloud_fold']:
    #         msg += ticker + ", "
    # return MIMEText(msg, 'plain')

