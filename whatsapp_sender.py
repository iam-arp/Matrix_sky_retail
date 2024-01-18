# whatsapp_sender.py
import pywhatkit as wa
import sys

def send_whatsapp_message(number, message, hours, minutes):
    wa.sendwhatmsg_instantly(number, message, hours, minutes)

if __name__ == "__main__":
    # Read command-line arguments for WhatsApp message details
    number, message, hours, minutes = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
    send_whatsapp_message(number, message, hours, minutes)
