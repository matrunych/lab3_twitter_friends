import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl


def intro():
    print("This programm gets data from twitter accounts")
    print("It will show you information about user's friends")
    acct = input('Enter Twitter Account: ')
    print("What info you you need? You can choose user's friends' names,")
    print("ids, location and date, when their accounts where created.")
    option = str(input("Enter 'id', 'name', 'location' or 'date' to get info: "))
    return acct, option


def get_json(acct):
    '''
    (str, str) -> dict
    Get friends from twitter user account and return in json
    '''
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    if (len(acct) < 1):
        acct = input('Please enter Twitter Account:')

    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': 200})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()

    js = json.loads(data)
    return js


def get_info(js, option):
    """
    (dict, str) -> list
    Return list with users' information
    """
    lst = []
    for u in js['users']:
        name = u["name"]
        if option == "name":
            lst.append(name)
        elif option == "id":
            id = u["id"]
            lst.append((name, id))
        elif option == "location":
            location = u["location"]
            if location != ' ' and location != '':
                lst.append((name, location))
            else:
                lst.append((name, "no location mentioned"))
        elif option == "date":
            date = u["created_at"]
            lst.append((name, date))
    return lst


if __name__ == "__main__":
    acct, option = intro()
    js = get_json(acct)
    print(get_info(js, option))
