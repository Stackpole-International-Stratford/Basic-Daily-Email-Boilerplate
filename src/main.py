import requests

def send_curl_request():
    url = 'http://10.4.1.234/barcode/api/parts-scanned-last-24-hours/'

    try:
        # Send GET request
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            print('Request successful:', response.text)
        else:
            print(f'Failed to send request. Status code: {response.status_code}')
            print('Response:', response.text)

    except Exception as e:
        print(f'An error occurred: {e}')

if __name__ == '__main__':
    send_curl_request()
