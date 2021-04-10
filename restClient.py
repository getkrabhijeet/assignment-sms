import requests
from requests.auth import HTTPBasicAuth


class Client:
    def __init__(self, auth_id, auth_token):
        self.auth_id = auth_id
        self.auth_token = auth_token
        self.auth = HTTPBasicAuth(auth_id, auth_token)
        self.BASE_URL = "https://api.plivo.com/v1/Account"
        self.last_message_uuid = ''
        self.number = self.__fetch_number__()

    def send_message(self, dst, text):
        URL = '/'.join([self.BASE_URL, self.auth_id, "Message"])
        URL += "/"
        data = dict(zip(["src", "dst", "text"], list(map(str, [self.number, dst, text]))))
        self.last_message_uuid = self.__do_post__(URL,data)["message_uuid"][0]


    def get_account_credit(self):
        URL = '/'.join([self.BASE_URL, self.auth_id])
        URL += "/"
        response = self.__do_get__(URL)
        return response['cash_credits']

    def verify_price_deduction_as_per_rate(self):
        if self.last_message_uuid:
            URL = '/'.join([self.BASE_URL, self.auth_id, "Message", self.last_message_uuid])
            URL += "/"
            price_deducted_last_message = self.__do_get__(URL)['total_amount']

            params = {"country_iso": "US"}
            URL = '/'.join([self.BASE_URL, self.auth_id, "Pricing"])
            URL += "/"
            rate_of_outbound_message = self.__do_get__(URL, params)['message']['outbound']['rate']

            print("Charge deducted for last message: " + price_deducted_last_message)
            print("Rate of Outbound message as per profile: " + rate_of_outbound_message)
            if rate_of_outbound_message == price_deducted_last_message:
                print("Charged as per Outbound rates")
            else:
                print("Charges deducted are not as per Outbound rates")
        else:
            print("No record present")
        pass

    def __do_get__(self, URL, params=None):
        return requests.get(URL, params=params, auth=self.auth).json()

    def __do_post__(self, URL, data=None):
        return requests.post(URL, auth=self.auth, data=data).json()

    def __fetch_number__(self):
        URL = '/'.join([self.BASE_URL, self.auth_id, "Number"])
        URL += "/"
        return self.__do_get__(URL)["objects"][0]["number"]


if __name__ == "__main__":
    auth_id = 'MAMWU1M2FKMZCXMWUZOG'
    auth_token = 'YjNlZTkzYTMxODE2MTcwNDk4OGRlOWFmMjczMGIy'

    #Instantiating client object using above auth_id and auth_token
    client = Client(auth_id, auth_token)

    print("Number fetched from account is : "+client.number)

    #Account credit before sending a message
    print("Account credit before sending message: "+client.get_account_credit())

    #Sending message
    print("Sending message to 17033132729...")
    client.send_message("17033132729", "Hello")

    #Verify amount deducted is as per rate
    client.verify_price_deduction_as_per_rate()

    #Account credit after sending a message
    print("Account credit after sending message: "+client.get_account_credit())

