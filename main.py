import requests, threading, names, random, string, os
from random import randint
from random import randrange
from multiprocessing import Process
print("Welcome to USMint bot V2. Attempting ATC ")
threads = 1
def main():
    global s, cc, randoAddy, rando, house_jigged
    global first
    global last
    global cc_last4
    global expMo
    global expYr
    global cvv
    global addy
    global city
    global postal
    global state
    global phoneNumber
    def atc(pid):
        completeAtc = False
        while not completeAtc:
            try:
                headers = {
                    'authority': 'catalog.usmint.gov',
                    'accept': '*/*',
                    'dnt': '1',
                    'x-requested-with': 'XMLHttpRequest',
                    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.59 (Edition beta)',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    'origin': 'https://catalog.usmint.gov',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-dest': 'empty',
                    'referer': 'https://catalog.usmint.gov/american-eagle-2020-one-ounce-silver-proof-coin-20EA.html?cgid=bestsellers',
                    'accept-language': 'en-US,en;q=0.9'}

                params = (
                    ('format', 'ajax'),
                )

                data = {
                    'cartAction': 'add',
                    'pid': f'{pid}',
                    'cgid': 'bestsellers',
                    'egc': 'null',
                    'navid': '',
                    'Quantity': '1'
                }

                response = s.post(
                    'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-AddProduct',
                    headers=headers, params=params, data=data)
                res = response.text
                quantity = res.split('<span class="value">')[1].split('</span>')[0]
                subtotal = res.split('<span class="value">')[2].split('</span>')[0]
                print(quantity + " item added to cart for a subtotal of " + subtotal)
                if int(quantity) > 0:
                    completeAtc = True
                else:
                    pass


            except Exception as ex:
                print(ex)
                print("Error on ATC... Retrying.")

    def getVals():
        global cartUrl
        global shippingSecure
        global billingSecure
        try:
            response = s.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show')
            shippingSecure = response.text.split('name="dwfrm_singleshipping_securekey" value="')[1].split('"/')[0]
            cartUrl = response.text.split('<form action="')[1].split('"')[0]
            billingSecure = response.text.split('"dwfrm_billing_securekey" value="')[1].split('"/')[0]
        except:
            print('Value errors... retrying')
            print(response.text)
            getVals()

    def validate():
        res = s.get("https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-ValidateBulkLimit")
        if res.text == 'success':
            return True
        else:
            return False

    def setAddress():
        headers = {
            'authority': 'catalog.usmint.gov',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.59 (Edition beta)',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
            'accept-language': 'en-US,en;q=0.9'}

        params = (
            ('avsdata',
             '{"firstname":"Evan","lastname":"","address1":"","address2":"","city":"","postalCode":"","state":"NY","country":"US"}'),
        )

        response = s.get('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/AVS-ajax',
                         headers=headers, params=params)
        json = response.json()
        errors = json['status']['ErrorCode']

        headers = {
            'authority': 'catalog.usmint.gov',
            'accept': 'text/html, */*; q=0.01',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.59 (Edition beta)',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://catalog.usmint.gov',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
            'accept-language': 'en-US,en;q=0.9'}

        data = {
            'dwfrm_singleshipping_shippingAddress_addressFields_selectedAddressID': 'newaddress',
            'dwfrm_singleshipping_shippingAddress_addressFields_firstName': f'{first}',
            'dwfrm_singleshipping_shippingAddress_addressFields_lastName': f'{last}',
            'dwfrm_singleshipping_shippingAddress_addressFields_phone': f'{phoneNumber}',
            'dwfrm_singleshipping_shippingAddress_email': 'evstwo@gmail.com',
            'dwfrm_billing_billingAddress_emailsource': 'Website - Checkout',
            'dwfrm_singleshipping_shippingAddress_addressFields_address1': f'{house_jigged}',
            'dwfrm_singleshipping_shippingAddress_addressFields_address2': '',
            'dwfrm_singleshipping_shippingAddress_addressFields_city': f'{city}',
            'dwfrm_singleshipping_shippingAddress_addressFields_states_state': f'{city}',
            'dwfrm_singleshipping_shippingAddress_addressFields_zip': f'{postal}',
            'dwfrm_singleshipping_shippingAddress_addressFields_country': 'US',
            'dwfrm_singleshipping_shippingAddress_isCreateAccountSelected': 'false',
            'dwfrm_singleshipping_createAccount_password': '',
            'dwfrm_singleshipping_createAccount_passwordconfirm': '',
            'dwfrm_singleshipping_createAccount_question': '1',
            'dwfrm_singleshipping_createAccount_answer': '',
            'dwfrm_singleshipping_securekey': f'{shippingSecure}',
            'dwfrm_billing_securekey': f'{billingSecure}',
            'format': 'ajax',
            'refresh': 'shipping',
            'dwfrm_singleshipping_shippingAddress_applyShippingAddress': ''
        }

        s.post(f'{cartUrl}', headers=headers, data=data)

        if errors != 0:
            return False
        if errors == 0:
            return True

    def setCardPay():
        headers = {
            'authority': 'catalog.usmint.gov',
            'accept': 'text/html, */*; q=0.01',
            'dnt': '1',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.59 (Edition beta)',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://catalog.usmint.gov',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
            'accept-language': 'en-US,en;q=0.9'}

        data = [
            ('dwfrm_singleshipping_shippingAddress_useAsBillingAddress', 'true'),
            ('dwfrm_billing_billingAddress_addressFields_selectedAddressID', ''),
            ('dwfrm_billing_billingAddress_addressFields_firstName', f'{first}'),
            ('dwfrm_billing_billingAddress_addressFields_lastName', f'{last}'),
            ('dwfrm_billing_billingAddress_addressFields_address1', f'{house_jigged}'),
            ('dwfrm_billing_billingAddress_addressFields_address2', ''),
            ('dwfrm_billing_billingAddress_addressFields_city', f'{city}'),
            ('dwfrm_billing_billingAddress_addressFields_states_state', f'{state}'),
            ('dwfrm_billing_billingAddress_addressFields_zip', f'{postal}'),
            ('dwfrm_billing_billingAddress_addressFields_country', 'US'),
            ('dwfrm_billing_billingAddress_addressFields_phone', f'{phoneNumber}'),
            ('dwfrm_billing_billingAddress_email_emailAddress', ''),
            ('dwfrm_billing_securekey', f'{billingSecure}'),
            ('dwfrm_billing_securekey', f'{billingSecure}'),
            ('dwfrm_singleshipping_securekey', f'{shippingSecure}'),
            ('refresh', 'payment'),
            ('format', 'ajax'),
            ('dwfrm_billing_applyBillingAndPayment', ''),
            ('dwfrm_billing_paymentMethods_selectedPaymentMethodID', 'CREDIT_CARD'),
            ('dwfrm_billing_paymentMethods_creditCard_type', 'Visa'),
            ('dwfrm_billing_paymentMethods_creditCard_owner', 'Evan'),
            ('dwfrm_billing_paymentMethods_creditCard_number', f'{cc}'),
            ('dwfrm_billing_paymentMethods_creditCard_month', f'{expMo}'),
            ('dwfrm_billing_paymentMethods_creditCard_year', f'{expYr}'),
            ('dwfrm_billing_paymentMethods_creditCard_cvn', f'{cvv}'),
            ('dwfrm_emailsignup_phone', ''),
        ]

        resp = s.post(f'{cartUrl}', headers=headers, data=data)
        res = s.get(
            'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show?format=ajax&refresh=payment_summaries&format=ajax')
        headers = {
            'authority': 'catalog.usmint.gov',
            'cache-control': 'max-age=0',
            'origin': 'https://catalog.usmint.gov',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 OPR/70.0.3728.59 (Edition beta)',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/Cart-Show',
            'accept-language': 'en-US,en;q=0.9'}

        data = {
            'dwfrm_billing_paymentMethods_selectedPaymentMethodID': 'CREDIT_CARD',
            'dwfrm_billing_paymentMethods_creditCard_type': 'Visa',
            'dwfrm_billing_paymentMethods_creditCard_owner': 'Evan',
            'dwfrm_billing_paymentMethods_creditCard_number': f'************{cc_last4}',
            'dwfrm_billing_paymentMethods_creditCard_month': f'{expMo}',
            'dwfrm_billing_paymentMethods_creditCard_year': f'{expYr}',
            'dwfrm_billing_paymentMethods_creditCard_cvn': '***',
            'dwfrm_billing_securekey': f'{billingSecure}',
            'dwfrm_emailsignup_phone': ''
        }
        response = s.post('https://catalog.usmint.gov/on/demandware.store/Sites-USM-Site/default/COSummary-Submit',
                          headers=headers, data=data)
        if '<div class="errorform">' in response.text:
            print("Error detected: " + response.text.split('<div class="errorform">')[1].split('</div>')[0])
        else:
            print("No error detected. Possible checkout? ")
        main()

    for x in range(1):
        s = requests.session()
        line = random.choice(open(r'/home/evxn/PycharmProjects/mint/proxies.txt').readlines())
        splitproxy = line.split(':')
        ip = splitproxy[0]
        port = splitproxy[1]
        proxies = {
            'http': f'http://user:pass@{ip}:{port}',
            'https': f'https://user:pass@{ip}:{port}',
        }
        s.proxies = proxies
        cards = ['4060699459226021:2/2022:187', '4143974592745559:1/2025:200'] #fake card numbers
        cardInfo = random.choice(cards)
        cardSplit = cardInfo.split(':')
        name = names.get_full_name(gender='male')
        list = name.split(' ')
        first = list[0]
        last = list[1]
        cc = cardSplit[0]
        cc_last4 = cc[12:]
        exp = cardSplit[1]
        splitexp = exp.split('/')
        expMo = splitexp[0]
        expYr = splitexp[1]
        cvv = cardSplit[2]
        addy = ''
        city = ''
        postal = ''
        state = 'NY'
        def random_with_N_digits(n):
            range_start = 10 ** (n - 1)
            range_end = (10 ** n) - 1
            return randint(range_start, range_end)

        phoneNumber = random_with_N_digits(10)

        def random_string_generator_variable_size(min_size, max_size, allowed_chars):
            return ''.join(random.choice(allowed_chars) for x in range(randint(min_size, max_size)))

        chars = string.ascii_letters
        randoAddy = random_string_generator_variable_size(3, 3, chars)
        apt = randrange(99)
        split = addy.split(" ")
        i = len(split)
        join = ' '.join(split[1: i])
        house_jigged = f'{addy[0]} {randoAddy} {join}'
        rando = random_string_generator_variable_size(6, 12, chars)
        atc(pid="19XE")
        getVals()
        if not validate():
            main()
        if not setAddress():
            main()
        setCardPay()

processes = []
for i in range(os.cpu_count()):
    processes.append(Process(target=main))
for process in processes:
    process.start()
for process in processes:
    process.join()
