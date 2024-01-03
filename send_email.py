"""Code to send an email using the Gmail SMTP server."""

__author__ = "Adam Kippenhan"
__copyright__ = "Copyright 2024, Adam Kippenhan"
__maintainer__ = "Adam Kippenhan"
__license__ = "MIT"
__status__ = "Production"

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os import remove
from os.path import isfile
from pathlib import Path
from smtplib import SMTP
from traceback import format_exc
from typing import List, Optional, Tuple, Union

from custom_logger import CustomLogger


def get_secrets(
    secrets_file: Path,
    username_tag: str,
    password_tag: str,
    log_file: Union[Path, str] = "stdout",
) -> Tuple[str, str]:
    """Get secrets from a given file and return them as a tuple.

    Parameters
    ----------
    secrets_file : Path
        The file containing the secrets.
    username_tag : str
        The username tag of the desired username in the secrets file.
    password_tag : str
        The password tag of the desired password in the secrets file.
    log_file : Union[Path, str], optional
        The log file for this function or stdout. Defaults to "stdout".

    Returns
    -------
    Tuple[str, str]
        A tuple containing the desired username and password.

    Raises
    ------
    ValueError
        If username_tag or password_tag cannot be found in secrets_file.
    """
    lg = CustomLogger(log_file)
    lg.info(f"Loading secrets for '{username_tag}' from '{secrets_file}'...")

    if not isfile(secrets_file):
        lg.error(f"File '{secrets_file}' does not exist!")
        raise Exception(f"File '{secrets_file}' does not exist!")

    username = password = ""
    with open(secrets_file, "r") as f:
        for line in f:
            if line.startswith(username_tag):
                username = line.partition(":")[2].strip()
            if line.startswith(password_tag):
                password = line.partition(":")[2].strip()

        # Ensure that username_tag and password_tag are present in secrets_file.
        if username == "":
            raise ValueError(
                f"Username tag: '{username_tag}' not found in '{secrets_file}'!"
            )
        if password == "":
            raise ValueError(
                f"Password tag: '{password_tag}' not found in '{secrets_file}'!"
            )

    lg.info("Secrets loaded successfully!")
    return username, password


def send_email(
    recipients: List[str],
    subject: str,
    body: str,
    secrets_file: Path,
    username_tag: str = "gmail_username",
    password_tag: str = "gmail_password",
    log_file: Union[Path, str] = "stdout",
    html: bool = False,
    attachments: Optional[List[Path]] = None,
):
    """Send an email using the Gmail SMTP server.

    Parameters
    ----------
    recipients : List[str]
        A list of email recipients. A value of ["DEBUG"] will address the email
        to the sender.
    subject : str
        The subject of the email.
    body : str
        The body of the email.
    secrets_file : Path
        The file containing email credentials.
    username_tag : str, optional
        The tag for the email username in the secrets file. Defaults to
        "gmail_username".
    password_tag : str, optional
        The tag for the email password in the secrets file. Defaults to
        "gmail_password".
    log_file : Union[Path, str], optional
        The log file for this function or stdout. Defaults to "stdout".
    html : bool, optional
        Whether or not to encode the body as html. Defaults to False.
    attachments : Optional[List[Path]]
        A list of files to attach to the email. Defaults to None.
    """
    lg = CustomLogger(log_file)

    # Get the email credentials.
    username, password = get_secrets(
        secrets_file=secrets_file,
        username_tag=username_tag,
        password_tag=password_tag,
        log_file=log_file,
    )

    # Address the email to the sender if recipients is ["DEBUG"].
    if recipients == ["DEBUG"]:
        recipients = [username]

    lg.info(f"Creating new email to recipient(s): {', '.join(recipients)}...")

    message = MIMEMultipart()
    message["From"] = username
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject

    message.attach(MIMEText(body, "html")) if html else message.attach(MIMEText(body))

    # Attach the given attachment(s) to the email.
    if attachments is not None:
        for attachment in attachments:
            lg.debug(f"Attaching '{attachment}' to email....")
            with open(attachment, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={attachment.name}",
            )
            message.attach(part)
    text = message.as_string()

    # Send the email.
    with SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(username, password)
        server.sendmail(username, recipients, text)

    lg.info("Email sent successfully!")


def test_send_email(
    secrets_file: Path,
    username_tag: str = "gmail_username",
    password_tag: str = "gmail_password",
    log_file: Union[Path, str] = "stdout",
    include_attachment: bool = False,
):
    """Test send_email by sending a simple test email.

    Parameters
    ----------
    secrets_file : Path
        The file containing email credentials.
    username_tag : str, optional
        The tag for the email username in the secrets file. Defaults to
        "gmail_username".
    password_tag : str, optional
        The tag for the email password in the secrets file. Defaults to
        "gmail_password".
    log_file : Union[Path, str], optional
        The log file for this function or stdout. Defaults to "stdout".
    include_attachment : bool, optional
        Whether or not to include an attachment in the test email. Defaults to
        False.
    """
    lg = CustomLogger(log_file)

    lg.info("====== INITIALIZING... ======")

    lg.info("Attempting to send test email...")

    if include_attachment:
        # Create a simple test attachment file.
        with open("test.txt", "x") as f:
            f.write("This is a test attachment.\n")
        test_file = open("test.txt", "r")
        try:
            send_email(
                recipients=["DEBUG"],
                subject="Test Email",
                body="This is a test.",
                secrets_file=secrets_file,
                username_tag=username_tag,
                password_tag=password_tag,
                log_file=log_file,
                attachments=[Path(test_file.name)],
            )
        # Catch any exceptions raised by send_email.
        except Exception as e:
            lg.error(f"Exception occurred: {e}\n{format_exc().strip()}")
        finally:
            # Remove the test attachment file.
            test_file.close()
            remove(Path(test_file.name))
    else:
        try:
            send_email(
                recipients=["DEBUG"],
                subject="Test Email",
                body="This is a test.",
                secrets_file=args.secrets_file,
                username_tag=username_tag,
                password_tag=password_tag,
                log_file=log_file,
            )
        # Catch any exceptions raised by send_email.
        except Exception as e:
            lg.error(f"Exception occurred: {e}\n{format_exc().strip()}")

    lg.info("====== TERMINATED ======")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="option")
    message_parser = subparsers.add_parser(
        "message",
        help="Send an email with recipient(s), a subject and a body specified "
        "on the command line or from a file with one or more optional email "
        "attachments specified from the command line. A secrets file must also "
        "be specified.",
    )
    message_parser.add_argument(
        "-f",
        "--file",
        type=Path,
        required=False,
        help="Read email recipients, subject and body from a file. The first "
        "line of the file will be interpreted as the email recipients (comma "
        "separated), the second line as the email subject and the remaining "
        "file contents will be interpreted as the email body.",
    )
    message_parser.add_argument(
        "--recipients",
        nargs="+",
        type=str,
        required=False,
        help="The email address(es) to send the email to.",
    )
    message_parser.add_argument(
        "--subject",
        type=str,
        required=False,
        help="The subject of the email to send.",
    )
    message_parser.add_argument(
        "--body",
        type=str,
        required=False,
        help="The body of the email to send.",
    )
    message_parser.add_argument(
        "--attachments",
        nargs="+",
        type=Path,
        required=False,
        help="A list of files, separated by spaces, to attach to the email.",
    )
    message_parser.add_argument(
        "--secrets-file",
        type=Path,
        required=True,
        help="The file containing credentials for the email sender.",
    )
    message_parser.add_argument(
        "--username-tag",
        default="gmail_username",
        type=str,
        required=False,
        help="The tag for the email username in the secrets file. Defaults to "
        "'gmail_username'.",
    )
    message_parser.add_argument(
        "--password-tag",
        default="gmail_password",
        type=str,
        required=False,
        help="The tag for the email username in the secrets file. Defaults to "
        "'gmail_password'.",
    )
    test_parser = subparsers.add_parser(
        "test",
        help="Send a test email with an optional test attachment.",
    )
    test_parser.add_argument(
        "--secrets-file",
        type=Path,
        required=True,
        help="The file containing credentials for the email sender.",
    )
    test_parser.add_argument(
        "--username-tag",
        default="gmail_username",
        type=str,
        required=False,
        help="The tag for the email username in the secrets file. Defaults to "
        "'gmail_username'.",
    )
    test_parser.add_argument(
        "--password-tag",
        default="gmail_password",
        type=str,
        required=False,
        help="The tag for the email username in the secrets file. Defaults to "
        "'gmail_password'.",
    )
    test_parser.add_argument(
        "--include-attachment",
        action="store_true",
        required=False,
        help="Include a simple test attachment in the test email.",
    )
    parser.add_argument(
        "--log-file",
        default="stdout",
        required=False,
        help="The log file for this application or stdout. Defaults to 'stdout'.",
    )
    args = parser.parse_args()

    log_file = "stdout" if args.log_file == "stdout" else Path(args.log_file)

    lg = CustomLogger(log_file)

    if args.option == "message":
        lg.info("====== INITIALIZING... ======")
        if not args.file and not args.recipients:
            parser.error(
                "Recipients must be specified either in file or with --recipients option!"
            )
        if args.file:  # Read email contents from a file.
            if not isfile(args.file):
                lg.error(f"File '{args.file}' does not exist!")
                raise Exception(f"File '{args.file}' does not exist!")
            with open(args.file) as f:
                recipients = f.readline().strip().split(",")
                if not recipients[0]:
                    lg.error(f"File '{args.file}' is empty!")
                    raise Exception(f"File '{args.file}' is empty!")
                subject = f.readline().strip()
                body = f.read()
        else:
            recipients = args.recipients
            subject = args.subject
            body = args.body
        send_email(
            recipients=recipients,
            subject=subject,
            body=body,
            secrets_file=args.secrets_file,
            log_file=log_file,
            attachments=args.attachments,
        )
        lg.info("====== TERMINATED ======")

    if args.option == "test":
        test_send_email(
            secrets_file=args.secrets_file,
            username_tag=args.username_tag,
            password_tag=args.password_tag,
            log_file=log_file,
            include_attachment=args.include_attachment,
        )
