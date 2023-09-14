import imaplib
import email
from bs4 import BeautifulSoup
import smtplib
from netmiko import ConnectHandler
from email.mime.text import MIMEText

# Your email login credentials
email_address = "xyz@gmail.com"
password = "passwd"

# Connect to your email server (e.g., Gmail)
mail = imaplib.IMAP4_SSL("imap.gmail.com")
mail.login(email_address, password)

# Select the mailbox you want to read emails from (e.g., Inbox)
mail.select("inbox")

# Search for the last unread email with the desired subject
# Change "Your Subject" to the subject of the email you're looking for
result, email_ids = mail.search(None, '(UNSEEN SUBJECT "Down")')

# Check if there are any unread emails with the specified subject
if email_ids[0]:
    # Get the latest email ID (assuming it's the most recent unread email)
    latest_email_id = email_ids[0].split()[-1]

    # Fetch the email content using the latest email ID
    result, email_data = mail.fetch(latest_email_id, "(RFC822)")

    # Parse the email content
    raw_email = email_data[0][1]
    email_message = email.message_from_bytes(raw_email)

    # Find the HTML part of the email (assuming it's multipart)
    html_content = None
    for part in email_message.walk():
        if part.get_content_type() == "text/html":
            html_content = part.get_payload(decode=True).decode()

    # If HTML content is found, parse it for the table
    if html_content:
        soup = BeautifulSoup(html_content, "html.parser")
        # Find the table element(s) in the HTML
        tables = soup.find_all("table")

        # Assuming you want to extract data from the first table found
        if tables:
            table = tables[0]
            # Extract table data into a variable
            table_data = []
            for row in table.find_all("tr"):
                row_data = [cell.get_text(strip=True) for cell in row.find_all("td")]
                table_data.append(row_data)

            # Now, table_data contains the data from the table
            # You can work with this data as needed
            print(table_data)
            first_row = table_data[0]
            second_row = table_data[1]
            third_row = table_data[2]

            domain = first_row[0]
            domain_value = first_row[1]

            ip = second_row[0]
            ip_value = second_row[1]

            status = third_row[0]
            status_value = third_row[1]

            print("Domain :", domain_value)
            print("IP :", ip_value )
            print("Status :", status_value )
            device = {

                    'device_type': 'cisco_ios',

                    'ip': ip_value,   # Replace with the IP address of your Cisco device

                    'username': 'cisco',

                    'password': 'cisco',

                    }
            try:

                net_connect = ConnectHandler(**device)
            except Exception as e:

                print(f"Failed to connect to the device: {e}")

                exit()
            try:

                ping_result = net_connect.send_command("ping 192.168.1.209")  # Replace with the IP you want to ping
                if "Success rate is 0 percent" in ping_result:

                    print("Ping failed. No response.")
                    sender_email = email_message.get('from')
                    reply_subject = "Re: " + email_message['subject']
                    reply_message = """
                    Hello,

                    Thank you for your email.
                    Please raise a Docket with ISP for further investigation.

                    Domain: {}
                    Ip: {}
                    Status: {}

                    Best regards,
                    Praveen Sreeedharan
                    """.format(domain_value, ip_value, status_value)
                    print(reply_message)
                    smtp_server = "smtp.gmail.com"
                    smtp_port = 587
                    smtp_username = "praveensreedha@gmail.com"
                    smtp_password = "uwluatmjroofdvpc"

                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                        server.starttls()
                        server.login(smtp_username, smtp_password)
                        msg = MIMEText(reply_message)
                        msg['Subject'] = reply_subject
                        msg['From'] = smtp_username
                        msg['To'] = sender_email
                        server.sendmail(smtp_username, sender_email, msg.as_string())
                    print("Reply sent successfully.")

                else:

                    print("Ping successful. Response received.")

                    print(ping_result)
            
            except Exception as e:

                print(f"Error executing the ping command: {e}")
            net_connect.disconnect()
        else:
            print("No tables found in the email.")
    else:
        print("No HTML content found in the email.")
else:
    print("No unread emails with the specified subject found in the inbox.")

# Close the mailbox
mail.logout()
