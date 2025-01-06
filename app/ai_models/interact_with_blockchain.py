import requests
import os
from dotenv import load_dotenv
import datetime
import requests
from collections import Counter
import hashlib

load_dotenv()

# Fetch API key and base URL from environment variables
API_KEY = os.getenv("Ether_API_KEY")
BASE_URL = os.getenv("Ether_BASE_URL")

def get_transaction_data(transaction_id):
    """
    Fetches transaction details using Etherscan API based on a transaction hash.
    """
    params = {
        'module': 'proxy',
        'action': 'eth_getTransactionByHash',
        'txhash': transaction_id,
        'apikey': API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    data = response.json()

    if data.get('error'):
        print(f"Error fetching transaction data: {data['error']['message']}")
        return None

    if data.get('result'):
        return data['result']

    return None


    """
    Fetches the minimum and maximum ERC-20 token values sent from the specified address.
    """
    params = {
        "module": "account",
        "action": "tokentx",
        "address": address,
        "startblock": 0,
        "endblock": 99999999,
        "sort": "asc",
        "apikey": API_KEY,
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    try:
        if "result" not in data:
            raise ValueError("Unexpected response format. 'result' field not found.")

        transactions = data["result"]
        if not isinstance(transactions, list):
            raise ValueError("Unexpected 'result' type. Expected a list.")

        if not transactions:
            return None, None  # No transactions found

        values = [int(tx["value"]) / (10 ** int(tx["tokenDecimal"])) for tx in transactions]
        return min(values), max(values)

    except ValueError as ve:
        return None, None
    except Exception as e:
        return None, None

def get_wallet_metrics(sender_address):
    URL = f"https://api.etherscan.io/api?module=account&action=txlist&address={sender_address}&startblock=0&endblock=latest&sort=desc&apikey={API_KEY}"
    
    # Fetch transactions
    response = requests.get(URL)
    data = response.json()

    if data['status'] == '1':
        transactions = data['result']

        # Calculate timestamps
        timestamps_sent = [int(txn['blockNumber'], 16) for txn in transactions if txn['from'].lower() == sender_address.lower()]
        timestamps_received = [int(txn['blockNumber'], 16) for txn in transactions if txn['to'].lower() == sender_address.lower()]

        timestamps_sent.sort()
        timestamps_received.sort()

        # Calculate time differences
        time_diffs_sent = [(timestamps_sent[i] - timestamps_sent[i-1]) for i in range(1, len(timestamps_sent))]
        time_diffs_received = [(timestamps_received[i] - timestamps_received[i-1]) for i in range(1, len(timestamps_received))]

        # Calculate averages
        avg_time_sent_minutes = sum(time_diffs_sent) / len(time_diffs_sent) if len(time_diffs_sent) > 0 else 0
        avg_time_received_minutes = sum(time_diffs_received) / len(time_diffs_received) if len(time_diffs_received) > 0 else 0

        if timestamps_sent[-1] < timestamps_received[-1] and timestamps_sent[0] < timestamps_received[0]:
            time_diff_first_last = timestamps_sent[-1] - timestamps_received[0]
        elif timestamps_sent[-1] < timestamps_received[-1] and timestamps_sent[0] > timestamps_received[0]:
            time_diff_first_last = timestamps_sent[-1] - timestamps_sent[0]
        elif timestamps_sent[-1] > timestamps_received[-1] and timestamps_sent[0] > timestamps_received[0]:
            time_diff_first_last = timestamps_received[-1] - timestamps_sent[0]
        else:
            time_diff_first_last = timestamps_received[-1] - timestamps_received[0]

        avg_time_sent_minutes /= (60 * 1e-18)  # Convert to minutes
        avg_time_received_minutes /= (60 * 1e-18)  # Convert to minutes
        time_diff_first_last /= (60 * 1e-18)

        # Total transactions
        sent_tnx = len(timestamps_sent)
        received_tnx = len(timestamps_received)

        return {
            'Avg_min_between_sent_tnx': avg_time_sent_minutes,
            'Avg_min_between_received_tnx': avg_time_received_minutes,
            'Time_Diff_between_first_and_last': time_diff_first_last,
            'Sent_tnx': sent_tnx,
            'Received_tnx': received_tnx
        }
    else:
        return {'error': data['message']}

def get_transaction_metrics(sender_address):
    txlist_url = f"https://api.etherscan.io/api?module=account&action=txlist&address={sender_address}&startblock=0&endblock=latest&sort=desc&apikey={API_KEY}"
    balance_url = f"https://api.etherscan.io/api?module=account&action=balance&address={sender_address}&tag=latest&apikey={API_KEY}"
    
    # Fetch transactions
    response = requests.get(txlist_url)
    data = response.json()

    if data['status'] != '1':
        return {'error': data['message']}

    transactions = data['result']

    # Fetch balance
    response_balance = requests.get(balance_url)
    balance_data = response_balance.json()
    if balance_data['status'] != '1':
        return {'error': balance_data['message']}

    balance = int(balance_data['result']) / 1e18  # Convert balance to Ether

    # Initialize metrics
    sent_values = []
    received_values = []
    num_created_contracts = 0
    total_ether_sent = 0

    for txn in transactions:
        value_in_ether = int(txn['value']) / 1e18  # Convert value to Ether

        # Sent transactions
        if txn['from'].lower() == sender_address.lower():
            sent_values.append(value_in_ether)
            total_ether_sent += value_in_ether
            if txn['to'] == '':  # Contract creation
                num_created_contracts += 1

        # Received transactions
        if txn['to'].lower() == sender_address.lower():
            received_values.append(value_in_ether)

    # Calculate metrics
    max_value_received = max(received_values) if received_values else 0
    avg_value_received = sum(received_values) / len(received_values) if received_values else 0
    avg_value_sent = sum(sent_values) / len(sent_values) if sent_values else 0

    return {
        'Number_of_Created_Contracts': num_created_contracts,
        'Max_Value_Received': max_value_received,
        'Avg_Value_Received': avg_value_received,
        'Avg_Value_Sent': avg_value_sent,
        'Total_Ether_Sent': total_ether_sent,
        'Total_Ether_Balance': balance,
    }

def get_erc20_metrics(sender_address):
    # ERC20 transaction endpoint
    erc20_url = f"https://api.etherscan.io/api?module=account&action=tokentx&address={sender_address}&startblock=0&endblock=latest&sort=desc&apikey={API_KEY}"
    
    # Fetch ERC20 transactions
    response = requests.get(erc20_url)
    data = response.json()

    if data['status'] != '1':
        return {'error': data['message']}

    erc20_transactions = data['result']

    # Initialize metrics
    total_ether_received = 0  # Total ERC20 token received transactions in Ether
    total_ether_sent = 0  # Total ERC20 token sent transactions in Ether
    total_ether_sent_to_contract = 0  # Total ERC20 token transfer to contracts in Ether
    unique_sent_addresses = set()  # Unique account addresses for sent tokens
    unique_received_tokens = set()  # Unique tokens received
    sent_token_types = Counter()  # Counter for sent token types
    received_token_types = Counter()  # Counter for received token types

    for txn in erc20_transactions:
        # Calculate token value in Ether (based on token decimals)
        value_in_ether = int(txn['value']) / (10 ** int(txn['tokenDecimal']))
        token_name = txn['tokenName']
        token_symbol = txn['tokenSymbol']
        to_address = txn['to']
        from_address = txn['from']

        # Sent transactions
        if from_address.lower() == sender_address.lower():
            total_ether_sent += value_in_ether
            unique_sent_addresses.add(to_address)
            sent_token_types[token_symbol] += value_in_ether

            # Check if sent to a contract
            if txn.get('contractAddress'):
                total_ether_sent_to_contract += value_in_ether

        # Received transactions
        if to_address.lower() == sender_address.lower():
            total_ether_received += value_in_ether
            unique_received_tokens.add(token_name)
            received_token_types[token_symbol] += value_in_ether

    # Identify most sent and received token types
    most_sent_token_type = sent_token_types.most_common(1)[0][0] if sent_token_types else None
    most_received_token_type = received_token_types.most_common(1)[0][0] if received_token_types else None

    return {
        'ERC20_Total_Ether_Received': total_ether_received,
        'ERC20_Total_Ether_Sent': total_ether_sent,
        'ERC20_Total_Ether_Sent_Contract': total_ether_sent_to_contract,
        'ERC20_Uniq_Sent_Addr': len(unique_sent_addresses),
        'ERC20_Uniq_Rec_Token_Name': len(unique_received_tokens),
        'ERC20_Most_Sent_Token_Type': most_sent_token_type,
        'ERC20_Most_Rec_Token_Type': most_received_token_type,
    }

def hash_string_to_numeric(value):
    """Convert a string to a numeric value using SHA-256 hashing."""
    return int(hashlib.sha256(value.encode('utf-8')).hexdigest(), 16) % 100

def obtain_parameters(transaction_id):
    transaction_data = get_transaction_data(transaction_id)
    sender_address = transaction_data.get("from")

    wallet_metrics = get_wallet_metrics(sender_address)
    transaction_metrics = get_transaction_metrics(sender_address)
    erc20_metrics = get_erc20_metrics(sender_address)

    all_values = list(wallet_metrics.values()) + list(transaction_metrics.values()) + list(erc20_metrics.values())

    # Hash 'ERC20_Most_Sent_Token_Type' & 'ERC20_Most_Rec_Token_Type' to numeric values
    if isinstance(all_values[-2], str):
        all_values[-2] = hash_string_to_numeric(all_values[-2])
    if isinstance(all_values[-1], str):
        all_values[-1] = hash_string_to_numeric(all_values[-1])

    return all_values



   

    
