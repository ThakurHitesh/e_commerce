import razorpay
import os

razorpay_connection = razorpay.Client(auth=(os.environ['RAZOR_PAY_API_KEY'], os.environ['RAZOR_PAY_API_SECRET']))
