import requests
import hashlib
import sys

# grab the password from the command line
password_list = sys.argv[1:]
if len(password_list) == 0:
    print("Please provide a password to check.")
    sys.exit(1)


def hash_password(list):
    # Loop through the list of passwords and hash each one
    for password in list:
        # user_pw = password.encode("utf-8")
        sha1_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()

        hashed_pw_prefix = sha1_hash[0:5]
        hashed_pw_suffix = sha1_hash[5:]

        check_password(hashed_pw_prefix, hashed_pw_suffix, password)


def check_password(hashed_pw_prefix, hashed_pw_suffix, password):
    url = f"https://api.pwnedpasswords.com/range/{hashed_pw_prefix}"
    res = requests.get(url)
    hash_list = res.text.splitlines()
    found_pwd_msg = ""

    for hash in hash_list:
        if hashed_pw_suffix == hash.split(":")[0]:
            number_of_breaches = hash.split(":")[1]
            formatted_number = "{:,}".format(int(number_of_breaches))
            found_pwd_msg = f"Your password '{password}' has been breached {formatted_number} times. You should change it!"

    if found_pwd_msg:
        print(found_pwd_msg)
    else:
        print(
            f"Your password '{password}' has not been found in any breaches. Good job!"
        )


if __name__ == "__main__":
    hash_password(password_list)
