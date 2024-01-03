# Email Sender

This is an application to send emails using the Gmail SMTP server.

## Requirements

### Installing Python Modules

The Python modules used for developing this application can be found in [`requirements.txt`](requirements.txt). To install these modules, run the following:

```bash
pip install -r requirements.txt
```

### Google Account

The sender email address must be a Google-based email as this application uses the Gmail SMTP server to send emails. For long-term or frequent use of this application, it might be a good idea to create a dedicated Google account to use solely with this application.

### Secrets File

A secrets file should be created containing credentials for the Google account. Since the password must be placed in the secrets file, it is recommended that an app password be used for this application. Instructions for how to create an app password can be found [here](https://support.google.com/accounts/answer/185833?hl=en&sjid=12652931280380728633-NA). This will require the account to have 2-Step Verification enabled. See [`template_secrets.txt`](template_secrets.txt) for an example of how to format the secrets file. It is important to note that `template_secrets.txt` is merely a template and should be copied and renamed **BEFORE** populating the values in order to protect sensitive information.

## Usage

The main file in this application is [`send_email.py`](send_email.py). Usage instructions for running this file on the command line are as follows:

```
usage: send_email.py [-h] [--log-file LOG_FILE] {message,test} ...

positional arguments:
  {message,test}
    message            Send an email with recipient(s), a subject and a body specified on
                       the command line or from a file with one or more optional email
                       attachments specified from the command line. A secrets file must also
                       be specified.
    test               Send a test email with an optional test attachment.

options:
  -h, --help           Show this help message and exit.
  --log-file LOG_FILE  The log file for this application or stdout. Defaults to 'stdout'.
```

### Sending an Email

The `message` option allows for an email to be sent using command line arguments. Usage instructions for this option are as follows:

```
usage: send_email.py message [-h] [-f FILE] [--recipients RECIPIENTS [RECIPIENTS ...]]
                             [--subject SUBJECT]
                             [--body BODY] [--attachments ATTACHMENTS [ATTACHMENTS ...]]
                             --secrets-file SECRETS_FILE [--username-tag USERNAME_TAG]
                             [--password-tag PASSWORD_TAG]

options:
  -h, --help            Show this help message and exit.
  -f FILE, --file FILE  Read email recipients, subject and body from a file. The first line
                        of the file will be interpreted as the email recipients (comma
                        separated), the second line as the email subject and the remaining
                        file contents will be interpreted as the email body.
  --recipients RECIPIENTS [RECIPIENTS ...]
                        The email address(es) to send the email to.
  --subject SUBJECT     The subject of the email to send.
  --body BODY           The body of the email to send.
  --attachments ATTACHMENTS [ATTACHMENTS ...]
                        A list of files, separated by spaces, to attach to the email.
  --secrets-file SECRETS_FILE
                        The file containing credentials for the email sender.
  --username-tag USERNAME_TAG
                        The tag for the email username in the secrets file. Defaults to
                        'gmail_username'.
  --password-tag PASSWORD_TAG
                        The tag for the email username in the secrets file. Defaults to
                        'gmail_password'.
```

### Sending a Test Email

The `test` option will send a simple test email to the sender, which can be used as an easy way to ensure the application is working correctly. Usage instructions for this option are as follows:

```
usage: send_email.py test [-h] --secrets-file SECRETS_FILE [--username-tag USERNAME_TAG]
                          [--password-tag PASSWORD_TAG] [--include-attachment]

options:
  -h, --help            Show this help message and exit.
  --secrets-file SECRETS_FILE
                        The file containing credentials for the email sender.
  --username-tag USERNAME_TAG
                        The tag for the email username in the secrets file. Defaults to
                        'gmail_username'.
  --password-tag PASSWORD_TAG
                        The tag for the email username in the secrets file. Defaults to
                        'gmail_password'.
  --include-attachment  Include a simple test attachment in the test email.
```

## Custom Logger

This application also includes a custom logger implementation, found in [`custom_logger.py`](custom_logger.py). This was used in place of the standard python logging module for various reasons. The logger will write log statements to stdout by default, but can also write to a user-specified log file. Each log statement wil include a timestamp in the format 'yyyy-mm-dd HH:MM:SS,nnn', the log level, the name of the function calling the logger and the line number that the logger is being called from. Below is an example of a log statement.

```
2024-01-02 13:24:41,614 [INFO main 1] Hello World!
```
